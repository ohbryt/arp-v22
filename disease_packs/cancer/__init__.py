"""
Cancer Disease Pack

Cancer target discovery with focus on biomarker-defined subtypes.
Index indication: NSCLC EGFR-mutant.

Key principles:
- Subtype-specific dependency
- Biomarker-driven patient selection
- Therapeutic window vs normal tissue
"""

from .ontology import CancerOntology, get_cancer_ontology
from .targets import CancerTargets, CANCER_TARGETS

__all__ = [
    "CancerOntology",
    "get_cancer_ontology",
    "CancerTargets",
    "CANCER_TARGETS",
]
