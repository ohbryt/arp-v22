"""
Heart Failure Disease Pack

Heart Failure with reduced ejection fraction (HFrEF) and preserved (HFpEF).
Primary pathology: remodeling, fibrosis, contractility dysfunction.
"""

from .ontology import HeartFailureOntology, get_heart_failure_ontology
from .targets import HeartFailureTargets, HEART_FAILURE_TARGETS

__all__ = [
    "HeartFailureOntology",
    "get_heart_failure_ontology",
    "HeartFailureTargets",
    "HEART_FAILURE_TARGETS",
]
