"""
Lung Fibrosis Ontology

Disease definitions, subtypes, stages, and biological axes for Lung Fibrosis.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class LungFibrosisStage(Enum):
    EARLY = "early"                    # Mild, limited fibrosis
    MODERATE = "moderate"              # Moderate progression
    ADVANCED = "advanced"              # Advanced, extensive fibrosis
    END_STAGE = "end_stage"            # Severe, lung transplant evaluation


class LungFibrosisAxis(Enum):
    FIBROBLAST_ACTIVATION = "fibroblast_activation"
    EPITHELIAL_DYSFUNCTION = "epithelial_dysfunction"
    INFLAMMATION = "inflammation"
    ECM_DEPOSITION = "ecm_deposition"
    WOUND_HEALING = "wound_healing"
    GAS_EXCHANGE = "gas_exchange"


@dataclass
class LungFibrosisSubtype:
    """Lung fibrosis subtype definition"""
    name: str
    code: str
    description: str
    prevalence_pct: float
    key_features: List[str]
    priority_targets: List[str]
    prognosis_notes: str


@dataclass
class LungFibrosisOntology:
    """Complete Lung Fibrosis ontology"""
    
    disease_name: str = "Idiopathic Pulmonary Fibrosis (IPF)"
    icd10_code: str = "J84.10"
    
    subtypes: List[LungFibrosisSubtype] = field(default_factory=list)
    
    pathways: Dict[str, List[str]] = field(default_factory=lambda: {
        "TGF-β Signaling": ["TGFB1", "SMAD2", "SMAD3", "SMAD7", "TGFBR1", "TGFBR2"],
        "Wnt/β-catenin": ["CTNNB1", "WNT1", "FZD1", "LRP6"],
        "FGF Signaling": ["FGF1", "FGFR1", "FGFR2", "FGFR3"],
        "PDGF Signaling": ["PDGFA", "PDGFB", "PDGFRA", "PDGFRB"],
        "ECM Organization": ["COL1A1", "COL3A1", "ELN", "FN1", "MMP2", "MMP9", "TIMP1"],
        "Epithelial-Mesenchymal": ["SNAI1", "ZEB1", "VIM", "CDH2"],
        "Integrin Signaling": ["ITGAV", "ITGA5", "ITGB1", "ITGB5"],
        "Growth Factor": ["CTGF", "PDGFC", "HBEGF"],
    })
    
    biomarkers: Dict[str, List[str]] = field(default_factory=lambda: {
        "Diagnosis": ["High-resolution CT (HRCT)", "Lung biopsy (surgical)"],
        "Disease Severity": ["FVC % predicted", "DLCO % predicted", "6MWD"],
        "Progression": ["FVC decline rate", "KL-6", "SP-D", "CC16"],
        "Fibrosis": ["Procollagen III peptide", "Hydroxyproline", "ELF score"],
        "Inflammation": ["CRP", "ESR", "IL-6"],
        "Prognosis": ["GAP index", "CPI", "Brigade index"],
    })
    
    tissue_focus: List[Dict[str, str]] = field(default_factory=lambda: [
        {"cell_type": "Lung Fibroblast", "role": "Primary collagen-producing cell", "priority": "high"},
        {"cell_type": "Alveolar Epithelium (ATII)", "role": "Repair capacity, surfactant", "priority": "high"},
        {"cell_type": "Macrophage", "role": "Inflammation, wound healing", "priority": "medium"},
        {"cell_type": "Neutrophil", "role": "Acute inflammation", "priority": "low"},
        {"cell_type": "Endothelium", "role": "Vascular remodeling", "priority": "medium"},
    ])
    
    @classmethod
    def get_default(cls) -> "LungFibrosisOntology":
        return cls(
            subtypes=cls._get_default_subtypes(),
        )
    
    @staticmethod
    def _get_default_subtypes() -> List[LungFibrosisSubtype]:
        return [
            LungFibrosisSubtype(
                name="Idiopathic Pulmonary Fibrosis",
                code="IPF",
                description="Cryptogenic fibrosing alveolitis of unknown cause",
                prevalence_pct=50.0,
                key_features=["UIP pattern on CT", "Usual interstitial pneumonia", "Poor prognosis"],
                priority_targets=["TGFB1", "MMP7", "ITGAV", "CTGF"],
                prognosis_notes="Median survival 2-5 years from diagnosis",
            ),
            LungFibrosisSubtype(
                name="Progressive Pulmonary Fibrosis",
                code="PPF",
                description="Fibrosing lung diseases with progressive phenotype",
                prevalence_pct=20.0,
                key_features=[">10% FVC decline in 24 months", "Various etiologies"],
                priority_targets=["TGFB1", "COL1A1", "MMP7"],
                prognosis_notes="Variable, generally poor",
            ),
            LungFibrosisSubtype(
                name="Autoimmune-related Fibrosis",
                code="AIF",
                description="Lung fibrosis associated with autoimmune disease",
                prevalence_pct=15.0,
                key_features=["RA-ILD", "SSc-ILD", "Systemic sclerosis"],
                priority_targets=["TGFB1", "NFKB1", "IL6"],
                prognosis_notes="May respond to immunosuppression",
            ),
            LungFibrosisSubtype(
                name="Post-COVID Fibrosis",
                code="COVID_FIB",
                description="Persistent fibrosis after COVID-19 pneumonia",
                prevalence_pct=10.0,
                key_features=["Post-viral", "Variable pattern"],
                priority_targets=["TGFB1", "VIM", "SNAI1"],
                prognosis_notes="Variable, some improvement over time",
            ),
        ]


def get_lung_fibrosis_ontology() -> LungFibrosisOntology:
    return LungFibrosisOntology.get_default()
