"""
Sarcopenia Disease Pack

Age-related skeletal muscle loss with functional decline.
Primary: anabolic resistance, mitochondrial dysfunction.
Secondary: disuse, cachexia, disease-related.
"""

from .ontology import SarcopeniaOntology, get_sarcopenia_ontology
from .targets import SarcopeniaTargets, SARCOPENIA_TARGETS
from .modality_routes import ModalityRecommendation, get_modality_for_target

__all__ = [
    "SarcopeniaOntology",
    "get_sarcopenia_ontology",
    "SarcopeniaTargets",
    "SARCOPENIA_TARGETS",
    "ModalityRecommendation",
    "get_modality_for_target",
]
