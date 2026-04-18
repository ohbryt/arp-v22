"""
Cardiac Fibrosis Disease Pack for ARP v22

Disease: Cardiac Fibrosis (CF)
Pathophysiology: Excessive extracellular matrix deposition in the heart leading to stiffness and dysfunction
Target Prioritization: IL-11 > LOXL2 > YAP/TAZ > FAP > NPRC
Modality Routing: Small molecules, biologics, natural compounds
"""

from .ontology import CARDIAC_FIBROSIS_ONTOLOGY
from .targets import CARDIAC_FIBROSIS_TARGETS
from .modality_routes import CARDIAC_FIBROSIS_MODALITY_ROUTES

__all__ = [
    'CARDIAC_FIBROSIS_ONTOLOGY',
    'CARDIAC_FIBROSIS_TARGETS',
    'CARDIAC_FIBROSIS_MODALITY_ROUTES'
]