"""
Cancer Target Definitions

Target-specific scoring, evidence, and configurations for Cancer.
Index indication: NSCLC EGFR-mutant.

Cancer scoring is different from other diseases:
- Genetic dependency is paramount (driver oncogene)
- Subtype specificity is critical
- Therapeutic window vs normal tissue
- Biomarker-defined patient selection
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.schema import TargetScores


@dataclass
class CancerScoreConfig:
    """Disease-specific score configuration for Cancer target"""
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
    
    # Cancer-specific scores
    dependency_score: float = 0.0  # CRISPR/shRNA dependency
    therapeutic_window_score: float = 0.0
    biomarker_score: float = 0.0
    resistance_relevance: float = 0.0
    
    # Subtype relevance
    nslcl_egfr_relevance: float = 0.0
    nslcl_alk_relevance: float = 0.0
    nslcl_kras_relevance: float = 0.0
    
    # Clinical evidence level
    evidence_level: str = "preclinical"
    
    # Recommended biomarker
    recommended_biomarker: Optional[str] = None
    
    # Companion diagnostic
    companion_dx: Optional[str] = None
    
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
# CANCER TARGET REGISTRY (focus on NSCLC EGFR-mutant)
# ============================================================================

CANCER_TARGETS: Dict[str, CancerScoreConfig] = {
    "EGFR": CancerScoreConfig(
        gene_name="EGFR",
        protein_name="Epidermal Growth Factor Receptor",
        genetic_causality=0.95,
        disease_context=0.92,
        perturbation_rescue=0.95,
        tissue_specificity=0.40,
        druggability=0.92,
        safety=0.55,
        translation=0.90,
        competitive_novelty=0.40,
        dependency_score=0.95,
        therapeutic_window_score=0.65,
        biomarker_score=0.95,
        resistance_relevance=0.70,
        nslcl_egfr_relevance=0.98,
        nslcl_alk_relevance=0.10,
        nslcl_kras_relevance=0.05,
        evidence_level="approved",
        recommended_biomarker="EGFR mutation (tissue or ctDNA)",
        companion_dx="Cobas EGFR Test, Guardant360",
        clinical_references=["NCT01496742", "NCT02296125"],
        drugs=["Osimertinib (1st line)", "Erlotinib", "Gefitinib", "Afatinib", "Amivantamab (biologic)"],
        key_papers=["Mok 2017 NEJM (FLAURA)", "Soria 2018 NEJM (Osimertinib)"],
    ),
    
    "T790M": CancerScoreConfig(
        gene_name="EGFR T790M",
        protein_name="EGFR T790M Resistance Mutation",
        genetic_causality=0.88,
        disease_context=0.85,
        perturbation_rescue=0.90,
        tissue_specificity=0.35,
        druggability=0.88,
        safety=0.50,
        translation=0.88,
        competitive_novelty=0.30,
        dependency_score=0.85,
        therapeutic_window_score=0.55,
        biomarker_score=0.92,
        resistance_relevance=0.95,
        nslcl_egfr_relevance=0.85,
        evidence_level="approved",
        recommended_biomarker="T790M mutation (ctDNA)",
        companion_dx="Cobas EGFR Mutation Test v2",
        clinical_references=["NCT01802632"],
        drugs=["Osimertinib (approved for T790M+)"],
        key_papers=["Pao 2005 PLoS Med", "Janne 2015 NEJM"],
    ),
    
    "C797S": CancerScoreConfig(
        gene_name="EGFR C797S",
        protein_name="EGFR C797S Resistance Mutation",
        genetic_causality=0.80,
        disease_context=0.78,
        perturbation_rescue=0.75,
        tissue_specificity=0.35,
        druggability=0.60,
        safety=0.55,
        translation=0.72,
        competitive_novelty=0.90,
        dependency_score=0.75,
        therapeutic_window_score=0.50,
        biomarker_score=0.85,
        resistance_relevance=0.98,
        nslcl_egfr_relevance=0.75,
        evidence_level="discovery",
        recommended_biomarker="C797S mutation",
        companion_dx="NGS panel",
        clinical_references=[],
        drugs=["EAI045 (allosteric, preclinical)", "JBJ-04-125-02 (allosteric)"],
        key_papers=["Jia 2016 Nature (EAI045)"],
    ),
    
    "MET": CancerScoreConfig(
        gene_name="MET",
        protein_name="Mesenchymal-Epithelial Transition Factor",
        genetic_causality=0.70,
        disease_context=0.82,
        perturbation_rescue=0.78,
        tissue_specificity=0.35,
        druggability=0.85,
        safety=0.60,
        translation=0.82,
        competitive_novelty=0.60,
        dependency_score=0.75,
        therapeutic_window_score=0.55,
        biomarker_score=0.80,
        resistance_relevance=0.88,
        nslcl_egfr_relevance=0.65,
        nslcl_alk_relevance=0.20,
        nslcl_kras_relevance=0.15,
        evidence_level="approved",
        recommended_biomarker="MET amplification or exon 14 skipping",
        companion_dx="MET FISH, NGS",
        clinical_references=["NCT02916173"],
        drugs=["Capmatinib", "Tepotinib", "Savolitinib", "Crizotinib"],
        key_papers=["Drilon 2016 JCO (Capmatinib)", "Paik 2020 NEJM (Tepotinib)"],
    ),
    
    "ALK": CancerScoreConfig(
        gene_name="ALK",
        protein_name="Anaplastic Lymphoma Kinase",
        genetic_causality=0.92,
        disease_context=0.90,
        perturbation_rescue=0.92,
        tissue_specificity=0.40,
        druggability=0.90,
        safety=0.65,
        translation=0.88,
        competitive_novelty=0.50,
        dependency_score=0.92,
        therapeutic_window_score=0.70,
        biomarker_score=0.95,
        resistance_relevance=0.60,
        nslcl_egfr_relevance=0.05,
        nslcl_alk_relevance=0.98,
        nslcl_kras_relevance=0.05,
        evidence_level="approved",
        recommended_biomarker="ALK rearrangement (FISH, IHC, NGS)",
        companion_dx="ALK FISH, VENTANA ALK IHC",
        clinical_references=["NCT00932451"],
        drugs=["Crizotinib", "Alectinib", "Lorlatinib", "Brigatinib", "Ceritinib"],
        key_papers=["Solomon 2014 NEJM (PROFILE 1014)", "Shaw 2019 JCO (ALEX)"],
    ),
    
    "KRAS": CancerScoreConfig(
        gene_name="KRAS",
        protein_name="KRAS G12C",
        genetic_causality=0.88,
        disease_context=0.85,
        perturbation_rescue=0.80,
        tissue_specificity=0.30,
        druggability=0.70,
        safety=0.55,
        translation=0.82,
        competitive_novelty=0.75,
        dependency_score=0.85,
        therapeutic_window_score=0.50,
        biomarker_score=0.90,
        resistance_relevance=0.55,
        nslcl_egfr_relevance=0.05,
        nslcl_alk_relevance=0.05,
        nslcl_kras_relevance=0.95,
        evidence_level="approved",
        recommended_biomarker="KRAS G12C mutation",
        companion_dx="QIAGEN therascreen KRAS",
        clinical_references=["NCT03600883"],
        drugs=["Sotorasib (approved)", "Adagrasib (approved)"],
        key_papers=["Fakih 2022 JCO (CodeBreaK 100)", "Janne 2022 NEJM (KRYSTAL-1)"],
    ),
    
    "PARP1": CancerScoreConfig(
        gene_name="PARP1",
        protein_name="Poly(ADP-Ribose) Polymerase 1",
        genetic_causality=0.70,
        disease_context=0.82,
        perturbation_rescue=0.78,
        tissue_specificity=0.35,
        druggability=0.85,
        safety=0.60,
        translation=0.78,
        competitive_novelty=0.55,
        dependency_score=0.72,
        therapeutic_window_score=0.55,
        biomarker_score=0.85,
        resistance_relevance=0.45,
        nslcl_egfr_relevance=0.10,
        nslcl_alk_relevance=0.10,
        nslcl_kras_relevance=0.15,
        evidence_level="approved",
        recommended_biomarker="BRCA1/2 mutation, HRD score",
        companion_dx="Myriad myChoice CDx",
        clinical_references=["NCT01843582"],
        drugs=["Olaparib", "Niraparib", "Rucaparib", "Talazoparib"],
        key_papers=["Robson 2017 NEJM (OlympiAD)", "Mateo 2020 NEJM (PROfound)"],
    ),
    
    "PD-L1": CancerScoreConfig(
        gene_name="CD274",
        protein_name="Programmed Death-Ligand 1 (PD-L1)",
        genetic_causality=0.60,
        disease_context=0.88,
        perturbation_rescue=0.82,
        tissue_specificity=0.45,
        druggability=0.88,
        safety=0.55,
        translation=0.92,
        competitive_novelty=0.45,
        dependency_score=0.65,
        therapeutic_window_score=0.60,
        biomarker_score=0.95,
        resistance_relevance=0.50,
        nslcl_egfr_relevance=0.70,
        nslcl_alk_relevance=0.70,
        nslcl_kras_relevance=0.65,
        evidence_level="approved",
        recommended_biomarker="PD-L1 TPS (IHC)",
        companion_dx="Dako 22C3, SP263",
        clinical_references=["NCT02181738"],
        drugs=["Pembrolizumab", "Atezolizumab", "Durvalumab", "Nivolumab"],
        key_papers=["Reck 2016 NEJM (KEYNOTE-024)", "Gandhi 2018 NEJM (KEYNOTE-189)"],
    ),
}


# ============================================================================
# TARGET LOOKUP FUNCTIONS
# ============================================================================

class CancerTargets:
    """Utility class for Cancer target access"""
    
    @staticmethod
    def get_all() -> Dict[str, CancerScoreConfig]:
        return CANCER_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[CancerScoreConfig]:
        return CANCER_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(CANCER_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[CancerScoreConfig]:
        """Get top N targets by composite score"""
        scored = []
        for gene, config in CANCER_TARGETS.items():
            # Cancer-specific scoring: dependency + biomarker + novelty
            score = (
                config.genetic_causality * 0.25 +
                config.dependency_score * 0.25 +
                config.biomarker_score * 0.20 +
                config.druggability * 0.15 +
                config.competitive_novelty * 0.15
            )
            scored.append((gene, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]
