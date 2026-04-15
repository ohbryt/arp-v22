"""
Heart Failure Target Definitions

Target-specific scoring, evidence, and configurations for Heart Failure.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.schema import TargetScores


@dataclass
class HeartFailureScoreConfig:
    """Disease-specific score configuration for Heart Failure target"""
    gene_name: str
    protein_name: str
    
    # 8-dimension scores (0-1)
    genetic_causality: float
    disease_context: float
    perturbation_rescue: float
    tissue_specificity: float
    druggability: float
    safety: float
    translation: float
    competitive_novelty: float
    
    # Relevance to Heart Failure axes
    remodeling_relevance: float = 0.0
    fibrosis_relevance: float = 0.0
    contractility_relevance: float = 0.0
    metabolism_relevance: float = 0.0
    
    # Subtype relevance (HFrEF vs HFpEF)
    hfreF_relevance: float = 0.0
    hfpef_relevance: float = 0.0
    
    # Clinical evidence level
    evidence_level: str = "preclinical"
    
    # Recommended biomarker
    recommended_biomarker: Optional[str] = None
    
    # Clinical trial references
    clinical_references: List[str] = field(default_factory=list)
    
    # Approved/in-development drugs
    drugs: List[str] = field(default_factory=list)
    
    # Key citations
    key_papers: List[str] = field(default_factory=list)
    
    def to_target_scores(self) -> TargetScores:
        return TargetScores(
            genetic_causality=self.genetic_causality,
            disease_context=self.disease_context,
            perturbation_rescue=self.perturbation_rescue,
            tissue_specificity=self.tissue_specificity,
            druggability=self.druggability,
            safety=self.safety,
            translation=self.translation,
            competitive_novelty=self.competitive_novelty,
        )


# ============================================================================
# HEART FAILURE TARGET REGISTRY
# ============================================================================

HEART_FAILURE_TARGETS: Dict[str, HeartFailureScoreConfig] = {
    "NPPA": HeartFailureScoreConfig(
        gene_name="NPPA",
        protein_name="Natriuretic Peptide A (ANP)",
        genetic_causality=0.75,
        disease_context=0.88,
        perturbation_rescue=0.85,
        tissue_specificity=0.70,
        druggability=0.75,
        safety=0.85,
        translation=0.92,
        competitive_novelty=0.60,
        remodeling_relevance=0.60,
        fibrosis_relevance=0.50,
        contractility_relevance=0.75,
        metabolism_relevance=0.55,
        hfreF_relevance=0.80,
        hfpef_relevance=0.85,
        evidence_level="approved",
        recommended_biomarker="NT-proBNP, BNP",
        clinical_references=["NCT01945316", "NCT00811486"],
        drugs=["Nesiritide (recombinant BNP)", "Entresto (ARNI)"],
        key_papers=["McKie 2016 Circulation", "Solomon 2012 JACC"],
    ),
    
    "NPPB": HeartFailureScoreConfig(
        gene_name="NPPB",
        protein_name="Natriuretic Peptide B (BNP)",
        genetic_causality=0.72,
        disease_context=0.90,
        perturbation_rescue=0.88,
        tissue_specificity=0.72,
        druggability=0.70,
        safety=0.88,
        translation=0.95,
        competitive_novelty=0.55,
        remodeling_relevance=0.65,
        fibrosis_relevance=0.55,
        contractility_relevance=0.80,
        metabolism_relevance=0.50,
        hfreF_relevance=0.85,
        hfpef_relevance=0.88,
        evidence_level="approved",
        recommended_biomarker="NT-proBNP (gold standard)",
        clinical_references=["NCT01074255"],
        drugs=["Nesiritide", "NT-proBNP (diagnostic)"],
        key_papers=["Maisel 2002 NEJM"],
    ),
    
    "SLC5A2": HeartFailureScoreConfig(
        gene_name="SLC5A2",
        protein_name="Sodium-Glucose Cotransporter 2 (SGLT2)",
        genetic_causality=0.60,
        disease_context=0.85,
        perturbation_rescue=0.82,
        tissue_specificity=0.40,  # Kidney, not heart
        druggability=0.95,
        safety=0.85,
        translation=0.90,
        competitive_novelty=0.50,
        remodeling_relevance=0.70,
        fibrosis_relevance=0.75,
        contractility_relevance=0.50,
        metabolism_relevance=0.85,
        hfreF_relevance=0.92,
        hfpef_relevance=0.88,
        evidence_level="approved",
        recommended_biomarker="NT-proBNP, eGFR, HbA1c",
        clinical_references=["NCT03036124", "NCT02829255", "NCT03521934"],
        drugs=["Empagliflozin (approved HF indication)", "Dapagliflozin (approved HF)", "Canagliflozin"],
        key_papers=["Packer 2020 NEJM (EMPEROR-Reduced)", "Anker 2021 NEJM (EMPEROR-Preserved)"],
    ),
    
    "AGTR1": HeartFailureScoreConfig(
        gene_name="AGTR1",
        protein_name="Angiotensin II Receptor Type 1",
        genetic_causality=0.70,
        disease_context=0.88,
        perturbation_rescue=0.85,
        tissue_specificity=0.65,
        druggability=0.92,
        safety=0.70,
        translation=0.88,
        competitive_novelty=0.40,
        remodeling_relevance=0.88,
        fibrosis_relevance=0.85,
        contractility_relevance=0.55,
        metabolism_relevance=0.40,
        hfreF_relevance=0.90,
        hfpef_relevance=0.82,
        evidence_level="approved",
        recommended_biomarker="BNP, cardiac remodeling (echo)",
        clinical_references=["NCT00538317"],
        drugs=["Losartan", "Valsartan", "Entresto (ARNI)"],
        key_papers=["Pfeffer 2015 Lancet"],
    ),
    
    "ARNI": HeartFailureScoreConfig(
        gene_name="ARNI",
        protein_name="Angiotensin Receptor-Neprilysin Inhibitor (Target Complex)",
        genetic_causality=0.65,
        disease_context=0.90,
        perturbation_rescue=0.88,
        tissue_specificity=0.60,
        druggability=0.88,
        safety=0.75,
        translation=0.90,
        competitive_novelty=0.55,
        remodeling_relevance=0.85,
        fibrosis_relevance=0.82,
        contractility_relevance=0.60,
        metabolism_relevance=0.45,
        hfreF_relevance=0.95,
        hfpef_relevance=0.78,
        evidence_level="approved",
        recommended_biomarker="NT-proBNP, LVEF, KCCQ",
        clinical_references=["NCT01035255"],
        drugs=["Sacubitril/Valsartan (Entresto) - approved"],
        key_papers=["McMurray 2014 NEJM (PARADIGM-HF)"],
    ),
    
    "NFKB1": HeartFailureScoreConfig(
        gene_name="NFKB1",
        protein_name="Nuclear Factor Kappa B Subunit 1",
        genetic_causality=0.55,
        disease_context=0.78,
        perturbation_rescue=0.72,
        tissue_specificity=0.50,
        druggability=0.40,
        safety=0.60,
        translation=0.65,
        competitive_novelty=0.80,
        remodeling_relevance=0.75,
        fibrosis_relevance=0.80,
        contractility_relevance=0.55,
        metabolism_relevance=0.50,
        hfreF_relevance=0.65,
        hfpef_relevance=0.80,
        evidence_level="preclinical",
        recommended_biomarker="p-NFκB, inflammatory cytokines",
        clinical_references=[],
        drugs=[],
        key_papers=["Van der Heiden 2010 J Mol Cell Cardiol"],
    ),
    
    "PPARGC1A": HeartFailureScoreConfig(
        gene_name="PPARGC1A",
        protein_name="PGC-1 Alpha",
        genetic_causality=0.58,
        disease_context=0.75,
        perturbation_rescue=0.72,
        tissue_specificity=0.60,
        druggability=0.35,
        safety=0.78,
        translation=0.68,
        competitive_novelty=0.85,
        remodeling_relevance=0.50,
        fibrosis_relevance=0.45,
        contractility_relevance=0.60,
        metabolism_relevance=0.92,
        hfreF_relevance=0.70,
        hfpef_relevance=0.72,
        evidence_level="preclinical",
        recommended_biomarker="PGC1A expression, mitochondrial markers",
        clinical_references=[],
        drugs=[],
        key_papers=["Riehle 2014 Circ Res"],
    ),
    
    "MMP9": HeartFailureScoreConfig(
        gene_name="MMP9",
        protein_name="Matrix Metalloproteinase-9",
        genetic_causality=0.50,
        disease_context=0.72,
        perturbation_rescue=0.65,
        tissue_specificity=0.55,
        druggability=0.70,
        safety=0.72,
        translation=0.75,
        competitive_novelty=0.60,
        remodeling_relevance=0.75,
        fibrosis_relevance=0.85,
        contractility_relevance=0.40,
        metabolism_relevance=0.30,
        hfreF_relevance=0.72,
        hfpef_relevance=0.68,
        evidence_level="biomarker",
        recommended_biomarker="MMP9, TIMP1, collagen markers",
        clinical_references=["NCT00406584"],
        drugs=[],
        key_papers=["Zile 2011 JACC"],
    ),
}


# ============================================================================
# TARGET LOOKUP FUNCTIONS
# ============================================================================

class HeartFailureTargets:
    """Utility class for Heart Failure target access"""
    
    @staticmethod
    def get_all() -> Dict[str, HeartFailureScoreConfig]:
        return HEART_FAILURE_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[HeartFailureScoreConfig]:
        return HEART_FAILURE_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(HEART_FAILURE_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[HeartFailureScoreConfig]:
        """Get top N targets by composite score"""
        scored = []
        for gene, config in HEART_FAILURE_TARGETS.items():
            score = (
                config.disease_context * 0.25 +
                config.perturbation_rescue * 0.25 +
                config.translation * 0.20 +
                config.safety * 0.15 +
                config.druggability * 0.15
            )
            scored.append((gene, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]
