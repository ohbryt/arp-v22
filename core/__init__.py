"""
ARP v22 - Core Module

3-Engine Architecture:
- Engine 1: Disease → Target (target prioritization)
- Engine 2: Target → Modality (modality routing)
- Engine 3: Modality → Candidate (candidate generation)
"""

__version__ = "22.0.1"

from .scoring_engine import TargetScorer, DiseaseEngine
from .weights import DISEASE_WEIGHTS, MODALITY_PREFERENCES
from .schema import (
    TargetDossier,
    TargetScores,
    DiseaseContextData,
    Penalty,
)

__all__ = [
    "TargetScorer",
    "DiseaseEngine",
    "DISEASE_WEIGHTS",
    "MODALITY_PREFERENCES",
    "TargetDossier",
    "TargetScores",
    "DiseaseContextData",
    "Penalty",
]
