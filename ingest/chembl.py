"""
ARP v22 - ChEMBL Data Ingestion

ChEMBL is a manually curated database of bioactive molecules with drug-like properties.
License: CC BY-SA 3.0 (share-alike for derivatives)

API Documentation: https://www.ebi.ac.uk/chembl/chemblws/
"""

import httpx
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Iterator
from datetime import datetime
from pathlib import Path
import pandas as pd


@dataclass
class ChEMBLConfig:
    """Configuration for ChEMBL ingestion"""
    version: str = "34"
    base_url: str = "https://www.ebi.ac.uk/chembl/api"
    max_results: int = 10000
    min_activity_value: float = 10000  # nM - only more potent
    target_types: List[str] = field(default_factory=lambda: [
        "SINGLE PROTEIN",
        "PROTEIN COMPLEX",
        "PROTEIN FAMILY",
    ])
    assay_types: List[str] = field(default_factory=lambda: [
        "B",
        "F",
        "A",
    ])  # B=Binding, F=Functional, A=ADME
    

class ChEMBLClient:
    """
    Client for ChEMBL API.
    
    Usage:
        client = ChEMBLClient()
        df = client.fetch_activities_by_target("THRB")
        df = client.fetch_drugs_by_indication("MASH")
    """
    
    BASE_URL = "https://www.ebi.ac.uk/chembl/api"
    
    def __init__(self, config: Optional[ChEMBLConfig] = None):
        self.config = config or ChEMBLConfig()
        self.session = httpx.Client(timeout=60.0)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """Make GET request to ChEMBL API"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def _paginate(self, endpoint: str, params: Dict = None) -> Iterator[Dict]:
        """Paginate through API results"""
        page = 1
        total_pages = 1
        
        while page <= total_pages:
            query_params = params.copy() if params else {}
            query_params.update({
                "page": page,
                "limit": 1000,
            })
            
            data = self._get(endpoint, query_params)
            
            page_meta = data.get("page_meta", {})
            total_pages = page_meta.get("total_pages", 1)
            page = page_meta.get("next_page") or page + 1
            
            for item in data.get("activities", data.get("molecules", data.get("targets", []))):
                yield item
            
            # Rate limiting
            time.sleep(0.5)
    
    def fetch_molecule_by_chembl_id(self, chembl_id: str) -> Dict:
        """Fetch molecule details by ChEMBL ID"""
        return self._get(f"molecule/{chembl_id}.json")
    
    def fetch_target_by_uniprot(self, uniprot_id: str) -> Dict:
        """Fetch target by UniProt ID"""
        data = self._get(f"target/uniprot/{uniprot_id}.json")
        return data.get("targets", [{}])[0] if data.get("targets") else {}
    
    def fetch_activities_by_target(
        self,
        target_chembl_id: str,
        min_value: Optional[float] = None,
    ) -> pd.DataFrame:
        """
        Fetch all bioactivity data for a target.
        
        Args:
            target_chembl_id: ChEMBL target ID (e.g., "CHEMBL2093872")
            min_value: Minimum activity value in nM (filter)
            
        Returns:
            DataFrame with columns: molecule_chembl_id, smiles, activity_type, 
                                   activity_value, activity_unit, assay_id, pchembl_value
        """
        min_val = min_value or self.config.min_activity_value
        
        records = []
        params = {
            "target_chembl_id": target_chembl_id,
            "assay_type": "|".join(self.config.assay_types),
            "min_value": str(min_val),
            "relation": "<",
            "incl": "molecule_chembl_id,canonical_smiles,activity_type,activity_value,activity_unit,assay_chembl_id,pchembl_value",
        }
        
        for activity in self._paginate("activity.json", params):
            record = {
                "molecule_chembl_id": activity.get("molecule_chembl_id"),
                "smiles": activity.get("canonical_smiles"),
                "activity_type": activity.get("activity_type"),
                "activity_value": self._parse_float(activity.get("activity_value")),
                "activity_unit": activity.get("activity_unit"),
                "assay_chembl_id": activity.get("assay_chembl_id"),
                "pchembl_value": self._parse_float(activity.get("pchembl_value")),
                "target_chembl_id": target_chembl_id,
            }
            records.append(record)
        
        df = pd.DataFrame(records)
        
        # Filter valid records
        if not df.empty:
            df = df.dropna(subset=["molecule_chembl_id", "pchembl_value"])
            df = df[df["pchembl_value"] > 0]
        
        return df
    
    def fetch_target_by_gene(self, gene_name: str) -> List[Dict]:
        """Fetch targets by gene name"""
        data = self._get("target.json", {
            "target_name__icontains": gene_name,
            "target_type": "|".join(self.config.target_types),
        })
        return data.get("targets", [])
    
    def fetch_drugs_by_indication(self, disease: str) -> pd.DataFrame:
        """
        Fetch drugs for a specific disease indication.
        
        Args:
            disease: Disease name (e.g., "MASH", "NAFLD", "sarcopenia")
            
        Returns:
            DataFrame with drug information
        """
        records = []
        
        for indication in self._paginate("indicator.json", {
            "disease__icontains": disease,
            "max_phase": "4",  # Only approved drugs
        }):
            record = {
                "molecule_chembl_id": indication.get("molecule_chembl_id"),
                "drug_name": indication.get("drug_name"),
                "indication": indication.get("disease"),
                "max_phase": indication.get("max_phase"),
                "mechanism_of_action": indication.get("mechanism_of_action"),
                "target_chembl_id": indication.get("target_chembl_id"),
            }
            records.append(record)
        
        return pd.DataFrame(records)
    
    def fetch_mechanisms(self, molecule_chembl_id: str) -> List[Dict]:
        """Fetch mechanism of action for a molecule"""
        data = self._get(f"molecule/{molecule_chembl_id}/mechanism.json")
        return data.get("mechanisms", [])
    
    def fetch_protein_classification(self, target_chembl_id: str) -> Dict:
        """Fetch protein classification for a target"""
        data = self._get(f"target/{target_chembl_id}/protein_classification.json")
        return data
    
    @staticmethod
    def _parse_float(value: Optional[str]) -> Optional[float]:
        """Parse float value safely"""
        if value is None:
            return None
        try:
            return float(value)
        except (ValueError, TypeError):
            return None
    
    def ingest(
        self,
        version: str = "34",
        output: str = "data/chembl_activities.parquet",
        target_genes: Optional[List[str]] = None,
    ) -> bool:
        """
        Run full ingestion of ChEMBL data.
        
        Args:
            version: ChEMBL version
            output: Output parquet file path
            target_genes: List of gene names to fetch (optional)
            
        Returns:
            True if successful
        """
        print(f"\n{'='*60}")
        print(f"ChEMBL Data Ingestion (v{version})")
        print(f"{'='*60}")
        
        # Default target genes if not specified
        if target_genes is None:
            target_genes = ["THRB", "NR1H4", "PPARA", "GLP1R", "SLC5A2"]
        
        all_activities = []
        
        for gene in target_genes:
            print(f"\n📥 Fetching data for {gene}...")
            
            # Find target
            targets = self.fetch_target_by_gene(gene)
            if not targets:
                print(f"   ⚠️ No target found for {gene}")
                continue
            
            # Get first protein target
            target = next(
                (t for t in targets if t.get("target_type") in self.config.target_types),
                None
            )
            if not target:
                print(f"   ⚠️ No suitable target found for {gene}")
                continue
            
            target_id = target.get("target_chembl_id")
            print(f"   Target: {target_id}")
            
            # Fetch activities
            df = self.fetch_activities_by_target(target_id)
            if not df.empty:
                print(f"   ✅ Fetched {len(df)} activities")
                all_activities.append(df)
            else:
                print(f"   ⚠️ No activities found")
        
        if all_activities:
            # Combine all activities
            combined = pd.concat(all_activities, ignore_index=True)
            
            # Add metadata
            combined.attrs["data_source"] = "ChEMBL"
            combined.attrs["version"] = version
            combined.attrs["access_date"] = datetime.now().isoformat()
            combined.attrs["license"] = "CC BY-SA 3.0"
            
            # Ensure output directory exists
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            
            # Save
            combined.to_parquet(output, index=False)
            
            print(f"\n✅ Ingestion complete: {len(combined)} records")
            print(f"   Output: {output}")
            
            # Print summary
            print(f"\n📊 Summary:")
            print(f"   Targets: {len(target_genes)}")
            print(f"   Total activities: {len(combined)}")
            print(f"   Unique molecules: {combined['molecule_chembl_id'].nunique()}")
            
            return True
        else:
            print(f"\n❌ No data fetched")
            return False


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest ChEMBL data")
    parser.add_argument("--version", default="34", help="ChEMBL version")
    parser.add_argument("--output", default="data/chembl_activities.parquet", help="Output file")
    parser.add_argument("--targets", nargs="+", help="Target gene names")
    
    args = parser.parse_args()
    
    client = ChEMBLClient()
    client.ingest(
        version=args.version,
        output=args.output,
        target_genes=args.targets,
    )
