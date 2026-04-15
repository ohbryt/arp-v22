"""
ARP v22 - UniProt Data Ingestion

UniProt is a comprehensive protein database.
License: CC BY 4.0

API Documentation: https://rest.uniprot.org/
"""

import httpx
import time
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd


class UniProtClient:
    """
    Client for UniProt REST API.
    
    Usage:
        client = UniProtClient()
        df = client.fetch_proteins_by_genes(["THRB", "NR1H4"])
        df = client.fetch_protein_by_uniprot_id("P10828")
    """
    
    BASE_URL = "https://rest.uniprot.org"
    
    def __init__(self):
        self.session = httpx.Client(timeout=60.0)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """Make GET request to UniProt API"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def fetch_protein_by_uniprot_id(self, uniprot_id: str) -> Dict:
        """Fetch protein details by UniProt ID"""
        # Get basic info
        data = self._get(f"uniprotkb/{uniprot_id}.json")
        
        # Parse relevant fields
        protein = data.get("primaryAccession", uniprot_id)
        gene_name = ""
        
        genes = data.get("genes", [])
        if genes:
            gene_name = genes[0].get("geneName", {}).get("value", "")
        
        # Get recommended name
        protein_name = ""
        names = data.get("proteinDescription", {})
        rec = names.get("recommendedName", {})
        if rec:
            full_name = rec.get("fullName", {})
            protein_name = full_name.get("value", "")
        
        # Get organism
        organism = ""
        org_data = data.get("organism", {})
        organism = org_data.get("scientificName", "")
        
        # Get gene ontology
        go_terms = []
        for go in data.get("goProcess", data.get("go", [])):
            go_terms.append({
                "id": go.get("id"),
                "term": go.get("name"),
                "category": go.get("ontology") if isinstance(go, dict) else "biological_process",
            })
        
        # Get sequences
        sequence = ""
        seq_data = data.get("sequence", {})
        sequence = seq_data.get("value", "")
        
        return {
            "uniprot_id": protein,
            "gene_name": gene_name,
            "protein_name": protein_name,
            "organism": organism,
            "sequence": sequence,
            "length": seq_data.get("length", 0),
            "mol_weight": seq_data.get("molWeight", 0),
            "go_terms": go_terms,
        }
    
    def fetch_proteins_by_genes(
        self,
        genes: List[str],
        organism: str = "Homo sapiens",
    ) -> pd.DataFrame:
        """
        Fetch proteins by gene names.
        
        Args:
            genes: List of gene names
            organism: Organism filter (default: Homo sapiens)
        """
        records = []
        
        for gene in genes:
            print(f"📥 Fetching {gene}...")
            
            try:
                # Search by gene name
                query = f"gene:{gene}+organism:{organism}"
                data = self._get("uniprotkb/search", {
                    "query": query,
                    "format": "json",
                    "fields": "accession,gene_names,protein_name,organism_name,length",
                    "size": 1,
                })
                
                results = data.get("results", [])
                if results:
                    result = results[0]
                    primary = result.get("primaryAccession", "")
                    
                    gene_data = result.get("genes", {})
                    gene_name = gene_data.get("geneName", {}).get("value", gene)
                    
                    protein_data = result.get("proteinDescription", {})
                    protein_name = ""
                    rec = protein_data.get("recommendedName", {})
                    if rec:
                        protein_name = rec.get("fullName", {})
                        if isinstance(protein_name, dict):
                            protein_name = protein_name.get("value", "")
                    
                    organism_name = result.get("organism", {}).get("scientificName", "")
                    
                    records.append({
                        "uniprot_id": primary,
                        "gene_name": gene_name,
                        "protein_name": protein_name,
                        "organism": organism_name,
                        "length": result.get("sequence", {}).get("length", 0),
                    })
                    
                    print(f"   ✅ Found: {primary}")
                else:
                    print(f"   ⚠️ Not found")
                
            except Exception as e:
                print(f"   ❌ Error: {e}")
            
            time.sleep(0.2)  # Rate limiting
        
        return pd.DataFrame(records)
    
    def fetch_proteins_by_pathway(
        self,
        pathway: str,
        organism: str = "Homo sapiens",
    ) -> pd.DataFrame:
        """Fetch all proteins in a pathway"""
        query = f"(go:{pathway})+AND+(organism:{organism})"
        
        all_results = []
        cursor = 0
        
        while True:
            data = self._get("uniprotkb/search", {
                "query": query,
                "format": "json",
                "fields": "accession,gene_names,protein_name,organism_name,length",
                "size": 500,
                "cursor": cursor,
            })
            
            results = data.get("results", [])
            if not results:
                break
            
            for result in results:
                primary = result.get("primaryAccession", "")
                gene_data = result.get("genes", {})
                gene_name = gene_data.get("geneName", {}).get("value", "")
                
                protein_data = result.get("proteinDescription", {})
                protein_name = ""
                rec = protein_data.get("recommendedName", {})
                if rec:
                    full_name = rec.get("fullName", {})
                    if isinstance(full_name, dict):
                        protein_name = full_name.get("value", "")
                
                organism_name = result.get("organism", {}).get("scientificName", "")
                
                all_results.append({
                    "uniprot_id": primary,
                    "gene_name": gene_name,
                    "protein_name": protein_name,
                    "organism": organism_name,
                    "length": result.get("sequence", {}).get("length", 0),
                })
            
            # Check for more results
            next_cursor = data.get("nextCursor")
            if not next_cursor or len(results) < 500:
                break
            cursor = next_cursor
        
        print(f"📥 Found {len(all_results)} proteins")
        return pd.DataFrame(all_results)
    
    def ingest(
        self,
        genes: Optional[List[str]] = None,
        output: str = "data/uniprot_proteins.parquet",
    ) -> bool:
        """
        Run UniProt ingestion.
        
        Args:
            genes: List of gene names (optional)
            output: Output parquet file path
            
        Returns:
            True if successful
        """
        print(f"\n{'='*60}")
        print("UniProt Data Ingestion")
        print(f"{'='*60}")
        
        if genes is None:
            genes = ["THRB", "NR1H4", "PPARA", "GLP1R", "SLC5A2"]
        
        df = self.fetch_proteins_by_genes(genes)
        
        if not df.empty:
            # Add metadata
            df.attrs["data_source"] = "UniProt"
            df.attrs["access_date"] = time.strftime("%Y-%m-%d")
            df.attrs["license"] = "CC BY 4.0"
            
            Path(output).parent.mkdir(parents=True, exist_ok=True)
            df.to_parquet(output, index=False)
            
            print(f"\n✅ Ingestion complete: {len(df)} proteins")
            print(f"   Output: {output}")
            return True
        
        print("\n❌ No data fetched")
        return False
