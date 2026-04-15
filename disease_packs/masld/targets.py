"""
MASLD Target Definitions

Target-specific scoring, evidence, and configurations for MASLD.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from core.schema import TargetScores, BiomarkerInfo, AssayRecommendation
from core.weights import WeightConfig


@dataclass
class MASHLDScoreConfig:
    """Disease-specific score configuration for a MASLD target"""
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
    
    # Relevance to MASLD axes
    steatosis_relevance: float = 0.0   # 0-1
    inflammation_relevance: float = 0.0  # 0-1
    fibrosis_relevance: float = 0.0      # 0-1
    
    # Clinical evidence level
    evidence_level: str = "preclinical"  # preclinical, phase1, phase2, phase3, approved
    
    # Recommended biomarker
    recommended_biomarker: Optional[str] = None
    
    # Clinical trial references
    clinical_references: List[str] = field(default_factory=list)
    
    # Approved drugs targeting this
    approved_drugs: List[str] = field(default_factory=list)
    
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
# MASLD TARGET REGISTRY
# ============================================================================

MASLD_TARGETS: Dict[str, MASHLDScoreConfig] = {
    "THRB": MASHLDScoreConfig(
        gene_name="THRB",
        protein_name="Thyroid hormone receptor beta",
        genetic_causality=0.85,
        disease_context=0.90,
        perturbation_rescue=0.95,
        tissue_specificity=0.75,
        druggability=0.90,
        safety=0.75,
        translation=0.90,
        competitive_novelty=0.70,
        steatosis_relevance=0.95,
        inflammation_relevance=0.60,
        fibrosis_relevance=0.55,
        evidence_level="approved",
        recommended_biomarker="LDL-C, hepatic fat (MRS)",
        clinical_references=["NCT03900429", "NCT04109599"],
        approved_drugs=["Resmetirom (FDA approved 2024)"],
        key_papers=["Newman 2020 NEJM", "Harrison 2024 NEJM"],
    ),
    
    "NR1H4": MASHLDScoreConfig(
        gene_name="NR1H4",
        protein_name="Farnesoid X receptor (FXR)",
        genetic_causality=0.80,
        disease_context=0.88,
        perturbation_rescue=0.85,
        tissue_specificity=0.80,
        druggability=0.92,
        safety=0.70,
        translation=0.85,
        competitive_novelty=0.65,
        steatosis_relevance=0.85,
        inflammation_relevance=0.70,
        fibrosis_relevance=0.65,
        evidence_level="approved",
        recommended_biomarker="ALP, bilirubin, FGF19",
        clinical_references=["REGENERATE", "NCT02548351"],
        approved_drugs=["Obeticholic acid (NASH approved 2023)"],
        key_papers=["Mudaliar 2013 Gastroenterology", "Harrison 2019 Lancet"],
    ),
    
    "PPARA": MASHLDScoreConfig(
        gene_name="PPARA",
        protein_name="Peroxisome proliferator-activated receptor alpha",
        genetic_causality=0.65,
        disease_context=0.82,
        perturbation_rescue=0.78,
        tissue_specificity=0.85,
        druggability=0.90,
        safety=0.72,
        translation=0.75,
        competitive_novelty=0.55,
        steatosis_relevance=0.90,
        inflammation_relevance=0.70,
        fibrosis_relevance=0.50,
        evidence_level="phase3",
        recommended_biomarker="Triglycerides, ALT, liver fat",
        clinical_references=["NCT03052121"],
        approved_drugs=["Fenofibrate (off-label)"],
        key_papers=["Staels 2015 J Hepatol"],
    ),
    
    "GLP1R": MASHLDScoreConfig(
        gene_name="GLP1R",
        protein_name="Glucagon-like peptide 1 receptor",
        genetic_causality=0.60,
        disease_context=0.85,
        perturbation_rescue=0.88,
        tissue_specificity=0.50,
        druggability=0.85,
        safety=0.80,
        translation=0.90,
        competitive_novelty=0.60,
        steatosis_relevance=0.80,
        inflammation_relevance=0.75,
        fibrosis_relevance=0.60,
        evidence_level="approved",
        recommended_biomarker="HbA1c, weight, ALT",
        clinical_references=["NCT02970968", "NCT03987451"],
        approved_drugs=["Semaglutide (FDA approved 2025 for MASLD)"],
        key_papers=["Newsom 2023 NEJM", "Loomba 2023 NEJM"],
    ),
    
    "SLC5A2": MASHLDScoreConfig(
        gene_name="SLC5A2",
        protein_name="Sodium-glucose cotransporter 2 (SGLT2)",
        genetic_causality=0.55,
        disease_context=0.78,
        perturbation_rescue=0.75,
        tissue_specificity=0.40,
        druggability=0.95,
        safety=0.82,
        translation=0.88,
        competitive_novelty=0.65,
        steatosis_relevance=0.70,
        inflammation_relevance=0.65,
        fibrosis_relevance=0.60,
        evidence_level="phase3",
        recommended_biomarker="HbA1c, eGFR, ALT, liver fat",
        clinical_references=["NCT03439244", "NCT03033160"],
        approved_drugs=["Empagliflozin (off-label)", "Canagliflozin (off-label)"],
        key_papers=["Cusi 2022 Diabetes Care", "Shai 2023 J Hepatol"],
    ),
    
    "NLRP3": MASHLDScoreConfig(
        gene_name="NLRP3",
        protein_name="NLR family pyrin domain containing 3",
        genetic_causality=0.70,
        disease_context=0.82,
        perturbation_rescue=0.80,
        tissue_specificity=0.50,
        druggability=0.75,
        safety=0.65,
        translation=0.70,
        competitive_novelty=0.75,
        steatosis_relevance=0.50,
        inflammation_relevance=0.95,
        fibrosis_relevance=0.70,
        evidence_level="preclinical",
        recommended_biomarker="IL-1β, IL-18, hs-CRP",
        clinical_references=[],
        approved_drugs=["Colchicine (off-label)"],
        key_papers=["Mridpa 2016 Nature", "Vergis 2020 Lancet"],
    ),
    
    "ACACA": MASHLDScoreConfig(
        gene_name="ACACA",
        protein_name="Acetyl-CoA carboxylase alpha",
        genetic_causality=0.60,
        disease_context=0.75,
        perturbation_rescue=0.72,
        tissue_specificity=0.75,
        druggability=0.85,
        safety=0.68,
        translation=0.70,
        competitive_novelty=0.70,
        steatosis_relevance=0.95,
        inflammation_relevance=0.40,
        fibrosis_relevance=0.30,
        evidence_level="phase2",
        recommended_biomarker="Liver fat (MRS), de novo lipogenesis",
        clinical_references=["NCT04086667"],
        approved_drugs=["Firsocostat (development discontinued)"],
        key_papers=["Loomba 2018 Hepatology"],
    ),
    
    "SREBF1": MASHLDScoreConfig(
        gene_name="SREBF1",
        protein_name="Sterol regulatory element binding transcription factor 1",
        genetic_causality=0.72,
        disease_context=0.80,
        perturbation_rescue=0.70,
        tissue_specificity=0.80,
        druggability=0.35,  # Transcription factor - hard to drug
        safety=0.60,
        translation=0.65,
        competitive_novelty=0.80,
        steatosis_relevance=0.95,
        inflammation_relevance=0.35,
        fibrosis_relevance=0.25,
        evidence_level="preclinical",
        recommended_biomarker="SREBP1c cleavage, liver fat",
        clinical_references=[],
        approved_drugs=[],
        key_papers=["Kumadaki 2008 J Lipid Res"],
    ),
    
    "HSD17B13": MASHLDScoreConfig(
        gene_name="HSD17B13",
        protein_name="17-beta hydroxysteroid dehydrogenase 13",
        genetic_causality=0.90,  # Strong genetic保护
        disease_context=0.70,
        perturbation_rescue=0.75,
        tissue_specificity=0.85,
        druggability=0.40,
        safety=0.85,
        translation=0.60,
        competitive_novelty=0.90,  # Novel target
        steatosis_relevance=0.60,
        inflammation_relevance=0.50,
        fibrosis_relevance=0.70,
        evidence_level="genetic",
        recommended_biomarker="Liver fat, ALT",
        clinical_references=[],
        approved_drugs=[],
        key_papers=["Abul-Husn 2018 Nat Genet", "Ma 2022 J Hepatol"],
    ),
    
    "PNPLA3": MASHLDScoreConfig(
        gene_name="PNPLA3",
        protein_name="Patatin-like phospholipase domain containing 3",
        genetic_causality=0.92,  # Very strong genetic
        disease_context=0.75,
        perturbation_rescue=0.60,
        tissue_specificity=0.80,
        druggability=0.30,  # Very hard target
        safety=0.75,
        translation=0.65,
        competitive_novelty=0.85,
        steatosis_relevance=0.90,
        inflammation_relevance=0.55,
        fibrosis_relevance=0.75,
        evidence_level="genetic",
        recommended_biomarker="PNPLA3 I148M genotype, liver fat",
        clinical_references=[],
        approved_drugs=[],
        key_papers=["Romeo 2008 Nat Genet", "Donner 2018 J Hepatol"],
    ),
}


# ============================================================================
# TARGET LOOKUP FUNCTIONS
# ============================================================================

class MASLDTargets:
    """Utility class for MASLD target access"""
    
    @staticmethod
    def get_all() -> Dict[str, MASHLDScoreConfig]:
        return MASLD_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[MASHLDScoreConfig]:
        return MASLD_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(MASLD_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[MASHLDScoreConfig]:
        """Get top N targets by composite score"""
        scored = []
        for config in MASLD_TARGETS.values():
            score = (
                config.disease_context * 0.35 +
                config.perturbation_rescue * 0.25 +
                config.genetic_causality * 0.15 +
                config.translation * 0.15 +
                config.druggability * 0.10
            )
            scored.append((config.gene_name, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]


def get_masld_target(gene_name: str) -> Optional[MASHLDScoreConfig]:
    """Get MASLD target configuration by gene name"""
    return MASLD_TARGETS.get(gene_name.upper())


def get_all_masld_targets() -> Dict[str, MASHLDScoreConfig]:
    """Get all MASLD targets"""
    return MASLD_TARGETS.copy()


def get_targets_by_evidence_level(level: str) -> Dict[str, MASHLDScoreConfig]:
    """Get targets filtered by clinical evidence level"""
    return {
        gene: config
        for gene, config in MASLD_TARGETS.items()
        if config.evidence_level == level
    }


def get_top_masld_targets(n: int = 5) -> List[MASHLDScoreConfig]:
    """Get top N targets by composite score"""
    scored = []
    for config in MASLD_TARGETS.values():
        # Calculate composite score (weighted by disease context + perturbation rescue)
        score = (
            config.disease_context * 0.35 +
            config.perturbation_rescue * 0.25 +
            config.genetic_causality * 0.15 +
            config.translation * 0.15 +
            config.druggability * 0.10
        )
        scored.append((gene, config, score))
    
    scored.sort(key=lambda x: x[2], reverse=True)
    return [item[1] for item in scored[:n]]
