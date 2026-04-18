"""
Pancreatic Ductal Adenocarcinoma (PDAC) Target Definitions

PDAC-specific targets with scoring for ARP v22 Cancer Disease Pack.

Key Sources:
- KRAS G12D: MRTX1133 (Mirati/BeiGene), Phase I/II NCT05737706
- CLDN18.2: CT041 CAR-T, Phase Ib
- FAP: Stromal targeting, CAR-T approaches
- RMC-6236: pan-KRAS G12X inhibitor, Phase I

References:
- Science Translational Medicine (2026): panKRASi
- Scientific Reports (2026): MRTX1133 metastasis
- JCI (2025): KRAS Achilles heel
- PMC12528555 (2025): Emerging therapeutics
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from disease_packs.cancer.targets import CancerScoreConfig, CancerTargets


@dataclass
class PDACTargetConfig(CancerScoreConfig):
    """PDAC-specific target configuration"""
    
    # PDAC-specific attributes
    pdac_frequency: float = 0.0
    mutation_type: str = "oncogenic"
    stromal_role: Optional[str] = None  # "tumor", "stroma", "immune"
    
    # Clinical status
    clinical_trial: Optional[str] = None
    response_rate: Optional[float] = None
    
    # PDAC-specific combinations
    combination_partners: List[str] = field(default_factory=list)


# ============================================================================
# PDAC TARGET REGISTRY
# ============================================================================

PDAC_TARGETS: Dict[str, PDACTargetConfig] = {
    # =========================================================================
    # ONCOGENIC DRIVERS
    # =========================================================================
    
    "KRAS_G12D": PDACTargetConfig(
        gene_name="KRAS",
        protein_name="KRAS G12D",
        genetic_causality=0.98,
        disease_context=0.95,
        perturbation_rescue=0.92,
        tissue_specificity=0.35,
        druggability=0.88,
        safety=0.60,
        translation=0.90,
        competitive_novelty=0.85,
        dependency_score=0.95,
        therapeutic_window_score=0.55,
        biomarker_score=0.92,
        resistance_relevance=0.50,
        evidence_level="phase1_2",
        recommended_biomarker="KRAS G12D mutation (NGS)",
        companion_dx="MRTX1133 companion diagnostic",
        clinical_trial="NCT05737706",
        response_rate=0.87,
        drugs=["MRTX1133", "RMC-6236"],
        key_papers=[
            "JCI 2025: KRAS Achilles heel of pancreas cancer",
            "Sci Transl Med 2026: panKRASi (adt5511)",
            "Sci Rep 2026: MRTX1133 metastasis model"
        ],
        
        # PDAC-specific
        pdac_frequency=0.41,
        mutation_type="oncogenic_driver",
        stromal_role="tumor",
        combination_partners=["PI3K", "BRD4", "MEK", "CDK4/6", "CD40", "PD-1"]
    ),
    
    "KRAS_G12V": PDACTargetConfig(
        gene_name="KRAS",
        protein_name="KRAS G12V",
        genetic_causality=0.95,
        disease_context=0.90,
        perturbation_rescue=0.88,
        tissue_specificity=0.35,
        druggability=0.85,
        safety=0.60,
        translation=0.85,
        competitive_novelty=0.80,
        dependency_score=0.90,
        therapeutic_window_score=0.55,
        biomarker_score=0.90,
        resistance_relevance=0.45,
        evidence_level="preclinical",
        recommended_biomarker="KRAS G12V mutation",
        clinical_trial=None,
        response_rate=None,
        drugs=["RMC-6236 (pan-G12X)"],
        key_papers=[
            "Frontiers 2024: KRAS G12D targeted therapies"
        ],
        
        pdac_frequency=0.30,
        mutation_type="oncogenic_driver",
        stromal_role="tumor",
        combination_partners=["MRTX1133", "PI3K", "MEK"]
    ),
    
    "KRAS_G12R": PDACTargetConfig(
        gene_name="KRAS",
        protein_name="KRAS G12R",
        genetic_causality=0.90,
        disease_context=0.85,
        perturbation_rescue=0.85,
        tissue_specificity=0.35,
        druggability=0.82,
        safety=0.60,
        translation=0.80,
        competitive_novelty=0.85,
        dependency_score=0.88,
        therapeutic_window_score=0.55,
        biomarker_score=0.88,
        resistance_relevance=0.40,
        evidence_level="preclinical",
        recommended_biomarker="KRAS G12R mutation",
        clinical_trial=None,
        response_rate=None,
        drugs=["RMC-6236 (pan-G12X)"],
        key_papers=[],
        
        pdac_frequency=0.15,
        mutation_type="oncogenic_driver",
        stromal_role="tumor",
        combination_partners=["RMC-6236"]
    ),
    
    "TP53": PDACTargetConfig(
        gene_name="TP53",
        protein_name="TP53",
        genetic_causality=0.90,
        disease_context=0.88,
        perturbation_rescue=0.75,
        tissue_specificity=0.30,
        druggability=0.25,  # Very difficult - tumor suppressor
        safety=0.40,
        translation=0.50,
        competitive_novelty=0.60,
        dependency_score=0.70,
        therapeutic_window_score=0.30,
        biomarker_score=0.60,
        resistance_relevance=0.70,
        evidence_level="indirect",
        recommended_biomarker="TP53 mutation status",
        clinical_trial=None,
        drugs=["APR-246 (in development)"],
        key_papers=[],
        
        pdac_frequency=0.70,
        mutation_type="tumor_suppressor",
        stromal_role="tumor",
        combination_partners=["MDM2 inhibitors"]
    ),
    
    "SMAD4": PDACTargetConfig(
        gene_name="SMAD4",
        protein_name="SMAD4 (DPC4)",
        genetic_causality=0.85,
        disease_context=0.80,
        perturbation_rescue=0.60,
        tissue_specificity=0.35,
        druggability=0.20,  # Loss of function
        safety=0.50,
        translation=0.40,
        competitive_novelty=0.70,
        dependency_score=0.65,
        therapeutic_window_score=0.25,
        biomarker_score=0.55,
        resistance_relevance=0.60,
        evidence_level="indirect",
        recommended_biomarker="SMAD4 deletion (IHC/FISH)",
        clinical_trial=None,
        drugs=[],
        key_papers=[],
        
        pdac_frequency=0.55,
        mutation_type="tumor_suppressor_loss",
        stromal_role="tumor",
        combination_partners=["TGF-β inhibitors (compensate)"]
    ),
    
    "CDKN2A": PDACTargetConfig(
        gene_name="CDKN2A",
        protein_name="p16INK4a",
        genetic_causality=0.88,
        disease_context=0.82,
        perturbation_rescue=0.65,
        tissue_specificity=0.35,
        druggability=0.35,
        safety=0.45,
        translation=0.45,
        competitive_novelty=0.65,
        dependency_score=0.70,
        therapeutic_window_score=0.30,
        biomarker_score=0.60,
        resistance_relevance=0.55,
        evidence_level="indirect",
        recommended_biomarker="CDKN2A deletion",
        clinical_trial=None,
        drugs=["CDK4/6 inhibitors (compensate)"],
        key_papers=[],
        
        pdac_frequency=0.95,
        mutation_type="tumor_suppressor_loss",
        stromal_role="tumor",
        combination_partners=["CDK4/6 inhibitors"]
    ),
    
    # =========================================================================
    # CAR-T / IMMUNOTHERAPY TARGETS
    # =========================================================================
    
    "CLDN18_2": PDACTargetConfig(
        gene_name="CLDN18",
        protein_name="Claudin-18 isoform 2 (CLDN18.2)",
        genetic_causality=0.70,
        disease_context=0.88,
        perturbation_rescue=0.82,
        tissue_specificity=0.55,
        druggability=0.90,
        safety=0.45,  # On-target/off-tumor risk
        translation=0.88,
        competitive_novelty=0.75,
        dependency_score=0.75,
        therapeutic_window_score=0.50,
        biomarker_score=0.85,
        resistance_relevance=0.40,
        evidence_level="phase1b",
        recommended_biomarker="CLDN18.2 expression (IHC, 40-60% PDAC+)",
        companion_dx="CLDN18.2 IHC",
        clinical_trial="NCT04404595 (CT041)",
        response_rate=0.50,  # 2/4 patients responded
        drugs=["CT041 (CAR-T)", "AZD6422 (Armored CAR-T)"],
        key_papers=[
            "JHO 2023: CT041 CAR T cell therapy",
            "Clin Cancer Res 2024: AZD6422 preclinical",
            "Adv Healthcare Mater 2025: CLDN18.2 CAR-sEVs"
        ],
        
        pdac_frequency=0.50,
        mutation_type="cell_surface_marker",
        stromal_role="tumor",
        combination_partners=["CXCR4 antagonists", "TGF-β inhibitors", "PD-1"]
    ),
    
    "MSTN": PDACTargetConfig(
        gene_name="MSTN",
        protein_name="Mesothelin",
        genetic_causality=0.60,
        disease_context=0.75,
        perturbation_rescue=0.65,
        tissue_specificity=0.50,
        druggability=0.85,
        safety=0.40,
        translation=0.75,
        competitive_novelty=0.65,
        dependency_score=0.60,
        therapeutic_window_score=0.45,
        biomarker_score=0.70,
        resistance_relevance=0.35,
        evidence_level="phase1_2",
        recommended_biomarker="Mesothelin expression",
        clinical_trial="Multiple Phase I/II",
        response_rate=0.20,  # Limited efficacy
        drugs=["SS1P", "CAR-T (multiple)", "Anetumab ravtansine"],
        key_papers=[],
        
        pdac_frequency=0.80,
        mutation_type="cell_surface_marker",
        stromal_role="tumor",
        combination_partners=["FAP targeting", "Chemotherapy"]
    ),
    
    # =========================================================================
    # STROMAL TARGETS
    # =========================================================================
    
    "FAP": PDACTargetConfig(
        gene_name="FAP",
        protein_name="Fibroblast Activation Protein",
        genetic_causality=0.55,
        disease_context=0.90,
        perturbation_rescue=0.75,
        tissue_specificity=0.70,
        druggability=0.80,
        safety=0.55,
        translation=0.78,
        competitive_novelty=0.85,
        dependency_score=0.60,
        therapeutic_window_score=0.60,
        biomarker_score=0.65,
        resistance_relevance=0.30,
        evidence_level="preclinical",
        recommended_biomarker="FAP expression in CAFs",
        clinical_trial=None,
        response_rate=None,
        drugs=["FAP-CAR-T", "FAP antibodies", "Small molecule inhibitors"],
        key_papers=[
            "Signal Transduct Target Ther 2020: CAF targeting"
        ],
        
        pdac_frequency=0.90,  # Expressed in 90% of CAFs
        mutation_type="stromal_marker",
        stromal_role="stroma",
        combination_partners=["KRAS inhibitors", "CAR-T", "CD40 agonists"]
    ),
    
    "CXCL12": PDACTargetConfig(
        gene_name="CXCL12",
        protein_name="CXCL12 (SDF-1)",
        genetic_causality=0.50,
        disease_context=0.85,
        perturbation_rescue=0.70,
        tissue_specificity=0.60,
        druggability=0.85,
        safety=0.65,
        translation=0.80,
        competitive_novelty=0.75,
        dependency_score=0.55,
        therapeutic_window_score=0.65,
        biomarker_score=0.60,
        resistance_relevance=0.25,
        evidence_level="phase2",
        recommended_biomarker="CXCL12/CXCR4 axis activation",
        clinical_trial="Multiple Phase II",
        response_rate=None,
        drugs=["AMD3100 (Plerixafor)", "BL-8040 (Motixafortide)"],
        key_papers=[],
        
        pdac_frequency=0.75,
        mutation_type="chemokine",
        stromal_role="stroma",
        combination_partners=["CAR-T", "Chemotherapy", "PD-1"]
    ),
    
    "TGFB1": PDACTargetConfig(
        gene_name="TGFB1",
        protein_name="TGF-β1",
        genetic_causality=0.65,
        disease_context=0.88,
        perturbation_rescue=0.80,
        tissue_specificity=0.40,
        druggability=0.75,
        safety=0.50,
        translation=0.82,
        competitive_novelty=0.70,
        dependency_score=0.65,
        therapeutic_window_score=0.45,
        biomarker_score=0.70,
        resistance_relevance=0.55,
        evidence_level="phase2",
        recommended_biomarker="pSMAD2/3 nuclear localization",
        clinical_trial="Multiple Phase II",
        response_rate=None,
        drugs=["Fresolumab", "LY3200882", "Galunisertib"],
        key_papers=[
            "PMC12528555 2025: TGF-β in PDAC"
        ],
        
        pdac_frequency=0.85,
        mutation_type="fibrosis_hub",
        stromal_role="stroma",
        combination_partners=["KRAS inhibitors", "Immunotherapy", "CD40"]
    ),
    
    "IL6": PDACTargetConfig(
        gene_name="IL6",
        protein_name="Interleukin-6",
        genetic_causality=0.55,
        disease_context=0.82,
        perturbation_rescue=0.72,
        tissue_specificity=0.45,
        druggability=0.88,
        safety=0.70,
        translation=0.85,
        competitive_novelty=0.65,
        dependency_score=0.55,
        therapeutic_window_score=0.70,
        biomarker_score=0.75,
        resistance_relevance=0.50,
        evidence_level="repurposed",
        recommended_biomarker="IL-6 levels (serum)",
        clinical_trial="Multiple (tocilizumab)",
        response_rate=None,
        drugs=["Tocilizumab (IL-6R)", "Sarilumab", "Siltuximab"],
        key_papers=[
            "JHO 2023: IL-8 increase, TGF-β1 decrease in CAR-T responders"
        ],
        
        pdac_frequency=0.80,
        mutation_type="inflammatory_cytokine",
        stromal_role="immune",
        combination_partners=["CAR-T", "Chemotherapy", "KRAS inhibitors"]
    ),
    
    # =========================================================================
    # DNA REPAIR / SYNTHETIC LETHALITY
    # =========================================================================
    
    "BRCA1": PDACTargetConfig(
        gene_name="BRCA1",
        protein_name="BRCA1",
        genetic_causality=0.88,
        disease_context=0.75,
        perturbation_rescue=0.82,
        tissue_specificity=0.35,
        druggability=0.90,
        safety=0.65,
        translation=0.88,
        competitive_novelty=0.60,
        dependency_score=0.80,
        therapeutic_window_score=0.70,
        biomarker_score=0.90,
        resistance_relevance=0.40,
        evidence_level="approved",
        recommended_biomarker="Germline/somatic BRCA1 mutation, HRD score",
        companion_dx="Myriad myChoice CDx",
        clinical_trial="NCT01843582",
        response_rate=0.60,  # In BRCA+ ovarian
        drugs=["Olaparib (approved)", "Niraparib", "Rucaparib"],
        key_papers=[],
        
        pdac_frequency=0.05,  # 5-7% of PDAC
        mutation_type="dna_repair",
        stromal_role="tumor",
        combination_partners=["Chemotherapy", "免疫疗法"]
    ),
    
    "BRCA2": PDACTargetConfig(
        gene_name="BRCA2",
        protein_name="BRCA2 (FANCD1)",
        genetic_causality=0.90,
        disease_context=0.78,
        perturbation_rescue=0.85,
        tissue_specificity=0.35,
        druggability=0.90,
        safety=0.65,
        translation=0.90,
        competitive_novelty=0.60,
        dependency_score=0.85,
        therapeutic_window_score=0.70,
        biomarker_score=0.92,
        resistance_relevance=0.40,
        evidence_level="approved",
        recommended_biomarker="Germline/somatic BRCA2 mutation",
        companion_dx="Myriad myChoice CDx",
        clinical_trial="NCT01843582",
        response_rate=0.65,
        drugs=["Olaparib (approved)", "Niraparib", "Rucaparib"],
        key_papers=[],
        
        pdac_frequency=0.07,
        mutation_type="dna_repair",
        stromal_role="tumor",
        combination_partners=["Chemotherapy", "PARP inhibitors"]
    ),
    
    "PARP1": PDACTargetConfig(
        gene_name="PARP1",
        protein_name="PARP1",
        genetic_causality=0.65,
        disease_context=0.75,
        perturbation_rescue=0.70,
        tissue_specificity=0.35,
        druggability=0.88,
        safety=0.60,
        translation=0.80,
        competitive_novelty=0.55,
        dependency_score=0.70,
        therapeutic_window_score=0.55,
        biomarker_score=0.85,
        resistance_relevance=0.45,
        evidence_level="approved",
        recommended_biomarker="HRD score, BRCA mutation",
        companion_dx="Myriad myChoice CDx",
        clinical_trial="NCT01843582",
        response_rate=0.50,
        drugs=["Olaparib", "Niraparib", "Rucaparib", "Talazoparib"],
        key_papers=[],
        
        pdac_frequency=0.05,  # HRD+ subset
        mutation_type="dna_repair",
        stromal_role="tumor",
        combination_partners=["BRCA mutations", "Chemotherapy"]
    ),
    
    # =========================================================================
    # SUBTYPE MARKERS
    # =========================================================================
    
    "GATA6": PDACTargetConfig(
        gene_name="GATA6",
        protein_name="GATA6",
        genetic_causality=0.70,
        disease_context=0.82,
        perturbation_rescue=0.65,
        tissue_specificity=0.55,
        druggability=0.25,  # Transcription factor
        safety=0.55,
        translation=0.60,
        competitive_novelty=0.75,
        dependency_score=0.65,
        therapeutic_window_score=0.40,
        biomarker_score=0.90,
        resistance_relevance=0.35,
        evidence_level="biomarker",
        recommended_biomarker="GATA6 IHC (Classical subtype)",
        companion_dx="Classical PDAC classifier",
        clinical_trial=None,
        response_rate=None,
        drugs=[],
        key_papers=[
            "Sci Transl Med 2026: panKRASi selects GATA6+ classical"
        ],
        
        pdac_frequency=0.40,  # Classical subtype
        mutation_type="transcription_factor",
        stromal_role="tumor",
        combination_partners=["KRAS inhibitors (predicts response)"]
    ),
    
    "HMGA2": PDACTargetConfig(
        gene_name="HMGA2",
        protein_name="HMGA2",
        genetic_causality=0.65,
        disease_context=0.78,
        perturbation_rescue=0.60,
        tissue_specificity=0.55,
        druggability=0.20,
        safety=0.50,
        translation=0.50,
        competitive_novelty=0.80,
        dependency_score=0.60,
        therapeutic_window_score=0.35,
        biomarker_score=0.88,
        resistance_relevance=0.45,
        evidence_level="biomarker",
        recommended_biomarker="HMGA2 IHC (Basal-like subtype)",
        clinical_trial=None,
        response_rate=None,
        drugs=[],
        key_papers=[
            "Sci Transl Med 2026: HMGA2+ selected by panKRASi"
        ],
        
        pdac_frequency=0.30,  # Basal-like subtype
        mutation_type="EMT_transcription_factor",
        stromal_role="tumor",
        combination_partners=["Immunotherapy优先"]
    ),
}


# ============================================================================
# TARGET LOOKUP
# ============================================================================

class PDACTargets:
    """Utility class for PDAC target access"""
    
    @staticmethod
    def get_all() -> Dict[str, PDACTargetConfig]:
        return PDAC_TARGETS.copy()
    
    @staticmethod
    def get(gene_name: str) -> Optional[PDACTargetConfig]:
        return PDAC_TARGETS.get(gene_name.upper())
    
    @staticmethod
    def get_all_genes() -> List[str]:
        return list(PDAC_TARGETS.keys())
    
    @staticmethod
    def get_top(n: int = 5) -> List[PDACTargetConfig]:
        """Get top N PDAC targets by composite score"""
        scored = []
        for gene, config in PDAC_TARGETS.items():
            # PDAC-specific scoring
            score = (
                config.genetic_causality * 0.20 +
                config.pdac_frequency * 0.15 +
                config.dependency_score * 0.15 +
                config.biomarker_score * 0.15 +
                config.druggability * 0.15 +
                config.competitive_novelty * 0.10 +
                config.translation * 0.10
            )
            scored.append((gene, config, score))
        
        scored.sort(key=lambda x: x[2], reverse=True)
        return [item[1] for item in scored[:n]]
    
    @staticmethod
    def get_by_category(category: str) -> List[PDACTargetConfig]:
        """Get targets by category"""
        categories = {
            "driver": ["KRAS_G12D", "KRAS_G12V", "KRAS_G12R", "TP53", "SMAD4", "CDKN2A"],
            "immunotherapy": ["CLDN18_2", "MSTN"],
            "stromal": ["FAP", "CXCL12", "TGFB1", "IL6"],
            "dna_repair": ["BRCA1", "BRCA2", "PARP1"],
            "subtype": ["GATA6", "HMGA2"]
        }
        genes = categories.get(category, [])
        return [PDAC_TARGETS[g] for g in genes if g in PDAC_TARGETS]
    
    @staticmethod
    def get_by_stromal_role(role: str) -> List[PDACTargetConfig]:
        """Get targets by stromal role (tumor, stroma, immune)"""
        return [
            config for config in PDAC_TARGETS.values()
            if config.stromal_role == role
        ]


def get_pdac_summary() -> Dict:
    """Get PDAC target summary"""
    return {
        "total_targets": len(PDAC_TARGETS),
        "by_category": {
            "oncogenic_drivers": len(PDACTargets.get_by_category("driver")),
            "immunotherapy": len(PDACTargets.get_by_category("immunotherapy")),
            "stromal": len(PDACTargets.get_by_category("stromal")),
            "dna_repair": len(PDACTargets.get_by_category("dna_repair")),
            "subtype_markers": len(PDACTargets.get_by_category("subtype"))
        },
        "top_5": [t.gene_name for t in PDACTargets.get_top(5)],
        "clinical_trials": sum(1 for t in PDAC_TARGETS.values() if t.clinical_trial),
        "approved_drugs": sum(1 for t in PDAC_TARGETS.values() if t.evidence_level == "approved")
    }