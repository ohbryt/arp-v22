"""
ARP v22 - Ingest Configuration

Configuration for data ingestion.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class IngestConfig:
    """Configuration for data ingestion"""
    
    # ChEMBL settings
    chembl_version: str = "34"
    chembl_min_activity_nM: float = 10000.0
    chembl_max_results: int = 100000
    
    # PubChem settings
    pubchem_max_compounds: int = 1000000
    
    # UniProt settings
    uniprot_organism: str = "Homo sapiens"
    
    # Output settings
    output_dir: str = "data"
    cache_dir: str = "data/cache"
    
    # API settings
    rate_limit_delay: float = 0.5  # seconds between requests
    timeout: int = 60  # seconds
    
    # Quality settings
    min_compound_quality: str = "medium"
    
    @classmethod
    def from_dict(cls, config: Dict) -> "IngestConfig":
        """Create config from dictionary"""
        return cls(**{k: v for k, v in config.items() if k in cls.__annotations__})
