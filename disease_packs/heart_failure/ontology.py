"""
Heart Failure Ontology

Disease definitions, subtypes, stages, and biological axes for Heart Failure.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class HeartFailureStage(Enum):
    STAGE_A = "stage_a"          # At risk, no symptoms
    STAGE_B = "stage_b"          # Structural heart disease, no symptoms
    STAGE_C = "stage_c"          # Structural heart disease with symptoms
    STAGE_D = "stage_d"          # Advanced heart failure


class HeartFailureAxis(Enum):
    REMODELING = "remodeling"
    FIBROSIS = "fibrosis"
    CONTRACTILITY = "contractility"
    METABOLISM = "metabolism"
    INFLAMMATION = "inflammation"
    NEUROHORMONAL = "neurohormonal"


@dataclass
class HeartFailureSubtype:
    """Heart Failure subtype definition"""
    name: str
    code: str
    description: str
    prevalence_pct: float
    key_features: List[str]
    priority_targets: List[str]
    prognosis_notes: str


@dataclass
class HeartFailureOntology:
    """Complete Heart Failure ontology"""
    
    disease_name: str = "Heart Failure"
    icd10_code: str = "I50.9"
    
    subtypes: List[HeartFailureSubtype] = field(default_factory=list)
    
    pathways: Dict[str, List[str]] = field(default_factory=lambda: {
        "Neurohormonal": ["NPPA", "NPPB", "AGTR1", "EDNRA", "ADRB1", "ADRB2"],
        "Remodeling": ["TGFB1", "SMAD3", "CTGF", "MMP2", "MMP9", "COL1A1"],
        "Metabolism": ["PPARA", "PPARD", "PPARGC1A", "SIRT1", "AMPK"],
        "Inflammation": ["NFKB1", "IL6", "TNF", "NLRP3"],
        "Contractility": ["RYR2", "SERCA2A", "PLB", "ACTA1"],
        "Fibrosis": ["POSTN", "COL1A1", "COL3A1", "LOX", "LOXL2"],
    })
    
    biomarkers: Dict[str, List[str]] = field(default_factory=lambda: {
        "Diagnosis": ["NT-proBNP", "BNP", "Troponin"],
        "Remodeling": ["LVEF", "LV mass index", "LA volume"],
        "Fibrosis": ["Native T1 mapping (MRI)", "ECV", "Collagen biomarkers"],
        "Inflammation": ["hs-CRP", "IL-6", "TNF-α", "GDF-15"],
        "Renal": ["Creatinine", "BUN", "eGFR", "Cystatin C"],
        "Metabolic": ["HbA1c", "NT-proBNP", "Uric acid"],
    })
    
    tissue_focus: List[Dict[str, str]] = field(default_factory=lambda: [
        {"cell_type": "Cardiomyocyte", "role": "Contractile function", "priority": "high"},
        {"cell_type": "Cardiac Fibroblast", "role": "Fibrosis, ECM", "priority": "high"},
        {"cell_type": "Endothelium", "role": "Vascular function", "priority": "medium"},
        {"cell_type": "Macrophage", "role": "Inflammation, repair", "priority": "medium"},
    ])
    
    @classmethod
    def get_default(cls) -> "HeartFailureOntology":
        return cls(
            subtypes=cls._get_default_subtypes(),
        )
    
    @staticmethod
    def _get_default_subtypes() -> List[HeartFailureSubtype]:
        return [
            HeartFailureSubtype(
                name="Heart Failure with Reduced Ejection Fraction",
                code="HFrEF",
                description="LVEF <40%, systolic dysfunction",
                prevalence_pct=50.0,
                key_features=["Reduced EF", "Dilated LV", "Ischemic or non-ischemic"],
                priority_targets=["NPPA", "NPPB", "AGTR1", "SLC5A2", "ARNI"],
                prognosis_notes="Improved with guidline-directed medical therapy",
            ),
            HeartFailureSubtype(
                name="Heart Failure with Preserved Ejection Fraction",
                code="HFpEF",
                description="LVEF ≥50%, diastolic dysfunction",
                prevalence_pct=40.0,
                key_features=["LV stiffening", "Comorbidities (HTN, DM, obesity)", "Normal EF"],
                priority_targets=["NPPA", "NPPB", "SGLT2", "ARNI", "NFKB1"],
                prognosis_notes="No proven mortality benefit therapies yet",
            ),
            HeartFailureSubtype(
                name="Heart Failure with Mildly Reduced Ejection Fraction",
                code="HFmrEF",
                description="LVEF 41-49%",
                prevalence_pct=10.0,
                key_features=["Intermediate phenotype", "May progress to HFrEF or HFpEF"],
                priority_targets=["SGLT2", "ARNI", "MRA"],
                prognosis_notes="May benefit from HFrEF therapies",
            ),
        ]


def get_heart_failure_ontology() -> HeartFailureOntology:
    return HeartFailureOntology.get_default()
