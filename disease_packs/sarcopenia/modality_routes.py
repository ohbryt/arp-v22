"""
Sarcopenia Modality Routing

Target class to modality mapping for Sarcopenia drug discovery.
"""

from dataclasses import dataclass
from typing import Dict, List
from enum import Enum


class Modality(Enum):
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    OLIGO = "oligo"
    ANTIBODY = "antibody"
    LIGAND_TRAP = "ligand_trap"


@dataclass
class ModalityRecommendation:
    """Modality recommendation for a target class"""
    modality: Modality
    preference_score: float  # 0-1
    rationale: str
    key_advantages: List[str]
    key_risks: List[str]
    development_timeline_years: float
    estimated_development_cost: str


# ============================================================================
# TARGET CLASS TO MODALITY MAPPING
# ============================================================================

TARGET_CLASS_MODALITIES: Dict[str, List[ModalityRecommendation]] = {
    "kinase": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.85,
            rationale="Kinases have well-defined ATP-binding pockets; oral inhibitors achievable",
            key_advantages=["Oral administration possible", "Established development path", "Good PK"],
            key_risks=["Off-target kinase inhibition", "Resistance development"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.BIOLOGIC,
            preference_score=0.45,
            rationale="Kinase inhibitors typically small molecules; biologics for extracellular kinases",
            key_advantages=["High specificity (antibodies)"],
            key_risks=["Intracellular targets not accessible"],
            development_timeline_years=6.0,
            estimated_development_cost="high",
        ),
    ],
    
    "transcription_factor": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.40,
            rationale="Transcription factors are intracellular and difficult to drug directly",
            key_advantages=["Oral administration"],
            key_risks=["Indirect mechanism", "Low specificity"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.OLIGO,
            preference_score=0.70,
            rationale="ASO/siRNA can target transcription factor expression",
            key_advantages=["High specificity", "Direct targeting of 'undruggable' targets"],
            key_risks=["Delivery to muscle", "Stability concerns", "Manufacturing cost"],
            development_timeline_years=7.0,
            estimated_development_cost="high",
        ),
    ],
    
    "extracellular_ligand": [
        ModalityRecommendation(
            modality=Modality.BIOLOGIC,
            preference_score=0.92,
            rationale="Extracellular ligands (myostatin, activin) are ideal biologic targets",
            key_advantages=["High specificity", "Proven clinical success (bimagrumab)", "Good safety"],
            key_risks=["Injection burden", "High cost", "Chronic administration needed"],
            development_timeline_years=5.0,
            estimated_development_cost="high",
        ),
        ModalityRecommendation(
            modality=Modality.PEPTIDE,
            preference_score=0.75,
            rationale="Peptides can mimic or block extracellular ligands",
            key_advantages=["Higher specificity than small molecules", "Better cell penetration than antibodies"],
            key_risks=["Stability issues", "Delivery challenges"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.ANTIBODY,
            preference_score=0.90,
            rationale="Myostatin/activin pathway already validated with antibodies",
            key_advantages=["Proven mechanism", "Long half-life", "High specificity"],
            key_risks=["Injection site reactions", "Immunogenicity"],
            development_timeline_years=5.0,
            estimated_development_cost="high",
        ),
    ],
    
    "receptor": [
        ModalityRecommendation(
            modality=Modality.BIOLOGIC,
            preference_score=0.80,
            rationale="Receptors (especially GPCRs) can be targeted with biologics/peptides",
            key_advantages=["Targeted delivery possible", "High specificity"],
            key_risks=["Receptor occupancy requirements", "Chronic dosing"],
            development_timeline_years=5.0,
            estimated_development_cost="high",
        ),
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.75,
            rationale="GPCRs have proven small molecule tractability (e.g., GLP1R)",
            key_advantages=["Oral options emerging", "Well-established SAR"],
            key_risks=["Selectivity challenges", "Off-target effects"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
    ],
    
    "enzyme": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.80,
            rationale="Enzymes typically have well-defined active sites",
            key_advantages=["Potent inhibition", "Oral options", "Clear SAR"],
            key_risks=["Selectivity", "Metabolic stability"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.PEPTIDE,
            preference_score=0.55,
            rationale="Some enzymes can be targeted with peptide inhibitors",
            key_advantages=["High specificity", "Modulate protein-protein interactions"],
            key_risks=["Stability", "Delivery"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
    ],
    
    "myostatin_axis": [
        ModalityRecommendation(
            modality=Modality.ANTIBODY,
            preference_score=0.95,
            rationale="Myostatin pathway validated with antibodies in clinical trials",
            key_advantages=["Muscle-selective", "Proven mechanism", "Good safety profile"],
            key_risks=["Injection burden", "Cost"],
            development_timeline_years=4.0,
            estimated_development_cost="high",
        ),
        ModalityRecommendation(
            modality=Modality.LIGAND_TRAP,
            preference_score=0.88,
            rationale="Soluble receptor traps (e.g., ACVR2B-Fc) block myostatin/activin",
            key_advantages=["Bimolecular mechanism", "Dual targeting possible"],
            key_risks=["Immunogenicity", "Long-term safety"],
            development_timeline_years=5.0,
            estimated_development_cost="very_high",
        ),
        ModalityRecommendation(
            modality=Modality.PEPTIDE,
            preference_score=0.65,
            rationale="Peptide myostatin inhibitors under development",
            key_advantages=["Oral potential", "Lower cost"],
            key_risks=["Stability", "Potency"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
    ],
}


# ============================================================================
# SARCOPENIA-SPECIFIC MODALITY PREFERENCES
# ============================================================================

DISEASE_MODALITY_PREFERENCES: Dict[str, float] = {
    "biologic": 0.85,
    "peptide": 0.80,
    "small_molecule": 0.70,
    "oligo": 0.50,
    "antibody": 0.82,
    "inhaled": 0.10,
}


# ============================================================================
# FUNCTIONAL ENDPOINT TO MODALITY MAPPING
# ============================================================================

FUNCTIONAL_ENDPOINT_MODALITY: Dict[str, List[str]] = {
    "muscle_mass_DXA": [
        "biologic",
        "antibody",
        "peptide",
    ],
    "grip_strength": [
        "small_molecule",
        "biologic",
        "peptide",
    ],
    "exercise_endurance": [
        "small_molecule",
        "biologic",
    ],
    "muscle_regeneration": [
        "biologic",
        "peptide",
        "cell_therapy",
    ],
}


# ============================================================================
# ROUTING DECISION FUNCTIONS
# ============================================================================

def get_modality_for_target(target_class: str) -> List[ModalityRecommendation]:
    """Get recommended modalities for a target class in Sarcopenia"""
    return TARGET_CLASS_MODALITIES.get(target_class, [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.70,
            rationale="Default for most targets",
            key_advantages=["Oral option", "Established path"],
            key_risks=["Off-target risk"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
    ])


def get_preferred_modality(target_class: str) -> Modality:
    """Get the preferred modality for a target class"""
    recommendations = get_modality_for_target(target_class)
    if recommendations:
        return recommendations[0].modality
    return Modality.SMALL_MOLECULE


def get_modality_for_functional_endpoint(endpoint: str) -> List[str]:
    """Get preferred modalities for a functional endpoint"""
    return FUNCTIONAL_ENDPOINT_MODALITY.get(endpoint, ["small_molecule", "biologic"])


def recommend_modality_for_sarcopenia(
    target_class: str,
    functional_endpoint: str,
    safety_priority: bool = True,
) -> List[str]:
    """
    Recommend modalities based on target class and functional endpoint.
    
    Args:
        target_class: The target class (kinase, extracellular_ligand, etc.)
        functional_endpoint: What functional improvement is desired
        safety_priority: If True, prioritize safer modalities
    
    Returns:
        List of recommended modalities in priority order
    """
    recommendations = get_modality_for_target(target_class)
    
    if not recommendations:
        return ["small_molecule"]
    
    # Sort by preference score
    sorted_recs = sorted(recommendations, key=lambda r: r.preference_score, reverse=True)
    
    if safety_priority:
        # Reorder to put biologics higher (better safety for chronic use)
        biologics_first = sorted(
            sorted_recs,
            key=lambda r: (
                r.modality in [Modality.BIOLOGIC, Modality.ANTIBODY],
                r.preference_score
            ),
            reverse=True
        )
        return [r.modality.value for r in biologics_first]
    
    return [r.modality.value for r in sorted_recs]
