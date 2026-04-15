"""
ARP v22 - Data Ingest Module

Provides standardized data ingestion from public databases:
- ChEMBL (bioactivity, drug targets)
- PubChem (chemical structures)
- UniProt (protein sequences)
- Ensembl (gene annotations)
"""

__version__ = "1.0.0"

__all__ = [
    "ChEMBLClient",
    "PubChemClient",
    "UniProtClient",
    "IngestConfig",
    "run_ingest",
]

from .chembl import ChEMBLClient, ChEMBLConfig
from .pubchem import PubChemClient
from .uniprot import UniProtClient
from .config import IngestConfig


def run_ingest(source: str, **kwargs) -> bool:
    """Run ingestion for a specific data source"""
    if source.lower() == "chembl":
        client = ChEMBLClient()
        return client.ingest(**kwargs)
    elif source.lower() == "pubchem":
        client = PubChemClient()
        return client.ingest(**kwargs)
    elif source.lower() == "uniprot":
        client = UniProtClient()
        return client.ingest(**kwargs)
    else:
        raise ValueError(f"Unknown source: {source}")
