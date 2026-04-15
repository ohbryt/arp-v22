"""
Cancer Ontology

Disease definitions, subtypes, and biological axes for Cancer.
Index indication: NSCLC EGFR-mutant.

Note: Cancer is fundamentally different from other diseases.
We prioritize TARGET DEPENDENCY and THERAPEUTIC WINDOW.
"""

from dataclasses import dataclass, field
from typing import List, Dict
from enum import Enum


class CancerStage(Enum):
    EARLY = "early"                    # Stage I-II, potentially curable
    LOCALLY_ADVANCED = "locally_advanced"  # Stage III
    METASTATIC = "metastatic"          # Stage IV
    RELAPSED = "relapsed"              # Progressed after prior therapy
    REFRACTORY = "refractory"          # Resistant to prior therapy


class CancerAxis(Enum):
    ONCOGENIC_DEPENDENCY = "oncogenic_dependency"
    RESISTANCE = "resistance"
    IMMUNE_EVASION = "immune_evasion"
    DNA_REPAIR = "dna_repair"
    APOPTOSIS = "apoptosis"
    METASTASIS = "metastasis"


@dataclass
class CancerSubtype:
    """Cancer subtype definition"""
    name: str
    code: str
    tissue_origin: str
    molecular_driver: str
    description: str
    prevalence_pct: float
    key_features: List[str]
    priority_targets: List[str]
    prognosis_notes: str


@dataclass
class CancerOntology:
    """Complete Cancer ontology"""
    
    disease_name: str = "Non-Small Cell Lung Cancer (NSCLC)"
    icd10_code: str = "C34.9"
    
    subtypes: List[CancerSubtype] = field(default_factory=list)
    
    pathways: Dict[str, List[str]] = field(default_factory=lambda: {
        "RTK Signaling": ["EGFR", "ALK", "ROS1", "MET", "RET", "KRAS", "BRAF"],
        "DNA Repair": ["BRCA1", "BRCA2", "ATM", "ATR", "PARP1", "CHEK1"],
        "Cell Cycle": ["CDK4", "CDK6", "CCNE1", "RB1", "TP53"],
        "PI3K/AKT/mTOR": ["PIK3CA", "AKT1", "MTOR", "PTEN"],
        "Apoptosis": ["BCL2", "BCL-XL", "MCL1", "BAX"],
        "Immune Evasion": ["PD-L1", "PD-L2", "CTLA4", "LAG3", "TIGIT"],
    })
    
    biomarkers: Dict[str, List[str]] = field(default_factory=lambda: {
        "Diagnosis": ["Histology", "IHC", "NGS panel"],
        "Molecular": ["EGFR mutation (PCR/NGS)", "ALK rearrangement (FISH/IHC)", "PD-L1 TPS"],
        "Resistance": ["EGFR T790M", "EGFR C797S", "ALK G1202R", "MET amplification"],
        "Monitoring": ["ctDNA (guardant)", "Tumor markers", "Imaging (RECIST)"],
        "Prognosis": ["Stage", "Performance status", "Comutations"],
    })
    
    tissue_focus: List[Dict[str, str]] = field(default_factory=lambda: [
        {"cell_type": "Tumor Cell", "role": "Primary target - oncogenic driver", "priority": "high"},
        {"cell_type": "TME - Immune", "role": "IO targets", "priority": "high"},
        {"cell_type": "TME - Fibroblast", "role": "Stroma, therapy resistance", "priority": "medium"},
        {"cell_type": "TME - Endothelium", "role": "Angiogenesis", "priority": "medium"},
    ])
    
    @classmethod
    def get_default(cls) -> "CancerOntology":
        return cls(
            subtypes=cls._get_default_subtypes(),
        )
    
    @staticmethod
    def _get_default_subtypes() -> List[CancerSubtype]:
        return [
            CancerSubtype(
                name="NSCLC EGFR-mutant (Ex19del/L858R)",
                code="NSCLC_EGFRm",
                tissue_origin="Lung",
                molecular_driver="EGFR",
                description="EGFR-activating mutations in exon 19 deletion or L858R",
                prevalence_pct=40.0,  # 40% of Asian NSCLC, 15% Caucasian
                key_features=["Sensitive to EGFR TKIs", "CNS metastases common", "Acquired resistance"],
                priority_targets=["EGFR", "T790M", "C797S", "MET"],
                prognosis_notes="OS improved with TKIs, but resistance develops",
            ),
            CancerSubtype(
                name="NSCLC EGFR C797S (Resistance)",
                code="NSCLC_EGFR_C797S",
                tissue_origin="Lung",
                molecular_driver="EGFR C797S",
                description="Third-generation EGFR TKI resistance mutation",
                prevalence_pct=15.0,  # Of T790M+ cases progressing on osimertinib
                key_features=["4th generation TKI development", "Allosteric inhibitors"],
                priority_targets=["EGFR", "EGFR allosteric", "MET"],
                prognosis_notes="Limited options, high unmet need",
            ),
            CancerSubtype(
                name="NSCLC ALK-rearranged",
                code="NSCLC_ALK",
                tissue_origin="Lung",
                molecular_driver="EML4-ALK",
                description="ALK gene fusion with EML4",
                prevalence_pct=5.0,
                key_features=["Young patients", "Never-smokers", "CNS metastases"],
                priority_targets=["ALK", "EML4-ALK"],
                prognosis_notes="Excellent response to ALK inhibitors",
            ),
            CancerSubtype(
                name="NSCLC KRAS G12C",
                code="NSCLC_KRAS_G12C",
                tissue_origin="Lung",
                molecular_driver="KRAS G12C",
                description="KRAS G12C missense mutation",
                prevalence_pct=13.0,
                key_features=["Historically 'undruggable'", "Covalent inhibitors"],
                priority_targets=["KRAS G12C", "SOS1", "SHP2"],
                prognosis_notes="Improved with sotorasib/adagrasib",
            ),
            CancerSubtype(
                name="TNBC BRCA1/2 mutated",
                code="TNBC_BRCA",
                tissue_origin="Breast",
                molecular_driver="BRCA1/2",
                description="Triple-negative breast cancer with BRCA1/2 mutation",
                prevalence_pct=15.0,
                key_features=["PARP inhibitor sensitive", "Homologous recombination deficiency"],
                priority_targets=["BRCA1", "BRCA2", "PARP1"],
                prognosis_notes="Improved with PARP inhibitors",
            ),
        ]


def get_cancer_ontology() -> CancerOntology:
    return CancerOntology.get_default()
