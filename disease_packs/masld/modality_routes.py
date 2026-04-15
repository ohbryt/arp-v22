"""
MASLD Modality Routing

Target class to modality mapping for MASLD drug discovery.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class Modality(Enum):
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    OLIGO = "oligo"
    LIVER_TARGETED_OLIGO = "liver_targeted_oligo"
    ANTIBODY = "antibody"


@dataclass
class ModalityRecommendation:
    """Modality recommendation for a target class"""
    modality: Modality
    preference_score: float  # 0-1
    rationale: str
    key_advantages: List[str]
    key_risks: List[str]
    development_timeline_years: float
    estimated_development_cost: str  # relative


# ============================================================================
# TARGET CLASS TO MODALITY MAPPING
# ============================================================================

TARGET_CLASS_MODALITIES: Dict[str, List[ModalityRecommendation]] = {
    "nuclear_receptor": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.95,
            rationale="Nuclear receptors have well-defined ligand-binding pockets; oral bioavailability achievable",
            key_advantages=["Oral administration", "Well-established SAR", "Patent landscape clear"],
            key_risks=["Off-target nuclear receptor activation", "Long half-life considerations"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.PEPTIDE,
            preference_score=0.25,
            rationale="Peptides generally not suitable for intracellular nuclear receptors",
            key_advantages=["High specificity"],
            key_risks=["Poor cell penetration", "Stability issues"],
            development_timeline_years=7.0,
            estimated_development_cost="high",
        ),
    ],
    
    "gpc_receptor": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.85,
            rationale="GLP1R and similar GPCRs have proven small molecule tractability",
            key_advantages=["Oral options emerging (orals)", "Injectable well-established"],
            key_risks=["Receptor selectivity", "Cardiovascular safety"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.PEPTIDE,
            preference_score=0.90,
            rationale="GLP1R agonists are peptide-based (semaglutide, liraglutide)",
            key_advantages=["High potency", "Proven efficacy", "Good safety profile"],
            key_risks=["Injection burden", "GI side effects"],
            development_timeline_years=5.0,
            estimated_development_cost="high",
        ),
    ],
    
    "transporter": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.95,
            rationale="SGLT2 inhibitors are proven small molecule drugs",
            key_advantages=["Oral administration", "Once-daily dosing", "Patent expired/protected"],
            key_risks=["Euglycemia risk", "Genital infections", "Renal function"],
            development_timeline_years=4.0,
            estimated_development_cost="low",
        ),
    ],
    
    "enzyme": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.90,
            rationale="Enzymes typically have well-defined active sites for small molecules",
            key_advantages=["Potent inhibition achievable", "Clear SAR", "Oral options possible"],
            key_risks=["Selectivity challenges", "Metabolic stability"],
            development_timeline_years=5.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.LIVER_TARGETED_OLIGO,
            preference_score=0.70,
            rationale="ASO/siRNA can target hepatocyte-expressed enzymes with GalNAc",
            key_advantages=["High specificity", "Liver-targeted delivery", "Long duration"],
            key_risks=["Hepatotoxicity risk", "Chronic dosing safety", "Manufacturing cost"],
            development_timeline_years=6.0,
            estimated_development_cost="high",
        ),
    ],
    
    "transcription_factor": [
        ModalityRecommendation(
            modality=Modality.LIVER_TARGETED_OLIGO,
            preference_score=0.75,
            rationale="Transcription factors require nucleic acid-based modulation (ASO/siRNA)",
            key_advantages=["High specificity for undruggable targets", "GalNAc liver targeting"],
            key_risks=["Delivery challenge", "Patent landscape unclear", "Safety monitoring"],
            development_timeline_years=7.0,
            estimated_development_cost="high",
        ),
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.40,
            rationale="Indirect modulation possible but less specific",
            key_advantages=["Oral option", "Established chemistry"],
            key_risks=["Indirect mechanism", "Off-target effects"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.BIOLOGIC,
            preference_score=0.30,
            rationale="Biologics typically cannot penetrate cells for TF targets",
            key_advantages=["High specificity"],
            key_risks=["Cannot intracellular targets", "Cell penetration"],
            development_timeline_years=7.0,
            estimated_development_cost="very_high",
        ),
    ],
    
    "inflammasome": [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.80,
            rationale="NLRP3 inhibitors have shown promise; oral options available",
            key_advantages=["Oral administration", "Anti-inflammatory", "Established safety"],
            key_risks=["Immune suppression", "Infection risk"],
            development_timeline_years=6.0,
            estimated_development_cost="moderate",
        ),
        ModalityRecommendation(
            modality=Modality.LIVER_TARGETED_OLIGO,
            preference_score=0.65,
            rationale="ASO can target NLRP3 expression in hepatocytes/Kupffer cells",
            key_advantages=["Specific knockdown", "GalNAc delivery"],
            key_risks=["Hepatotoxicity", "Delivery to immune cells"],
            development_timeline_years=6.0,
            estimated_development_cost="high",
        ),
    ],
}


# ============================================================================
# DISEASE-SPECIFIC MODALITY PREFERENCES
# ============================================================================

DISEASE_MODALITY_PREFERENCES: Dict[str, float] = {
    "small_molecule": 0.90,
    "liver_targeted_oligo": 0.80,
    "peptide": 0.60,
    "biologic": 0.50,
    "antibody": 0.45,
    "inhaled": 0.05,
}


# ============================================================================
# ROUTING DECISION FUNCTION
# ============================================================================

def get_modality_for_target(target_class: str) -> List[ModalityRecommendation]:
    """Get recommended modalities for a target class in MASLD"""
    return TARGET_CLASS_MODALITIES.get(target_class, [
        ModalityRecommendation(
            modality=Modality.SMALL_MOLECULE,
            preference_score=0.70,
            rationale="Default for most targets",
            key_advantages=["Oral option", "Established development path"],
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


def get_modality_compatibility_score(target_class: str, modality: str) -> float:
    """Get compatibility score between target class and modality"""
    recommendations = get_modality_for_target(target_class)
    for rec in recommendations:
        if rec.modality.value == modality:
            return rec.preference_score
    return 0.3  # Low default compatibility
