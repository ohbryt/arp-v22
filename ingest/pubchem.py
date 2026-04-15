"""
ARP v22 - PubChem Data Ingestion

PubChem is a public database of chemical molecules.
License: Public domain (US government works)

API Documentation: https://pubchem.ncbi.nlm.nih.gov/pug-rest/
"""

import httpx
import time
from typing import Dict, List, Optional
from pathlib import Path
import pandas as pd


class PubChemClient:
    """
    Client for PubChem PUG REST API.
    
    Usage:
        client = PubChemClient()
        df = client.fetch_by_cid([12345, 67890])
        df = client.fetch_by_inchikey("XXXXXXXXXXXXXX")
    """
    
    BASE_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
    
    def __init__(self):
        self.session = httpx.Client(timeout=120.0)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """Make GET request to PubChem API"""
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def fetch_by_cid(self, cids: List[int]) -> pd.DataFrame:
        """Fetch compound properties by CID"""
        cid_str = ",".join(str(c) for c in cids)
        
        # Get properties
        props = self._get(
            "compound/cid/{}/property/MolecularFormula,MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,TPSA,RotatableBondCount,Complexity,Charge/JSON".format(cid_str),
        )
        
        table = props.get("PropertyTable", {}).get("Properties", [])
        
        df = pd.DataFrame(table)
        df = df.rename(columns={
            "CID": "pubchem_cid",
            "MolecularFormula": "molecular_formula",
            "MolecularWeight": "molecular_weight",
            "XLogP": "logp",
            "HBondDonorCount": "hbd",
            "HBondAcceptorCount": "hba",
            "TPSA": "tpsa",
            "RotatableBondCount": "rotatable_bonds",
            "Complexity": "complexity",
            "Charge": "charge",
        })
        
        return df
    
    def fetch_by_inchikey(self, inchikey: str) -> pd.DataFrame:
        """Fetch compound by InChIKey"""
        data = self._get(f"compound/inchikey/{inchikey}/property/MolecularFormula,MolecularWeight,CanonicalSMILES/JSON")
        
        props = data.get("PropertyTable", {}).get("Properties", [{}])[0]
        if not props:
            return pd.DataFrame()
        
        return pd.DataFrame([{
            "inchi_key": inchikey,
            "pubchem_cid": props.get("CID"),
            "molecular_formula": props.get("MolecularFormula"),
            "molecular_weight": props.get("MolecularWeight"),
            "canonical_smiles": props.get("CanonicalSMILES"),
        }])
    
    def fetch_synonyms(self, cid: int) -> List[str]:
        """Fetch all synonyms for a compound"""
        try:
            data = self._get(f"compound/cid/{cid}/synonyms/JSON")
            return data.get("InformationList", {}).get("Information", [{}])[0].get("Synonym", [])
        except:
            return []
    
    def search_by_name(self, name: str, max_results: int = 10) -> List[Dict]:
        """Search compounds by name"""
        data = self._get(f"compound/name/{name}/property/MolecularWeight,XLogP/JSON")
        
        results = []
        for prop in data.get("PropertyTable", {}).get("Properties", []):
            results.append({
                "name": name,
                "cid": prop.get("CID"),
                "mw": prop.get("MolecularWeight"),
                "logp": prop.get("XLogP"),
            })
        
        return results[:max_results]
    
    def get_cid_from_smiles(self, smiles: str) -> Optional[int]:
        """Get CID from SMILES"""
        try:
            data = self._get(f"compound/smiles/{smiles}/cids/JSON")
            cids = data.get("IdentifierList", {}).get("CID", [])
            return cids[0] if cids else None
        except:
            return None
    
    def ingest(
        self,
        compounds: Optional[List[str]] = None,
        output: str = "data/pubchem_compounds.parquet",
    ) -> bool:
        """
        Run PubChem ingestion.
        
        Args:
            compounds: List of InChIKeys or names (optional)
            output: Output parquet file path
            
        Returns:
            True if successful
        """
        print(f"\n{'='*60}")
        print("PubChem Data Ingestion")
        print(f"{'='*60}")
        
        if compounds:
            print(f"\n📥 Fetching {len(compounds)} compounds...")
            all_data = []
            
            for i, compound in enumerate(compounds):
                if i % 100 == 0:
                    print(f"   Progress: {i}/{len(compounds)}")
                
                try:
                    if "-" in compound and len(compound) == 27:
                        df = self.fetch_by_inchikey(compound)
                    else:
                        results = self.search_by_name(compound)
                        if results:
                            cid = results[0].get("cid")
                            if cid:
                                df = self.fetch_by_cid([cid])
                    
                    if not df.empty:
                        all_data.append(df)
                except Exception as e:
                    print(f"   Error fetching {compound}: {e}")
                
                time.sleep(0.1)  # Rate limiting
            
            if all_data:
                combined = pd.concat(all_data, ignore_index=True)
                
                # Add metadata
                combined.attrs["data_source"] = "PubChem"
                combined.attrs["access_date"] = time.strftime("%Y-%m-%d")
                
                Path(output).parent.mkdir(parents=True, exist_ok=True)
                combined.to_parquet(output, index=False)
                
                print(f"\n✅ Ingestion complete: {len(combined)} compounds")
                print(f"   Output: {output}")
                return True
        
        print("\n⚠️ No compounds specified")
        return False
