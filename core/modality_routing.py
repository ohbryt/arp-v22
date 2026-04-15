"""
ARP v22 - Engine 2: Target → Modality Routing

This module implements modality routing given a target and disease context.
It scores different modality options and recommends the best fit.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum

from .schema import DiseaseType, TargetDossier
from .weights import (
    MODALITY_PREFERENCES,
    TARGET_CLASS_MODALITY,
    Disease,
)


class ModalityType(Enum):
    """Available modality types"""
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    OLIGO = "oligo"
    ANTIBODY = "antibody"
    ADC = "adc"
    DEGRADER = "degrader"
    INHALED_SM = "inhaled_small_molecule"
    INHALED_BIO = "inhaled_biologic"
    CELL_THERAPY = "cell_therapy"
    GENE_THERAPY = "gene_therapy"


@dataclass
class ModalityScore:
    """Scoring for a single modality recommendation"""
    modality: str
    score: float  # 0-1 composite score
    fit_score: float  # Target-modality fit
    disease_score: float  # Disease-specific preference
    safety_score: float  # Safety for chronic use
    developability_score: float  # Ease of development
    timeline_years: float
    estimated_cost: str
    rationale: str
    key_advantages: List[str] = field(default_factory=list)
    key_risks: List[str] = field(default_factory=list)
    recommended: bool = False


@dataclass
class ModalityRoutingResult:
    """Result from routing a target to modalities"""
    target_id: str
    gene_name: str
    disease: str
    recommended_modalities: List[ModalityScore]
    primary_recommendation: Optional[ModalityScore] = None
    routing_time_seconds: float = 0.0
    
    def get_top_modality(self) -> Optional[str]:
        if self.recommended_modalities:
            return self.recommended_modalities[0].modality
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_id": self.target_id,
            "gene_name": self.gene_name,
            "disease": self.disease,
            "primary_modality": self.get_top_modality(),
            "all_modalities": [
                {
                    "modality": m.modality,
                    "score": round(m.score, 3),
                    "recommended": m.recommended,
                    "timeline": m.timeline_years,
                }
                for m in self.recommended_modalities
            ],
            "routing_time_seconds": round(self.routing_time_seconds, 3),
        }


@dataclass
class AssayRecommendation:
    """Recommended assay for target validation"""
    assay_name: str
    assay_type: str
    readout: str
    priority: str  # "primary", "secondary", "tertiary"
    gold_standard: bool = False
    development_status: str = "established"
    species_relevance: str = "human"
    estimated_cost: str = "moderate"
    timeline_weeks: int = 4


# ============================================================================
# MODALITY ROUTING ENGINE
# ============================================================================

class ModalityRouter:
    """
    Engine 2: Target → Modality Routing
    
    Given a target and disease context, routes to appropriate modality options.
    """
    
    def __init__(self):
        self._setup_default_scores()
    
    def _setup_default_scores(self):
        """Default modality scores by target class"""
        self.target_class_defaults = {
            "kinase": {
                "small_molecule": 0.90,
                "degrader": 0.70,
                "biologic": 0.40,
            },
            "nuclear_receptor": {
                "small_molecule": 0.95,
                "peptide": 0.25,
                "biologic": 0.20,
            },
            "gpcr": {
                "small_molecule": 0.80,
                "peptide": 0.90,
                "biologic": 0.70,
            },
            "transporter": {
                "small_molecule": 0.95,
            },
            "enzyme": {
                "small_molecule": 0.85,
                "oligo": 0.65,
                "biologic": 0.50,
            },
            "transcription_factor": {
                "oligo": 0.80,
                "degrader": 0.75,
                "small_molecule": 0.35,
            },
            "extracellular_ligand": {
                "biologic": 0.95,
                "peptide": 0.80,
                "antibody": 0.90,
                "small_molecule": 0.40,
            },
            "ion_channel": {
                "small_molecule": 0.95,
            },
            "cell_surface_antigen": {
                "antibody": 0.95,
                "adc": 0.90,
                "biologic": 0.80,
            },
            "myostatin_axis": {
                "antibody": 0.95,
                "biologic": 0.90,
                "peptide": 0.70,
            },
        }
        
        # Timeline and cost estimates by modality
        self.modality_timeline = {
            "small_molecule": (5.0, "moderate"),
            "biologic": (6.0, "high"),
            "peptide": (5.5, "moderate"),
            "oligo": (6.5, "high"),
            "antibody": (5.5, "high"),
            "adc": (7.0, "very_high"),
            "degrader": (6.0, "high"),
            "inhaled_small_molecule": (5.5, "moderate"),
            "inhaled_biologic": (6.5, "high"),
            "cell_therapy": (8.0, "very_high"),
            "gene_therapy": (8.0, "very_high"),
        }
        
        # Safety scores for chronic use
        self.modality_safety_chronic = {
            "small_molecule": 0.70,
            "biologic": 0.85,
            "peptide": 0.80,
            "oligo": 0.75,
            "antibody": 0.85,
            "adc": 0.60,
            "degrader": 0.65,
            "inhaled_small_molecule": 0.75,
            "inhaled_biologic": 0.80,
            "cell_therapy": 0.50,
            "gene_therapy": 0.40,
        }
    
    def route_target(
        self,
        target: TargetDossier,
        disease: DiseaseType,
    ) -> ModalityRoutingResult:
        """
        Route a target to appropriate modality options.
        
        Args:
            target: Target dossier with target information
            disease: Disease context
            
        Returns:
            ModalityRoutingResult with scored modality options
        """
        start_time = time.time()
        
        # Get disease preferences
        disease_enum = Disease(disease.value)
        disease_prefs = MODALITY_PREFERENCES.get(disease_enum, {})
        
        # Get target class
        target_class = target.target_class.value if target.target_class else "enzyme"
        class_scores = self.target_class_defaults.get(target_class, {"small_molecule": 0.70})
        
        # Calculate scores for each modality
        modality_scores = []
        
        all_modalities = set(list(class_scores.keys()) + list(disease_prefs.keys()))
        
        for modality in all_modalities:
            # Target-modality fit (from target class)
            fit_score = class_scores.get(modality, 0.30)
            
            # Disease preference
            disease_score = disease_prefs.get(modality, 0.50)
            
            # Safety for chronic use
            safety_score = self.modality_safety_chronic.get(modality, 0.60)
            
            # Developability
            developability_score = self._calc_developability(modality, target)
            
            # Composite score
            composite = (
                fit_score * 0.35 +
                disease_score * 0.25 +
                safety_score * 0.20 +
                developability_score * 0.20
            )
            
            # Timeline and cost
            timeline, cost = self.modality_timeline.get(modality, (6.0, "moderate"))
            
            # Rationale
            rationale = self._generate_rationale(modality, target, fit_score, disease_score)
            
            # Get advantages and risks
            advantages, risks = self._get_modality_pros_cons(modality, target)
            
            modality_scores.append(ModalityScore(
                modality=modality,
                score=composite,
                fit_score=fit_score,
                disease_score=disease_score,
                safety_score=safety_score,
                developability_score=developability_score,
                timeline_years=timeline,
                estimated_cost=cost,
                rationale=rationale,
                key_advantages=advantages,
                key_risks=risks,
            ))
        
        # Sort by score
        modality_scores.sort(key=lambda x: x.score, reverse=True)
        
        # Mark top recommendation
        if modality_scores:
            modality_scores[0].recommended = True
        
        elapsed = time.time() - start_time
        
        return ModalityRoutingResult(
            target_id=target.target_id,
            gene_name=target.gene_name,
            disease=disease.value,
            recommended_modalities=modality_scores,
            primary_recommendation=modality_scores[0] if modality_scores else None,
            routing_time_seconds=elapsed,
        )
    
    def _calc_developability(self, modality: str, target: TargetDossier) -> float:
        """Calculate developability score for modality"""
        base_scores = {
            "small_molecule": 0.85,
            "biologic": 0.70,
            "peptide": 0.75,
            "oligo": 0.60,
            "antibody": 0.70,
            "adc": 0.50,
            "degrader": 0.55,
            "inhaled_small_molecule": 0.75,
            "inhaled_biologic": 0.60,
            "cell_therapy": 0.30,
            "gene_therapy": 0.25,
        }
        
        base = base_scores.get(modality, 0.50)
        
        # Adjust for target properties
        if target.is_extracellular:
            if modality in ["biologic", "antibody", "peptide"]:
                base += 0.10
        
        if target.is_liver_specific and modality in ["oligo", "liver_targeted_oligo"]:
            base += 0.15
        
        return min(1.0, base)
    
    def _generate_rationale(
        self,
        modality: str,
        target: TargetDossier,
        fit_score: float,
        disease_score: float,
    ) -> str:
        """Generate rationale text for modality choice"""
        if fit_score >= 0.80:
            fit_reason = "excellent target fit"
        elif fit_score >= 0.60:
            fit_reason = "good target fit"
        else:
            fit_reason = "moderate target fit"
        
        if disease_score >= 0.80:
            disease_reason = "highly preferred for this disease"
        elif disease_score >= 0.60:
            disease_reason = "preferred for this disease"
        else:
            disease_reason = "acceptable for this disease"
        
        return f"{fit_reason}, {disease_reason}"
    
    def _get_modality_pros_cons(
        self,
        modality: str,
        target: TargetDossier,
    ) -> Tuple[List[str], List[str]]:
        """Get advantages and risks for a modality"""
        pros_cons = {
            "small_molecule": {
                "pros": ["Oral administration possible", "Established development path", "Good tissue penetration"],
                "cons": ["Off-target risk", "Metabolic stability challenges", "Selectivity issues"],
            },
            "biologic": {
                "pros": ["High specificity", "Lower off-target risk", "Proven safety"],
                "cons": ["Injection administration", "High manufacturing cost", "Potential immunogenicity"],
            },
            "peptide": {
                "pros": ["High specificity", "Modulate protein-protein interactions", "Better cell penetration than antibodies"],
                "cons": ["Stability issues", "Delivery challenges", "Short half-life often"],
            },
            "oligo": {
                "pros": ["Direct targeting of 'undruggable' targets", "High specificity for nucleic acid targets", "Liver-targeted delivery (GalNAc)"],
                "cons": ["Delivery to tissue", "Stability concerns", "Manufacturing cost"],
            },
            "antibody": {
                "pros": ["Very high specificity", "Long half-life", "Proven clinical success"],
                "cons": ["Injection only", "High cost", "Cannot target intracellular proteins"],
            },
            "adc": {
                "pros": ["Targeted payload delivery", "High potency", "Bystander effect"],
                "cons": ["Complexity", "Toxicity risk", "Resistance development"],
            },
            "degrader": {
                "pros": ["Target protein degradation", "Overcome resistance", "High specificity possible"],
                "cons": ["Chemistry challenges", "Optimizing PK/PD", "Novel regulatory pathway"],
            },
            "inhaled_small_molecule": {
                "pros": ["Local lung delivery", "Reduced systemic exposure", "Direct lung target"],
                "cons": ["Local irritation", "Limited systemic effect", "Inhalation device required"],
            },
            "inhaled_biologic": {
                "pros": ["Local lung delivery", "High specificity", "Reduced systemic side effects"],
                "cons": ["Limited tissue penetration", "Cost", "Immunogenicity risk"],
            },
        }
        
        default = {"pros": ["Viable option"], "cons": ["Development challenges"]}
        return pros_cons.get(modality, default)


# ============================================================================
# ASSAY RECOMMENDATION ENGINE
# ============================================================================

class AssayEngine:
    """
    Generates assay recommendations for target validation.
    """
    
    # Disease-specific assay templates
    ASSAY_TEMPLATES = {
        "masld": [
            AssayRecommendation(
                assay_name="Hepatocyte lipid accumulation",
                assay_type="In vitro cell assay",
                readout="Nile red or BODIPY fluorescence",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Stellate cell activation",
                assay_type="In vitro cell assay",
                readout="α-SMA expression by qPCR",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Inflammatory cytokine panel",
                assay_type="Multiplex assay",
                readout="IL-6, TNF-α, IL-1β",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="Liver organoid function",
                assay_type="3D organoid assay",
                readout="Lipid content, albumin secretion",
                priority="secondary",
                estimated_cost="high",
                timeline_weeks=8,
            ),
            AssayRecommendation(
                assay_name="In vivo liver fat (MRS)",
                assay_type="Preclinical in vivo",
                readout="Hepatic triglyceride content",
                priority="tertiary",
                species_relevance="mouse",
                estimated_cost="high",
            ),
        ],
        
        "sarcopenia": [
            AssayRecommendation(
                assay_name="Myotube atrophy rescue",
                assay_type="In vitro cell assay",
                readout="Myotube diameter, myosin heavy chain",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Muscle protein synthesis",
                assay_type="Metabolic labeling",
                readout="[³H]leucine incorporation",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Mitochondrial function",
                assay_type="Seahorse XF",
                readout="OCR, ECAR",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="Atrogen expression",
                assay_type="qPCR",
                readout="MuRF1, MAFbx expression",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="In vivo grip strength",
                assay_type="Preclinical in vivo",
                readout="Grip strength meter",
                priority="tertiary",
                species_relevance="mouse",
                estimated_cost="moderate",
            ),
            AssayRecommendation(
                assay_name="Muscle mass (DXA)",
                assay_type="Preclinical in vivo",
                readout="Lean mass measurement",
                priority="tertiary",
                species_relevance="mouse",
            ),
        ],
        
        "lung_fibrosis": [
            AssayRecommendation(
                assay_name="Fibroblast activation",
                assay_type="In vitro cell assay",
                readout="α-SMA, collagen contraction",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Collagen deposition",
                assay_type="Biochemical assay",
                readout="Hydroxyproline content",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Epithelial injury-repair",
                assay_type="Wound healing assay",
                readout="Migration, proliferation",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="Precision-cut lung slice",
                assay_type="Ex vivo tissue",
                readout="Fibrosis score, collagen",
                priority="secondary",
                estimated_cost="high",
                timeline_weeks=6,
            ),
            AssayRecommendation(
                assay_name="Lung compliance",
                assay_type="Preclinical in vivo",
                readout="FlexiVent system",
                priority="tertiary",
                species_relevance="mouse",
                estimated_cost="high",
            ),
        ],
        
        "heart_failure": [
            AssayRecommendation(
                assay_name="Cardiomyocyte hypertrophy",
                assay_type="In vitro cell assay",
                readout="Cell size, ANP/BNP secretion",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="Contractility",
                assay_type="iPSC-CMs",
                readout="Beating rate, contraction force",
                priority="primary",
                gold_standard=True,
                estimated_cost="high",
            ),
            AssayRecommendation(
                assay_name="Fibroblast activation",
                assay_type="In vitro cell assay",
                readout="α-SMA, collagen synthesis",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="Echocardiography",
                assay_type="Preclinical in vivo",
                readout="EF%, FS%, LV dimensions",
                priority="tertiary",
                species_relevance="mouse",
            ),
        ],
        
        "cancer": [
            AssayRecommendation(
                assay_name="Cell viability",
                assay_type="Cell line screening",
                readout="ATP-lite, CellTiter-Glo",
                priority="primary",
                gold_standard=True,
            ),
            AssayRecommendation(
                assay_name="CRISPR dependency",
                assay_type="Genome-wide CRISPR",
                readout="Dependency score",
                priority="primary",
                gold_standard=True,
                estimated_cost="very_high",
            ),
            AssayRecommendation(
                assay_name="Apoptosis assay",
                assay_type="Cell death assay",
                readout="Caspase-3/7, Annexin V",
                priority="secondary",
            ),
            AssayRecommendation(
                assay_name="PDX efficacy",
                assay_type="In vivo tumor model",
                readout="Tumor growth inhibition",
                priority="tertiary",
                estimated_cost="very_high",
            ),
        ],
    }
    
    def get_assays(
        self,
        disease: DiseaseType,
        target_class: Optional[str] = None,
    ) -> List[AssayRecommendation]:
        """Get assay recommendations for a disease"""
        assays = self.ASSAY_TEMPLATES.get(disease.value, [])
        
        # Could filter by target class here if needed
        return assays


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def route_to_modality(
    target: TargetDossier,
    disease: DiseaseType,
) -> ModalityRoutingResult:
    """Convenience function for routing"""
    router = ModalityRouter()
    return router.route_target(target, disease)


def get_assay_recommendations(
    disease: DiseaseType,
    target_class: Optional[str] = None,
) -> List[AssayRecommendation]:
    """Convenience function for assay recommendations"""
    engine = AssayEngine()
    return engine.get_assays(disease, target_class)
