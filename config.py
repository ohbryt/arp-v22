"""
ARP v22 - Configuration File

This file defines all configurable parameters for the pipeline.
Override values using environment variables or by creating a config_local.py.
"""

from pathlib import Path

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"
SCHEMAS_DIR = PROJECT_ROOT / "schemas"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)


# ============================================================================
# DATA SOURCES
# ============================================================================

DATA_SOURCES = {
    "chembl": {
        "version": "34",
        "base_url": "https://www.ebi.ac.uk/chembl/api",
        "min_activity_nM": 10000,
        "license": "CC BY-SA 3.0",
    },
    "pubchem": {
        "base_url": "https://pubchem.ncbi.nlm.nih.gov/rest/pug",
        "max_compounds": 1000000,
        "license": "Public Domain",
    },
    "uniprot": {
        "base_url": "https://rest.uniprot.org",
        "taxonomy": "Homo sapiens",
        "license": "CC BY 4.0",
    },
    "alphafold": {
        "base_url": "https://alphafold.ebi.ac.uk",
        "license": "CC BY 4.0",
    },
    "pdb": {
        "base_url": "https://files.rcsb.org",
        "license": "CC0 1.0",
    },
    "open_targets": {
        "base_url": "https://api.platform.opentargets.org",
        "license": "CC0 1.0",
    },
}


# ============================================================================
# SCREENING PARAMETERS
# ============================================================================

SCREENING = {
    "method": "qsar+docking",  # "qsar", "docking", "consensus"
    "qsar": {
        "model_path": str(MODELS_DIR / "qsar_model.pt"),
        "confidence_threshold": 0.7,
        "use_rdkit_fallback": True,
    },
    "docking": {
        "vina_path": "vina",
        "exhaustiveness": 8,
        "num_poses": 10,
        "energy_range": 3.0,
    },
    "max_hits": 1000,
}


# ============================================================================
# ADMET PARAMETERS
# ============================================================================

ADMET_THRESHOLDS = {
    "logp": {"min": -2, "max": 5, "unit": "log units"},
    "tpsa": {"min": 40, "max": 140, "unit": "A^2"},
    "molecular_weight": {"min": 100, "max": 500, "unit": "Da"},
    "hbd": {"max": 5, "unit": "count"},
    "hba": {"max": 10, "unit": "count"},
    "rotatable_bonds": {"max": 10, "unit": "count"},
    "aromatic_rings": {"max": 5, "unit": "count"},
    "fraction_csp3": {"min": 0.25, "unit": "ratio"},
}

# PAINS filter patterns (RDKit format)
PAINS_FILTERS = {
    "pains_a": r"(?i)\[.*\:(?:\w{1,3}\?)+\].*\#.*\=",
    "pains_b": r"c1ccnc1\C=C/c.*c.*\n",
    # ... full PAINS patterns would be much longer
}


# ============================================================================
# DISEASE-SPECIFIC PARAMETERS
# ============================================================================

DISEASE_PARAMS = {
    "masld": {
        "name": "Metabolic dysfunction-associated steatotic liver disease",
        "targets": ["THRB", "NR1H4", "PPARA", "GLP1R", "SLC5A2", "NLRP3", "ACACA"],
        "primary_axis": "fibrosis",
        "weight_matrix": {
            "genetic_causality": 0.05,
            "disease_context": 0.25,
            "perturbation_rescue": 0.15,
            "tissue_specificity": 0.20,
            "druggability": 0.10,
            "safety": 0.20,
            "translation": 0.05,
            "competitive_novelty": 0.00,
        },
    },
    "sarcopenia": {
        "name": "Age-related sarcopenia",
        "targets": ["MTOR", "FOXO1", "FOXO3", "MSTN", "AMPK", "PGC1A", "SIRT1"],
        "primary_axis": "muscle_function",
        "weight_matrix": {
            "genetic_causality": 0.05,
            "disease_context": 0.15,
            "perturbation_rescue": 0.25,
            "tissue_specificity": 0.20,
            "druggability": 0.10,
            "safety": 0.20,
            "translation": 0.05,
            "competitive_novelty": 0.00,
        },
    },
}


# ============================================================================
# PIPELINE PARAMETERS
# ============================================================================

PIPELINE = {
    "max_compounds_per_screen": 100000,
    "batch_size": 1000,
    "cache_dir": str(DATA_DIR / "cache"),
    "temp_dir": "/tmp/arp_v22",
    "gpu_required": False,
    "min_disk_space_gb": 50,
}


# ============================================================================
# MANIFEST PARAMETERS
# ============================================================================

MANIFEST = {
    "required_fields": [
        "run_id",
        "git_commit",
        "python_version",
        "environment_hash",
        "data_snapshots",
        "models",
        "params",
    ],
    "determinism_levels": ["full", "partial", "non_deterministic"],
}


# ============================================================================
# API KEYS (from environment)
# ============================================================================

import os

API_KEYS = {
    "ncbi_api_key": os.environ.get("NCBI_API_KEY", ""),
    "scopus_api_key": os.environ.get("SCOPUS_API_KEY", ""),
    "brave_api_key": os.environ.get("BRAVE_API_KEY", ""),
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_disease_params(disease: str) -> dict:
    """Get parameters for a specific disease"""
    return DISEASE_PARAMS.get(disease.lower(), {})


def get_data_source(source: str) -> dict:
    """Get configuration for a data source"""
    return DATA_SOURCES.get(source.lower(), {})


def validate_config() -> bool:
    """Validate configuration"""
    errors = []
    
    # Check directories exist
    for d in [DATA_DIR, MODELS_DIR, RESULTS_DIR]:
        if not d.exists():
            errors.append(f"Directory not found: {d}")
    
    # Check API keys
    if not API_KEYS["ncbi_api_key"]:
        errors.append("NCBI API key not set (NCBI_API_KEY)")
    
    return len(errors) == 0, errors
