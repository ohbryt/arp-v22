"""
Lung Fibrosis Disease Pack

Idiopathic Pulmonary Fibrosis (IPF) and related fibrotic lung diseases.
Primary pathology: fibroblast activation, ECM deposition, epithelial dysfunction.
"""

from .ontology import LungFibrosisOntology, get_lung_fibrosis_ontology
from .targets import LungFibrosisTargets, LUNG_FIBROSIS_TARGETS

__all__ = [
    "LungFibrosisOntology",
    "get_lung_fibrosis_ontology",
    "LungFibrosisTargets",
    "LUNG_FIBROSIS_TARGETS",
]
