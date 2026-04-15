"""
MASLD Ontology

Disease definitions, subtypes, stages, and biological axes for MASLD.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum


class MASHLDStage(Enum):
    STEATOSIS = "steatosis"           # Simple fatty liver
    STEATOSIS_WITH_INFLAMMATION = "steatosis_with_inflammation"
    MASH_EARLY = "mash_early"         # MASH without fibrosis
    MASH_F1 = "mash_f1"               # MASH with stage 1 fibrosis
    MASH_F2 = "mash_f2"               # MASH with stage 2 fibrosis
    MASH_F3 = "mash_f3"               # MASH with stage 3 fibrosis (bridging)
    CIRRHOSIS = "cirrhosis"           # Stage 4 fibrosis
    HCC = "hcc"                        # Hepatocellular carcinoma


class MASHLDAxis(Enum):
    LIPOGENESIS = "lipogenesis"       # Fat accumulation
    INFLAMMATION = "inflammation"     # Inflammatory response
    FIBROSIS = "fibrosis"             # Fibrotic scarring
    METABOLIC = "metabolic"           # Metabolic dysregulation
    APOPTOSIS = "apoptosis"           # Hepatocyte cell death
    REGENERATION = "regeneration"     # Liver regeneration capacity


@dataclass
class MASHLDSubtype:
    """MASLD subtype definition"""
    name: str
    code: str
    description: str
    prevalence_pct: float
    key_features: List[str]
    priority_targets: List[str]  # Gene names
    prognosis_notes: str


@dataclass
class MASHLDStageDefinition:
    """MASLD stage definition"""
    stage: MASHLDStage
    fibrosis_score: str  # e.g., "F0", "F1", "F2-F3"
    description: str
    clinical_indicators: List[str]
    recommended_endpoints: List[str]
    typical_duration_years: Optional[str] = None


@dataclass
class MASLDOntology:
    """Complete MASLD ontology"""
    
    # Disease metadata
    disease_name: str = "Metabolic dysfunction-associated steatotic liver disease"
    former_name: str = "NAFLD (Non-alcoholic fatty liver disease)"
    icd10_code: str = "K76.0"
    
    # Subtypes
    subtypes: List[MASHLDSubtype] = field(default_factory=list)
    
    # Stages
    stages: List[MASHLDStageDefinition] = field(default_factory=list)
    
    # Key pathways
    pathways: Dict[str, List[str]] = field(default_factory=lambda: {
        "Lipid Metabolism": ["SREBF1", "SREBF2", "PPARA", "PPARG", "THRB", "FXR", "ACACA", "DGAT1"],
        "Bile Acid Signaling": ["FXR", "TGR5", "SHP", "FGF19"],
        "Inflammation": ["NLRP3", "NFKB1", "JNK1", "ASK1", "TLR4"],
        "Fibrosis": ["TGFB1", "SMAD3", "COL1A1", "ACTA2", "MMP2", "MMP9", "LOXL2"],
        "Metabolic": ["GLP1R", "SGLT2", "AMPK", "mTOR", "ACC"],
        "Apoptosis": ["CASP3", "BAX", "BCL2", "P53"],
    })
    
    # Key biomarkers by stage
    biomarkers: Dict[str, List[str]] = field(default_factory=lambda: {
        "Diagnosis": ["ALT", "AST", "GGT", "Ultrasound fatty liver"],
        "Steatosis": ["Hepatic fat % (MRS)", "CAP score (FibroScan)"],
        "Inflammation": ["hs-CRP", "IL-6", "TNF-α"],
        "Fibrosis": ["FIB-4", "NFS", "ELF", "Liver stiffness (Elastography)"],
        "Severity": ["Prothrombin time", "Albumin", "Bilirubin", "Platelet count"],
        "Metabolic": ["HbA1c", "HOMA-IR", "Triglycerides", "HDL-C"],
    })
    
    # Tissue/cell focus
    tissue_focus: List[Dict[str, str]] = field(default_factory=lambda: [
        {"cell_type": "Hepatocyte", "role": "Primary metabolic cell", "priority": "high"},
        {"cell_type": "Hepatic Stellate Cell", "role": "Fibrosis driver", "priority": "high"},
        {"cell_type": "Kupffer Cell", "role": "Inflammation", "priority": "high"},
        {"cell_type": "Liver Sinusoidal Endothelial Cell", "role": "Vascular function", "priority": "medium"},
        {"cell_type": "Cholangiocyte", "role": "Bile duct", "priority": "low"},
    ])
    
    @classmethod
    def get_default(cls) -> "MASLDOntology":
        """Get default MASLD ontology"""
        return cls(
            subtypes=cls._get_default_subtypes(),
            stages=cls._get_default_stages(),
        )
    
    @staticmethod
    def _get_default_subtypes() -> List[MASHLDSubtype]:
        return [
            MASHLDSubtype(
                name="Metabolic MASLD",
                code="MASLD_MET",
                description="Standard MASLD with metabolic risk factors",
                prevalence_pct=80.0,
                key_features=["Obesity", "T2D", "Dyslipidemia", "Metabolic syndrome"],
                priority_targets=["THRB", "FXR", "PPARA", "GLP1R", "SGLT2"],
                prognosis_notes="Variable progression, ~20-30% develop MASH",
            ),
            MASHLDSubtype(
                name="MASLD with T2D",
                code="MASLD_T2D",
                description="MASLD in type 2 diabetes population",
                prevalence_pct=55.0,
                key_features=["T2D", "Insulin resistance", "Higher fibrosis risk"],
                priority_targets=["GLP1R", "SGLT2", "FXR", "THRB"],
                prognosis_notes="Higher progression rate to advanced fibrosis",
            ),
            MASHLDSubtype(
                name="Lean MASLD",
                code="MASLD_LEAN",
                description="MASLD in non-obese individuals",
                prevalence_pct=5.0,
                key_features=["BMI <25", "Metabolic abnormalities", "Genetic predisposition"],
                priority_targets=["PNPLA3", "TM6SF2", "HSD17B13"],
                prognosis_notes="May have genetic component (PNPLA3)",
            ),
        ]
    
    @staticmethod
    def _get_default_stages() -> List[MASHLDStageDefinition]:
        return [
            MASHLDStageDefinition(
                stage=MASHLDStage.STEATOSIS,
                fibrosis_score="F0",
                description="Simple fatty liver without inflammation or fibrosis",
                clinical_indicators=["Hepatic fat >5%", "Normal ALT/AST", "CAP score elevated"],
                recommended_endpoints=["Liver fat reduction (MRS)", "CAP score", "ALT normalization"],
            ),
            MASHLDStageDefinition(
                stage=MASHLDStage.MASH_F2,
                fibrosis_score="F2",
                description="MASH with moderate fibrosis (portal/perisinusoidal)",
                clinical_indicators=["Elevated ALT/AST", "NAS ≥4", "FibroScan 7-12 kPa"],
                recommended_endpoints=[" fibrosis improvement ≥1 stage", "NASH resolution", "Liver stiffness"],
            ),
            MASHLDStageDefinition(
                stage=MASHLDStage.MASH_F3,
                fibrosis_score="F3",
                description="MASH with advanced fibrosis (bridging)",
                clinical_indicators=["FibroScan 12-20 kPa", "Low albumin", "Low platelets"],
                recommended_endpoints=["Fibrosis reversal", "Clinical outcomes (decompensation)", "Transplant-free survival"],
            ),
        ]


# Convenience function
def get_masld_ontology() -> MASLDOntology:
    return MASLDOntology.get_default()
