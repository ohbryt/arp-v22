"""
Sarcopenia Target Definitions

Target-specific scoring, evidence, and configurations for Sarcopenia.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from core.schema import TargetScores


@dataclass
class SarcopeniaScoreConfig:
    """Disease-specific score configuration for a Sarcopenia target"""
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
    
    # Relevance to Sarcopenia axes
    anabolism_relevance: float = 0.0    # 0-1
    catabolism_relevance: float = 0.0   # 0-1
    mitochondrial_relevance: float = 0.0  # 0-1
    neuromuscular_relevance: float = 0.0  # 0-1
    
    # Clinical evidence level
    evidence_level: str = "preclinical"
    
    # Recommended biomarker
    recommended_biomarker: Optional[str] = None
    
    # Functional endpoint mapping
    functional_endpoint: Optional[str] = None  # e.g., "grip_strength", "muscle_mass_DXA"
    
    # Clinical references
    clinical_references: List[str] = field(default_factory=list)
    
    # Developmental agents
    developmental_agents: List[str] = field(default_factory=list)
    
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
# SARCOPENIA TARGET REGISTRY
# ============================================================================

SARCOPENIA_TARGETS: Dict[str, SarcopeniaScoreConfig] = {
    "MTOR": SarcopeniaScoreConfig(
        gene_name="MTOR",
        protein_name="Mechanistic target of rapamycin",
        genetic_causality=0.60,
        disease_context=0.88,
        perturbation_rescue=0.90,  # Strong preclinical rescue
        tissue_specificity=0.55,  # Broad expression
        druggability=0.85,
        safety=0.50,  # Immunosuppression concern
        translation=0.80,
        competitive_novelty=0.50,
        anabolism_relevance=0.95,
        catabolism_relevance=0.30,
        mitochondrial_relevance=0.50,
        neuromuscular_relevance=0.20,
        evidence_level="preclinical",
        recommended_biomarker="S6K1 phosphorylation, muscle protein synthesis (D3-creatine)",
        functional_endpoint="muscle_mass_DXA",
        developmental_agents=["Rapamycin (preclinical)", "CCI-779 (preclinical)"],
        key_papers=["Bodine 2001 PNAS", "Ravikumar 2004 Nature", "Laplante 2012 Cell"],
    ),
    
    "FOXO1": SarcopeniaScoreConfig(
        gene_name="FOXO1",
        protein_name="Forkhead box protein O1",
        genetic_causality=0.55,
        disease_context=0.85,
        perturbation_rescue=0.88,
        tissue_specificity=0.50,
        druggability=0.35,  # Transcription factor - hard
        safety=0.60,
        translation=0.70,
        competitive_novelty=0.65,
        anabolism_relevance=0.30,
        catabolism_relevance=0.95,
        mitochondrial_relevance=0.40,
        neuromuscular_relevance=0.20,
        evidence_level="preclinical",
        recommended_biomarker="MuRF1, MAFbx expression",
        functional_endpoint="grip_strength",
        developmental_agents=["AS1842856 (FOXO1 inhibitor, preclinical)"],
        key_papers=["Stitt 2004 Molecular Cell", "Sandri 2004 Cell", "Milan 2015 JCI"],
    ),
    
    "FOXO3": SarcopeniaScoreConfig(
        gene_name="FOXO3",
        protein_name="Forkhead box protein O3",
        genetic_causality=0.58,
        disease_context=0.82,
        perturbation_rescue=0.85,
        tissue_specificity=0.55,
        druggability=0.35,
        safety=0.60,
        translation=0.68,
        competitive_novelty=0.70,
        anabolism_relevance=0.25,
        catabolism_relevance=0.92,
        mitochondrial_relevance=0.45,
        neuromuscular_relevance=0.15,
        evidence_level="preclinical",
        recommended_biomarker="MAFbx expression",
        functional_endpoint="muscle_mass_DXA",
        developmental_agents=[],
        key_papers=["Demontis 2013 Aging Cell"],
    ),
    
    "MSTN": SarcopeniaScoreConfig(
        gene_name="MSTN",
        protein_name="Myostatin",
        genetic_causality=0.75,
        disease_context=0.90,
        perturbation_rescue=0.92,
        tissue_specificity=0.85,  # Muscle-specific
        druggability=0.80,
        safety=0.78,
        translation=0.85,
        competitive_novelty=0.60,
        anabolism_relevance=0.75,
        catabolism_relevance=0.70,
        mitochondrial_relevance=0.30,
        neuromuscular_relevance=0.25,
        evidence_level="phase2",
        recommended_biomarker="Myostatin levels (serum), muscle mass (DXA)",
        functional_endpoint="muscle_mass_DXA",
        clinical_references=["NCT03010384", "NCT01616277"],
        developmental_agents=["Apitegromab (Phase 2, SMA)", "Bimagrumab (Phase 2/3)", "Domagrozumab (discontinued)"],
        key_papers=["Schuelke 2004 NEJM", "Camporez 2020 JCI", "Lach-Trifiletti 2023 J Cachexia Sarcopenia Muscle"],
    ),
    
    "PRKAA1": SarcopeniaScoreConfig(
        gene_name="PRKAA1",
        protein_name="AMP-activated protein kinase (AMPK)",
        genetic_causality=0.50,
        disease_context=0.80,
        perturbation_rescue=0.78,
        tissue_specificity=0.60,
        druggability=0.75,
        safety=0.72,
        translation=0.75,
        competitive_novelty=0.55,
        anabolism_relevance=0.50,
        catabolism_relevance=0.60,
        mitochondrial_relevance=0.90,
        neuromuscular_relevance=0.20,
        evidence_level="preclinical",
        recommended_biomarker="AMPK phosphorylation, mitochondrial markers (PGC1A)",
        functional_endpoint="exercise_endurance",
        developmental_agents=["AICAR (preclinical)", "Metformin (off-label)"],
        key_papers=["Jager 2007 J Biol Chem", "Canto 2010 Nature"],
    ),
    
    "AKT1": SarcopeniaScoreConfig(
        gene_name="AKT1",
        protein_name="AKT serine/threonine kinase 1",
        genetic_causality=0.55,
        disease_context=0.82,
        perturbation_rescue=0.80,
        tissue_specificity=0.50,
        druggability=0.82,
        safety=0.55,  # Cancer concerns
        translation=0.70,
        competitive_novelty=0.45,
        anabolism_relevance=0.88,
        catabolism_relevance=0.40,
        mitochondrial_relevance=0.35,
        neuromuscular_relevance=0.25,
        evidence_level="preclinical",
        recommended_biomarker="Phospho-AKT, muscle protein synthesis",
        functional_endpoint="muscle_mass_DXA",
        developmental_agents=["SC79 (AKT activator, preclinical)"],
        key_papers=["Izumiya 2008 PNAS", "Haday 2018 FASEB J"],
    ),
    
    "MYOD1": SarcopeniaScoreConfig(
        gene_name="MYOD1",
        protein_name="Myogenic differentiation 1",
        genetic_causality=0.50,
        disease_context=0.78,
        perturbation_rescue=0.72,
        tissue_specificity=0.85,
        druggability=0.30,
        safety=0.70,
        translation=0.65,
        competitive_novelty=0.75,
        anabolism_relevance=0.50,
        catabolism_relevance=0.30,
        mitochondrial_relevance=0.25,
        neuromuscular_relevance=0.85,
        evidence_level="preclinical",
        recommended_biomarker="MYOD1 expression, satellite cell count",
        functional_endpoint="muscle_regeneration",
        developmental_agents=[],
        key_papers=["Sabourin 1999 Exp Cell Res"],
    ),
    
    "PPARGC1A": SarcopeniaScoreConfig(
        gene_name="PPARGC1A",
        protein_name="PGC-1 alpha (Peroxisome proliferator-activated receptor gamma coactivator 1-alpha)",
        genetic_causality=0.55,
        disease_context=0.75,
        perturbation_rescue=0.78,
        tissue_specificity=0.65,
        druggability=0.40,
        safety=0.75,
        translation=0.70,
        competitive_novelty=0.70,
        anabolism_relevance=0.50,
        catabolism_relevance=0.35,
        mitochondrial_relevance=0.95,
        neuromuscular_relevance=0.20,
        evidence_level="preclinical",
        recommended_biomarker="PGC1A expression, mitochondrial DNA content",
        functional_endpoint="exercise_endurance",
        developmental_agents=["ZLN005 (PGC1A activator, preclinical)"],
        key_papers=["Wenz 2009 FASEB J", "Rius-Perez 2020 Ageing Res Rev"],
    ),
    
    "SIRT1": SarcopeniaScoreConfig(
        gene_name="SIRT1",
        protein_name="Sirtuin 1",
        genetic_causality=0.52,
        disease_context=0.72,
        perturbation_rescue=0.75,
        tissue_specificity=0.55,
        druggability=0.65,
        safety=0.72,
        translation=0.68,
        competitive_novelty=0.55,
        anabolism_relevance=0.55,
        catabolism_relevance=0.50,
        mitochondrial_relevance=0.85,
        neuromuscular_relevance=0.20,
        evidence_level="preclinical",
        recommended_biomarker="NAD+/NADH ratio, SIRT1 activity",
        functional_endpoint="exercise_endurance",
        developmental_agents=["Resveratrol (preclinical)", "SRT2104 (Phase 1)"],
        key_papers=["Gomes 2018 Cell", "Milan 2015 JCI"],
    ),
    
    "ACVR2B": SarcopeniaScoreConfig(
        gene_name="ACVR2B",
        protein_name="Activin receptor type-2B",
        genetic_causality=0.65,
        disease_context=0.82,
        perturbation_rescue=0.88,
        tissue_specificity=0.80,
        druggability=0.75,
        safety=0.72,
        translation=0.78,
        competitive_novelty=0.65,
        anabolism_relevance=0.70,
        catabolism_relevance=0.75,
        mitochondrial_relevance=0.25,
        neuromuscular_relevance=0.20,
        evidence_level="phase1",
        recommended_biomarker="Activin A/B levels, muscle mass",
        functional_endpoint="muscle_mass_DXA",
        developmental_agents=["Bimagrumab (anti-ACVR2B, Phase 2/3)"],
        key_papers=["Lach-Trifiletti 2023"],
    ),
}


# ============================================================================
# TARGET LOOKUP FUNCTIONS
# ============================================================================

def get_sarcopenia_target(gene_name: str) -> Optional[SarcopeniaScoreConfig]:
    """Get Sarcopenia target configuration by gene name"""
    return SARCOPENIA_TARGETS.get(gene_name.upper())


def get_all_sarcopenia_targets() -> Dict[str, SarcopeniaScoreConfig]:
    """Get all Sarcopenia targets"""
    return SARCOPENIA_TARGETS.copy()


def get_targets_by_functional_endpoint(endpoint: str) -> Dict[str, SarcopeniaScoreConfig]:
    """Get targets filtered by functional endpoint"""
    return {
        gene: config
        for gene, config in SARCOPENIA_TARGETS.items()
        if config.functional_endpoint == endpoint
    }


def get_targets_by_axis(axis: str) -> Dict[str, SarcopeniaScoreConfig]:
    """Get targets filtered by primary axis"""
    axis_map = {
        "anabolism": "anabolism_relevance",
        "catabolism": "catabolism_relevance",
        "mitochondrial": "mitochondrial_relevance",
        "neuromuscular": "neuromuscular_relevance",
    }
    attr = axis_map.get(axis.lower())
    if not attr:
        return {}
    
    return {
        gene: config
        for gene, config in SARCOPENIA_TARGETS.items()
        if getattr(config, attr, 0) >= 0.70
    }


class SarcopeniaTargets:
    """Utility class for Sarcopenia target access"""
    
    @staticmethod
    def get_all() -> Dict[str, SarcopeniaScoreConfig]:
        return SARCOPENIA_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[SarcopeniaScoreConfig]:
        return SARCOPENIA_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(SARCOPENIA_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[SarcopeniaScoreConfig]:
        """Get top N targets by composite score"""
        scored = []
        for gene, config in SARCOPENIA_TARGETS.items():
            score = (
                config.perturbation_rescue * 0.30 +
                config.safety * 0.20 +
                config.tissue_specificity * 0.20 +
                config.disease_context * 0.15 +
                config.translation * 0.15
            )
            scored.append((gene, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]


def get_top_sarcopenia_targets(n: int = 5) -> List[SarcopeniaScoreConfig]:
    """Get top N targets by composite score (alias for SarcopeniaTargets.get_top)"""
    return SarcopeniaTargets.get_top(n)
