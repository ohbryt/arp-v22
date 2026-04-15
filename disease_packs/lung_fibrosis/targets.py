"""
Lung Fibrosis Target Definitions

Target-specific scoring, evidence, and configurations for Lung Fibrosis.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.schema import TargetScores


@dataclass
class LungFibrosisScoreConfig:
    """Disease-specific score configuration for Lung Fibrosis target"""
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
    
    # Relevance to Lung Fibrosis axes
    fibroblast_relevance: float = 0.0
    epithelial_relevance: float = 0.0
    inflammation_relevance: float = 0.0
    ecm_relevance: float = 0.0
    
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
# LUNG FIBROSIS TARGET REGISTRY
# ============================================================================

LUNG_FIBROSIS_TARGETS: Dict[str, LungFibrosisScoreConfig] = {
    "TGFB1": LungFibrosisScoreConfig(
        gene_name="TGFB1",
        protein_name="Transforming Growth Factor Beta 1",
        genetic_causality=0.75,
        disease_context=0.92,
        perturbation_rescue=0.88,
        tissue_specificity=0.60,
        druggability=0.80,
        safety=0.55,  # Wound healing concern
        translation=0.85,
        competitive_novelty=0.50,
        fibroblast_relevance=0.95,
        epithelial_relevance=0.70,
        inflammation_relevance=0.65,
        ecm_relevance=0.90,
        evidence_level="phase3",
        recommended_biomarker="FVC, DLCO, KL-6",
        clinical_references=["NCT03824948", "NCT03918186"],
        drugs=["Pirfenidone (TGF-β modulation)", "Nintedanib (TKI, anti-fibrotic)"],
        key_papers=["Khalil 2016 Lancet Respir Med", "Wollin 2015 J Pharmacol Exp Ther"],
    ),
    
    "MMP7": LungFibrosisScoreConfig(
        gene_name="MMP7",
        protein_name="Matrix Metalloproteinase-7",
        genetic_causality=0.65,
        disease_context=0.85,
        perturbation_rescue=0.75,
        tissue_specificity=0.70,
        druggability=0.70,
        safety=0.80,
        translation=0.88,
        competitive_novelty=0.65,
        fibroblast_relevance=0.70,
        epithelial_relevance=0.85,
        inflammation_relevance=0.50,
        ecm_relevance=0.80,
        evidence_level="biomarker",
        recommended_biomarker="MMP7 (diagnostic and prognostic)",
        clinical_references=["NCT02936583"],
        drugs=[],
        key_papers=["Rosas 2008 Am J Respir Crit Care Med"],
    ),
    
    "ITGAV": LungFibrosisScoreConfig(
        gene_name="ITGAV",
        protein_name="Integrin Alpha-V",
        genetic_causality=0.60,
        disease_context=0.82,
        perturbation_rescue=0.80,
        tissue_specificity=0.75,
        druggability=0.80,
        safety=0.70,
        translation=0.78,
        competitive_novelty=0.75,
        fibroblast_relevance=0.85,
        epithelial_relevance=0.60,
        inflammation_relevance=0.40,
        ecm_relevance=0.75,
        evidence_level="phase2",
        recommended_biomarker="FVC",
        clinical_references=["NCT01371305"],
        drugs=["BG00011 (anti-αvβ6) - discontinued"],
        key_papers=["Munger 1999 J Clin Invest"],
    ),
    
    "CTGF": LungFibrosisScoreConfig(
        gene_name="CTGF",
        protein_name="Connective Tissue Growth Factor",
        genetic_causality=0.55,
        disease_context=0.88,
        perturbation_rescue=0.82,
        tissue_specificity=0.65,
        druggability=0.70,
        safety=0.65,
        translation=0.80,
        competitive_novelty=0.70,
        fibroblast_relevance=0.92,
        epithelial_relevance=0.55,
        inflammation_relevance=0.50,
        ecm_relevance=0.85,
        evidence_level="phase2",
        recommended_biomarker="Collagen markers",
        clinical_references=["NCT03848087"],
        drugs=["Pamrevlumab (anti-CTGF, Phase 2/3)"],
        key_papers=["Ponta 2008 Nat Rev Drug Discov"],
    ),
    
    "COL1A1": LungFibrosisScoreConfig(
        gene_name="COL1A1",
        protein_name="Collagen Type I Alpha 1",
        genetic_causality=0.50,
        disease_context=0.85,
        perturbation_rescue=0.70,
        tissue_specificity=0.60,
        druggability=0.40,
        safety=0.75,
        translation=0.75,
        competitive_novelty=0.60,
        fibroblast_relevance=0.90,
        epithelial_relevance=0.20,
        inflammation_relevance=0.30,
        ecm_relevance=0.95,
        evidence_level="downstream",
        recommended_biomarker="Procollagen I peptide",
        clinical_references=[],
        drugs=["Pirfenidone (indirect)"],
        key_papers=["Kuhn 2003 Am J Respir Crit Care Med"],
    ),
    
    "SMAD3": LungFibrosisScoreConfig(
        gene_name="SMAD3",
        protein_name="SMAD Family Member 3",
        genetic_causality=0.60,
        disease_context=0.82,
        perturbation_rescue=0.78,
        tissue_specificity=0.55,
        druggability=0.35,
        safety=0.60,
        translation=0.70,
        competitive_novelty=0.80,
        fibroblast_relevance=0.85,
        epithelial_relevance=0.70,
        inflammation_relevance=0.55,
        ecm_relevance=0.80,
        evidence_level="preclinical",
        recommended_biomarker="pSMAD3",
        clinical_references=[],
        drugs=[],
        key_papers=["Derynck 2014 Nature"],
    ),
    
    "PDGFRA": LungFibrosisScoreConfig(
        gene_name="PDGFRA",
        protein_name="Platelet-Derived Growth Factor Receptor Alpha",
        genetic_causality=0.55,
        disease_context=0.78,
        perturbation_rescue=0.75,
        tissue_specificity=0.70,
        druggability=0.85,
        safety=0.68,
        translation=0.80,
        competitive_novelty=0.55,
        fibroblast_relevance=0.88,
        epithelial_relevance=0.40,
        inflammation_relevance=0.35,
        ecm_relevance=0.70,
        evidence_level="approved",
        recommended_biomarker="FVC",
        clinical_references=["NCT00204816"],
        drugs=["Nintedanib (TKI, approved for IPF)"],
        key_papers=["Wollin 2015 J Pharmacol Exp Ther"],
    ),
    
    "CXCR4": LungFibrosisScoreConfig(
        gene_name="CXCR4",
        protein_name="C-X-C Motif Chemokine Receptor 4",
        genetic_causality=0.50,
        disease_context=0.72,
        perturbation_rescue=0.70,
        tissue_specificity=0.65,
        druggability=0.82,
        safety=0.70,
        translation=0.72,
        competitive_novelty=0.75,
        fibroblast_relevance=0.65,
        epithelial_relevance=0.55,
        inflammation_relevance=0.80,
        ecm_relevance=0.50,
        evidence_level="phase1",
        recommended_biomarker="FVC",
        clinical_references=["NCT03335579"],
        drugs=["Baloatapress (BX) - Phase 1"],
        key_papers=["Xu 2019 Nat Commun"],
    ),
}


# ============================================================================
# TARGET LOOKUP FUNCTIONS
# ============================================================================

class LungFibrosisTargets:
    """Utility class for Lung Fibrosis target access"""
    
    @staticmethod
    def get_all() -> Dict[str, LungFibrosisScoreConfig]:
        return LUNG_FIBROSIS_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[LungFibrosisScoreConfig]:
        return LUNG_FIBROSIS_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(LUNG_FIBROSIS_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[LungFibrosisScoreConfig]:
        """Get top N targets by composite score"""
        scored = []
        for gene, config in LUNG_FIBROSIS_TARGETS.items():
            score = (
                config.disease_context * 0.30 +
                config.perturbation_rescue * 0.25 +
                config.fibroblast_relevance * 0.15 +
                config.translation * 0.15 +
                config.druggability * 0.15
            )
            scored.append((gene, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]
