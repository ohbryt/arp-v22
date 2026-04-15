"""
Sarcopenia Ontology

Disease definitions, subtypes, stages, and biological axes for Sarcopenia.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class SarcopeniaStage(Enum):
    PRESARCOPENIA = "presarcopenia"       # Low muscle mass, normal strength
    SARCOPENIA = "sarcopenia"              # Low muscle mass + low strength or performance
    SEVERE_SARCOPENIA = "severe_sarcopenia"  # All three criteria


class SarcopeniaAxis(Enum):
    ANABOLISM = "anabolism"               # Muscle protein synthesis
    CATABOLISM = "catabolism"             # Muscle protein breakdown
    MITOCHONDRIAL = "mitochondrial"       # Energy metabolism
    NEUROMUSCULAR = "neuromuscular"       # Nerve-muscle connection
    INFLAMMATION = "inflammation"         # Chronic low-grade inflammation
    SATELLITE_CELL = "satellite_cell"     # Muscle stem cells


@dataclass
class SarcopeniaSubtype:
    """Sarcopenia subtype definition"""
    name: str
    code: str
    description: str
    prevalence_pct: float
    key_features: List[str]
    priority_targets: List[str]
    prognosis_notes: str


@dataclass
class SarcopeniaStageDefinition:
    """Sarcopenia stage definition"""
    stage: SarcopeniaStage
    description: str
    diagnostic_criteria: Dict[str, str]
    recommended_endpoints: List[str]
    typical_intervention: str


@dataclass
class SarcopeniaOntology:
    """Complete Sarcopenia ontology"""
    
    # Disease metadata
    disease_name: str = "Age-related Sarcopenia"
    icd10_code: str = "M62.84"
    
    # Subtypes
    subtypes: List[SarcopeniaSubtype] = field(default_factory=list)
    
    # Stages
    stages: List[SarcopeniaStageDefinition] = field(default_factory=list)
    
    # Key pathways
    pathways: Dict[str, List[str]] = field(default_factory=lambda: {
        "Anabolic Signaling": ["MTOR", "AKT1", "S6K1", "4E-BP1", "MYOD1"],
        "Catabolic Pathways": ["FOXO1", "FOXO3", "MAFbx", "MuRF1", "UPS"],
        "Mitochondrial Function": ["PGC1A", "SIRT1", "AMPK", "TFAM", "NRF1"],
        "Inflammation": ["NLRP3", "NFKB1", "TNF", "IL6", "CRP"],
        "Muscle Stem Cell": ["PAX7", "MYOD1", "MYOG", "CDK", "Cyclin"],
        "Neuromuscular": ["CHN", "RAPSN", "DOK7", "MUSK"],
    })
    
    # Key biomarkers
    biomarkers: Dict[str, List[str]] = field(default_factory=lambda: {
        "Muscle Mass": ["DXA (appendicular lean mass)", "BIA", "CT (muscle cross-sectional area)", "MRI"],
        "Muscle Strength": ["Grip strength", "Knee extension", "Peak expiratory flow"],
        "Physical Performance": ["SPPB", "Gait speed (6-min walk)", "Chair stand test", "Timed Up-and-Go"],
        "Metabolic": ["Insulin-like Growth Factor-1", "Testosterone", "Vitamin D", "Cystatin C"],
        "Inflammatory": ["IL-6", "TNF-α", "CRP", "IL-1β"],
        "Degeneration": ["Creatinine (urine)", "3-Methylhistidine"],
    })
    
    # Tissue/cell focus
    tissue_focus: List[Dict[str, str]] = field(default_factory=lambda: [
        {"cell_type": "Skeletal Muscle Fiber (Type II)", "role": "Primary target for loss", "priority": "high"},
        {"cell_type": "Satellite Cell", "role": "Muscle regeneration", "priority": "high"},
        {"cell_type": "Motor Neuron", "role": "Neuromuscular junction", "priority": "medium"},
        {"cell_type": "Mitochondria", "role": "Energy metabolism", "priority": "high"},
        {"cell_type": "Immune Cell (Macrophage)", "role": "Inflammation, remodeling", "priority": "medium"},
    ])
    
    @classmethod
    def get_default(cls) -> "SarcopeniaOntology":
        """Get default Sarcopenia ontology"""
        return cls(
            subtypes=cls._get_default_subtypes(),
            stages=cls._get_default_stages(),
        )
    
    @staticmethod
    def _get_default_subtypes() -> List[SarcopeniaSubtype]:
        return [
            SarcopeniaSubtype(
                name="Primary (Age-related) Sarcopenia",
                code="SARC_PRIMARY",
                description="Natural age-related muscle loss without obvious cause",
                prevalence_pct=65.0,
                key_features=["Age >65", "Anabolic resistance", "Mitochondrial dysfunction"],
                priority_targets=["MTOR", "FOXO1", "FOXO3", "AMPK", "MSTN", "PGC1A"],
                prognosis_notes="Progressive, leads to frailty, falls, loss of independence",
            ),
            SarcopeniaSubtype(
                name="Cachexia-associated",
                code="SARC_CACHEXIA",
                description="Muscle wasting associated with chronic disease",
                prevalence_pct=20.0,
                key_features=["Cancer", "CHF", "CKD", "COPD", "RA", "Systemic inflammation"],
                priority_targets=["MTOR", "NLRP3", "NFKB1", "FOXO1", "AKT1"],
                prognosis_notes="Often reversible if underlying disease treated",
            ),
            SarcopeniaSubtype(
                name="Disuse Sarcopenia",
                code="SARC_DISUSE",
                description="Muscle atrophy from immobilization or bed rest",
                prevalence_pct=10.0,
                key_features=["Bed rest", "Limb immobilization", "Sedentary lifestyle"],
                priority_targets=["MTOR", "AMPK", "FOXO1", "MYOD1"],
                prognosis_notes="Potentially reversible with rehabilitation",
            ),
            SarcopeniaSubtype(
                name="Frailty",
                code="SARC_FRAILTY",
                description="Multisystem decline with sarcopenia as key component",
                prevalence_pct=15.0,
                key_features=["Weight loss", "Exhaustion", "Low activity", "Slow gait", "Weakness"],
                priority_targets=["MTOR", "SIRT1", "AMPK", "MSTN"],
                prognosis_notes="High mortality, falls, hospitalization risk",
            ),
        ]
    
    @staticmethod
    def _get_default_stages() -> List[SarcopeniaStageDefinition]:
        return [
            SarcopeniaStageDefinition(
                stage=SarcopeniaStage.PRESARCOPENIA,
                description="Low muscle mass with normal strength",
                diagnostic_criteria={
                    "muscle_mass": "Appendicular lean mass <7.26 kg/m² (men), <5.5 kg/m² (women)",
                    "strength": "Normal",
                    "performance": "Normal",
                },
                recommended_endpoints=["Muscle mass preservation", "Prevent strength decline"],
                typical_intervention="Resistance exercise, protein supplementation",
            ),
            SarcopeniaStageDefinition(
                stage=SarcopeniaStage.SARCOPENIA,
                description="Low muscle mass + low strength OR low performance",
                diagnostic_criteria={
                    "muscle_mass": "Below threshold",
                    "strength": "Grip strength <26 kg (men), <16 kg (women)",
                    "performance": "Gait speed ≤0.8 m/s",
                },
                recommended_endpoints=["Strength improvement", "Physical function", "Fall prevention"],
                typical_intervention="Exercise + nutrition + pharmacotherapy",
            ),
            SarcopeniaStageDefinition(
                stage=SarcopeniaStage.SEVERE_SARCOPENIA,
                description="All three criteria met (low mass, strength, performance)",
                diagnostic_criteria={
                    "muscle_mass": " Significantly below threshold",
                    "strength": "Grip strength <26 kg (men), <16 kg (women)",
                    "performance": "SPPB ≤3 or gait speed <0.8 m/s",
                },
                recommended_endpoints=["Functional independence", "Quality of life", "Survival"],
                typical_intervention="Multimodal including pharmacotherapy",
            ),
        ]


# Convenience function
def get_sarcopenia_ontology() -> SarcopeniaOntology:
    return SarcopeniaOntology.get_default()
