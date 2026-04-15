"""
MASLD Disease Pack

Metabolic dysfunction-associated steatotic liver disease (MASLD)
Formerly NAFLD - spectrum from steatosis to MASH to fibrosis to cirrhosis
"""

from .ontology import MASLDOntology, get_masld_ontology
from .targets import MASLDTargets, MASLD_TARGETS
from .modality_routes import ModalityRecommendation, get_modality_for_target

__all__ = [
    "MASLDOntology",
    "get_masld_ontology",
    "MASLDTargets",
    "MASLD_TARGETS",
    "ModalityRecommendation",
    "get_modality_for_target",
]
