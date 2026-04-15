"""
ARP v22 - Engine 1: Disease → Target Scoring Engine

This module implements the target prioritization scoring engine.
Given a disease context, it scores candidate targets using disease-specific
weight matrices and returns prioritized target dossiers.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
from datetime import date

from .schema import (
    TargetDossier,
    TargetScores,
    TargetPrioritizationResult,
    DiseaseContextData,
    Penalty,
    EvidenceSource,
    BiomarkerInfo,
    AssayRecommendation,
    DiseaseType,
    TargetClass,
    Status,
    ScoringEngineConfig,
)
from .weights import (
    get_disease_weights,
    get_modality_score,
    get_penalties_for_disease,
    MODALITY_PREFERENCES,
    TARGET_CLASS_MODALITY,
    Disease,
)


# ============================================================================
# TARGET REGISTRY
# ============================================================================

@dataclass
class TargetInfo:
    """Known information about a target"""
    gene_name: str
    protein_name: str
    target_class: TargetClass
    is_extracellular: bool
    is_liver_specific: bool
    has_known_pocket: bool
    has_degradation_logic: bool
    default_scores: Optional[TargetScores] = None
    default_penalties: List[str] = field(default_factory=list)  # penalty names


# Pre-populated target registry with known targets per disease area
TARGET_REGISTRY: Dict[str, Dict[str, TargetInfo]] = {
    "masld": {
        "THRB": TargetInfo(
            gene_name="THRB",
            protein_name="Thyroid hormone receptor beta",
            target_class=TargetClass.NUCLEAR_RECEPTOR,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "NR1H4": TargetInfo(
            gene_name="NR1H4",
            protein_name="Farnesoid X receptor (FXR)",
            target_class=TargetClass.NUCLEAR_RECEPTOR,
            is_extracellular=False,
            is_liver_specific=True,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "PPARA": TargetInfo(
            gene_name="PPARA",
            protein_name="Peroxisome proliferator-activated receptor alpha",
            target_class=TargetClass.NUCLEAR_RECEPTOR,
            is_extracellular=False,
            is_liver_specific=True,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "GLP1R": TargetInfo(
            gene_name="GLP1R",
            protein_name="Glucagon-like peptide 1 receptor",
            target_class=TargetClass.GPCR,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "SLC5A2": TargetInfo(
            gene_name="SLC5A2",
            protein_name="Sodium-glucose cotransporter 2 (SGLT2)",
            target_class=TargetClass.TRANSPORTER,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "NLRP3": TargetInfo(
            gene_name="NLRP3",
            protein_name="NLR family pyrin domain containing 3",
            target_class=TargetClass.ENZYME,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "ACACA": TargetInfo(
            gene_name="ACACA",
            protein_name="Acetyl-CoA carboxylase alpha",
            target_class=TargetClass.ENZYME,
            is_extracellular=False,
            is_liver_specific=True,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "SREBF1": TargetInfo(
            gene_name="SREBF1",
            protein_name="Sterol regulatory element binding transcription factor 1",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=True,
            has_known_pocket=False,
            has_degradation_logic=True,
        ),
    },
    
    "sarcopenia": {
        "MTOR": TargetInfo(
            gene_name="MTOR",
            protein_name="Mechanistic target of rapamycin kinase",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
            default_penalties=["immunosuppression", "tumor_growth_concern"],
        ),
        "FOXO1": TargetInfo(
            gene_name="FOXO1",
            protein_name="Forkhead box protein O1",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=False,
            has_degradation_logic=True,
        ),
        "FOXO3": TargetInfo(
            gene_name="FOXO3",
            protein_name="Forkhead box protein O3",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=False,
            has_degradation_logic=True,
        ),
        "PRKAA1": TargetInfo(
            gene_name="PRKAA1",
            protein_name="AMP-activated protein kinase catalytic subunit alpha-1",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "MSTN": TargetInfo(
            gene_name="MSTN",
            protein_name="Myostatin",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "AKT1": TargetInfo(
            gene_name="AKT1",
            protein_name="AKT serine/threonine kinase 1",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
            default_penalties=["tumor_growth_concern"],
        ),
        "MYOD1": TargetInfo(
            gene_name="MYOD1",
            protein_name="Myogenic differentiation 1",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=True,
            has_known_pocket=False,
            has_degradation_logic=False,
        ),
        "PPARGC1A": TargetInfo(
            gene_name="PPARGC1A",
            protein_name="PPARG coactivator 1 alpha",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=False,
            has_degradation_logic=False,
        ),
        "SIRT1": TargetInfo(
            gene_name="SIRT1",
            protein_name="Sirtuin 1",
            target_class=TargetClass.ENZYME,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
    },
    
    "lung_fibrosis": {
        "TGFB1": TargetInfo(
            gene_name="TGFB1",
            protein_name="Transforming growth factor beta 1",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
            default_penalties=["wound_healing_inhibition", "epithelial_regeneration_impairment"],
        ),
        "COL1A1": TargetInfo(
            gene_name="COL1A1",
            protein_name="Collagen type I alpha 1 chain",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=False,
            has_degradation_logic=False,
        ),
        "MMP7": TargetInfo(
            gene_name="MMP7",
            protein_name="Matrix metalloproteinase-7",
            target_class=TargetClass.ENZYME,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "ITGAV": TargetInfo(
            gene_name="ITGAV",
            protein_name="Integrin alpha-V",
            target_class=TargetClass.CELL_SURFACE_ANTIGEN,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "CTGF": TargetInfo(
            gene_name="CTGF",
            protein_name="Connective tissue growth factor",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
    },
    
    "heart_failure": {
        "NPPA": TargetInfo(
            gene_name="NPPA",
            protein_name="Natriuretic peptide A (ANP)",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "NPPB": TargetInfo(
            gene_name="NPPB",
            protein_name="Natriuretic peptide B (BNP)",
            target_class=TargetClass.EXTRACELLULAR_LIGAND,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "SLC5A2": TargetInfo(
            gene_name="SLC5A2",
            protein_name="SGLT2",
            target_class=TargetClass.TRANSPORTER,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "EDNRA": TargetInfo(
            gene_name="EDNRA",
            protein_name="Endothelin receptor A",
            target_class=TargetClass.GPCR,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
            default_penalties=["qtc_herg_risk", "pro_arrhythmia"],
        ),
        "NFKB1": TargetInfo(
            gene_name="NFKB1",
            protein_name="Nuclear factor kappa B subunit 1",
            target_class=TargetClass.TRANSCRIPTION_FACTOR,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=False,
            has_degradation_logic=True,
        ),
    },
    
    "cancer": {
        "EGFR": TargetInfo(
            gene_name="EGFR",
            protein_name="Epidermal Growth Factor Receptor",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "ALK": TargetInfo(
            gene_name="ALK",
            protein_name="Anaplastic Lymphoma Kinase",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "MET": TargetInfo(
            gene_name="MET",
            protein_name="Mesenchymal-Epithelial Transition Factor",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "KRAS": TargetInfo(
            gene_name="KRAS",
            protein_name="KRAS G12C",
            target_class=TargetClass.KINASE,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "PD-L1": TargetInfo(
            gene_name="PD-L1",
            protein_name="Programmed Death-Ligand 1",
            target_class=TargetClass.CELL_SURFACE_ANTIGEN,
            is_extracellular=True,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
        "PARP1": TargetInfo(
            gene_name="PARP1",
            protein_name="Poly(ADP-Ribose) Polymerase 1",
            target_class=TargetClass.ENZYME,
            is_extracellular=False,
            is_liver_specific=False,
            has_known_pocket=True,
            has_degradation_logic=False,
        ),
    },
}


# ============================================================================
# DISEASE CONTEXT DEFINITIONS
# ============================================================================

DISEASE_CONTEXTS: Dict[DiseaseType, DiseaseContextData] = {
    DiseaseType.MASLD: DiseaseContextData(
        disease=DiseaseType.MASLD,
        subtype="MASH with fibrosis",
        stage="F2-F3",
        primary_axis="fibrosis",
        secondary_axes=["steatosis", "inflammation"],
        tissue_focus=["hepatocyte", "hepatic_stellate", "kupffer_cell"],
        patient_population="Adults with biopsy-proven MASH",
    ),
    
    DiseaseType.SARCOPENIA: DiseaseContextData(
        disease=DiseaseType.SARCOPENIA,
        subtype="Age-related",
        stage="Moderate to severe",
        primary_axis="muscle_function",
        secondary_axes=["anabolism", "catabolism", "mitochondrial"],
        tissue_focus=["skeletal_muscle", "satellite_cell"],
        patient_population="Older adults ≥65 years",
    ),
    
    DiseaseType.LUNG_FIBROSIS: DiseaseContextData(
        disease=DiseaseType.LUNG_FIBROSIS,
        subtype="IPF",
        stage="Mild to moderate",
        primary_axis="fibrosis",
        secondary_axes=["epithelial_dysfunction", "inflammation"],
        tissue_focus=["lung_fibroblast", "alveolar_epithelium"],
        patient_population="Adults with IPF",
    ),
    
    DiseaseType.HEART_FAILURE: DiseaseContextData(
        disease=DiseaseType.HEART_FAILURE,
        subtype="HFrEF",
        stage="NYHA II-III",
        primary_axis="remodeling",
        secondary_axes=["fibrosis", "contractility", "metabolism"],
        tissue_focus=["cardiomyocyte", "cardiac_fibroblast"],
        patient_population="Adults with HFrEF EF<40%",
    ),
    
    DiseaseType.CANCER: DiseaseContextData(
        disease=DiseaseType.CANCER,
        subtype="NSCLC EGFR-mutant",
        stage="Advanced",
        primary_axis="oncogenic_dependency",
        secondary_axes=["resistance", "immune_evasion"],
        tissue_focus=["tumor_cell"],
        patient_population="Adults with EGFRm NSCLC",
    ),
}


# ============================================================================
# SCORING ENGINE
# ============================================================================

class TargetScorer:
    """
    Engine 1: Disease → Target Scoring
    
    Given a disease context, score candidate targets using
    disease-specific weight matrices.
    """
    
    def __init__(self, config: Optional[ScoringEngineConfig] = None):
        self.config = config or ScoringEngineConfig()
    
    def score_target(
        self,
        target_info: TargetInfo,
        disease: DiseaseType,
        disease_context: Optional[DiseaseContextData] = None,
        score_overrides: Optional[Dict[str, float]] = None,
    ) -> Tuple[TargetScores, List[Penalty], float]:
        """
        Score a single target for a disease.
        
        Returns:
            Tuple of (scores, penalties, priority_score)
        """
        # Get disease weights
        disease_enum = Disease(disease.value)
        weights = get_disease_weights(disease_enum)
        
        # Use provided scores or defaults
        if score_overrides:
            # Generate default first, then merge partial overrides
            if target_info.default_scores:
                base_scores = target_info.default_scores
            else:
                base_scores = self._generate_default_scores(target_info, disease)
            # Merge: override only provided fields, keep defaults for rest
            scores_dict = base_scores.to_dict()
            scores_dict.update(score_overrides)
            scores = TargetScores(**scores_dict)
        elif target_info.default_scores:
            scores = target_info.default_scores
        else:
            # Generate default scores based on target properties
            scores = self._generate_default_scores(target_info, disease)
        
        # Calculate weighted priority score
        priority_score = self._calculate_priority_score(scores, weights)
        
        # Apply penalties
        penalties = self._apply_penalties(target_info, disease, scores)
        penalty_reduction = sum(p.severity for p in penalties) / len(penalties) if penalties else 0
        priority_score *= (1 - penalty_reduction * 0.3)  # 30% max penalty impact
        
        return scores, penalties, priority_score
    
    def _generate_default_scores(
        self,
        target_info: TargetInfo,
        disease: DiseaseType,
    ) -> TargetScores:
        """Generate PRIOR/DEFAULT scores when evidence is not available.
        
        Note: These are conservative defaults (0.4-0.6) to reflect
        uncertainty. Evidence-based scores should be higher (0.7-0.9).
        """
        
        # Conservative default scores by disease
        base_scores = {
            DiseaseType.MASLD: TargetScores(
                genetic_causality=0.45,
                disease_context=0.50,  # No evidence = conservative
                perturbation_rescue=0.50,
                tissue_specificity=0.60 if target_info.is_liver_specific else 0.40,
                druggability=0.60,
                safety=0.50,
                translation=0.45,
                competitive_novelty=0.50,
            ),
            DiseaseType.SARCOPENIA: TargetScores(
                genetic_causality=0.45,
                disease_context=0.50,
                perturbation_rescue=0.50,
                tissue_specificity=0.60 if getattr(target_info, 'is_muscle_specific', False) else 0.40,
                druggability=0.55,
                safety=0.50,
                translation=0.45,
                competitive_novelty=0.50,
            ),
            DiseaseType.LUNG_FIBROSIS: TargetScores(
                genetic_causality=0.40,
                disease_context=0.50,
                perturbation_rescue=0.50,
                tissue_specificity=0.55,
                druggability=0.55,
                safety=0.50,
                translation=0.50,
                competitive_novelty=0.50,
            ),
            DiseaseType.HEART_FAILURE: TargetScores(
                genetic_causality=0.50,
                disease_context=0.50,
                perturbation_rescue=0.50,
                tissue_specificity=0.50,
                druggability=0.60,
                safety=0.45,  # Safety concerns weighted
                translation=0.55,
                competitive_novelty=0.50,
            ),
            DiseaseType.CANCER: TargetScores(
                genetic_causality=0.55,
                disease_context=0.50,
                perturbation_rescue=0.50,
                tissue_specificity=0.35,  # Often low for cancer
                druggability=0.60,
                safety=0.40,  # Safety concerns high
                translation=0.50,
                competitive_novelty=0.55,
            ),
        }
        
        return base_scores.get(disease, TargetScores(
            genetic_causality=0.40,
            disease_context=0.40,
            perturbation_rescue=0.40,
            tissue_specificity=0.40,
            druggability=0.50,
            safety=0.40,
            translation=0.40,
            competitive_novelty=0.50,
        ))
    
    def _calculate_priority_score(
        self,
        scores: TargetScores,
        weights: Any,
    ) -> float:
        """Calculate weighted priority score"""
        return (
            scores.genetic_causality * weights.genetic_causality
            + scores.disease_context * weights.disease_context
            + scores.perturbation_rescue * weights.perturbation_rescue
            + scores.tissue_specificity * weights.tissue_specificity
            + scores.druggability * weights.druggability
            + scores.safety * weights.safety
            + scores.translation * weights.translation
            + scores.competitive_novelty * weights.competitive_novelty
        )
    
    def _apply_penalties(
        self,
        target_info: TargetInfo,
        disease: DiseaseType,
        scores: TargetScores,
    ) -> List[Penalty]:
        """Apply penalty terms based on target and disease"""
        penalties = []
        disease_enum = Disease(disease.value)
        penalty_configs = get_penalties_for_disease(disease_enum)
        
        # Check default penalties for this target
        for penalty_name in target_info.default_penalties:
            for config in penalty_configs:
                if config.name == penalty_name:
                    penalties.append(Penalty(
                        name=config.name,
                        severity=config.default_severity,
                        rationale=f"Known liability for {target_info.gene_name}",
                        evidence="Class-based or known liability",
                    ))
        
        # Safety-based penalties
        if scores.safety < 0.5:
            for config in penalty_configs:
                if "safety" in config.name.lower():
                    penalties.append(Penalty(
                        name=config.name,
                        severity=config.default_severity * (1 - scores.safety),
                        rationale="Low safety score indicates concern",
                        evidence="Safety dimension score",
                    ))
        
        return penalties


class DiseaseEngine:
    """
    Main engine for disease-to-target prioritization.
    """
    
    def __init__(self, config: Optional[ScoringEngineConfig] = None):
        self.scorer = TargetScorer(config)
        self.config = config or ScoringEngineConfig()
    
    def prioritize_targets(
        self,
        disease: DiseaseType,
        candidate_genes: Optional[List[str]] = None,
        disease_context: Optional[DiseaseContextData] = None,
        score_overrides: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> TargetPrioritizationResult:
        """
        Prioritize targets for a given disease.
        
        Args:
            disease: The disease type
            candidate_genes: List of gene names to evaluate (uses registry if None)
            disease_context: Optional disease context override
            score_overrides: Optional score overrides per gene
            
        Returns:
            TargetPrioritizationResult with ranked targets
        """
        start_time = time.time()
        
        # Get disease context
        ctx = disease_context or DISEASE_CONTEXTS.get(disease)
        
        # Get candidate genes from registry
        if candidate_genes is None:
            candidate_genes = list(TARGET_REGISTRY.get(disease.value, {}).keys())
        
        # Score each target
        dossiers = []
        for gene in candidate_genes:
            target_info = TARGET_REGISTRY.get(disease.value, {}).get(gene)
            
            if target_info is None:
                # Create a basic target info for unknown targets
                target_info = TargetInfo(
                    gene_name=gene,
                    protein_name=gene,
                    target_class=TargetClass.ENZYME,
                    is_extracellular=False,
                    is_liver_specific=False,
                    has_known_pocket=True,
                    has_degradation_logic=False,
                )
            
            # Get score overrides for this gene
            gene_overrides = score_overrides.get(gene) if score_overrides else None
            
            scores, penalties, priority_score = self.scorer.score_target(
                target_info=target_info,
                disease=disease,
                disease_context=ctx,
                score_overrides=gene_overrides,
            )
            
            # Calculate confidence
            confidence = self._calculate_confidence(scores, penalties)
            
            # Get recommended modalities
            modalities = self._get_recommended_modalities(target_info, disease, priority_score)
            
            # Create dossier
            dossier = TargetDossier(
                target_id=f"{gene}_{disease.value}",
                gene_name=gene,
                protein_name=target_info.protein_name,
                disease=disease,
                disease_context=ctx,
                scores=scores,
                penalties=penalties,
                priority_score=priority_score,
                confidence=confidence,
                recommended_modalities=modalities,
                target_class=target_info.target_class,
                is_extracellular=target_info.is_extracellular,
                is_liver_specific=target_info.is_liver_specific,
                has_known_pocket=target_info.has_known_pocket,
                has_degradation_logic=target_info.has_degradation_logic,
                status=Status.PRIORITIZED if priority_score >= self.config.min_priority_score else Status.DEPRIORITIZED,
                created_date=date.today(),
                last_updated=date.today(),
            )
            
            dossiers.append(dossier)
        
        # Sort by priority score
        dossiers.sort(key=lambda d: d.priority_score, reverse=True)
        
        # Assign ranks
        for i, dossier in enumerate(dossiers):
            dossier.rank = i + 1
        
        # Quality gate check
        quality_gate_passed = (
            len(dossiers) >= 5 and
            any(d.priority_score >= 0.70 for d in dossiers)
        )
        
        elapsed = time.time() - start_time
        
        return TargetPrioritizationResult(
            disease=disease,
            targets=dossiers[:self.config.max_targets_returned],
            total_candidates_evaluated=len(candidate_genes),
            scoring_time_seconds=elapsed,
            quality_gate_passed=quality_gate_passed,
        )
    
    def _calculate_confidence(self, scores: TargetScores, penalties: List[Penalty]) -> float:
        """Calculate confidence in the priority score"""
        # Base confidence from score variance
        score_values = [
            scores.genetic_causality,
            scores.disease_context,
            scores.perturbation_rescue,
            scores.tissue_specificity,
            scores.druggability,
            scores.safety,
            scores.translation,
            scores.competitive_novelty,
        ]
        
        # Low variance = higher confidence
        mean_score = sum(score_values) / len(score_values)
        variance = sum((s - mean_score) ** 2 for s in score_values) / len(score_values)
        score_confidence = 1 - min(variance * 2, 0.5)
        
        # Penalty reduces confidence
        penalty_reduction = sum(p.severity for p in penalties) / max(len(penalties), 1) * 0.2
        
        return max(0.3, min(0.95, score_confidence - penalty_reduction))
    
    def _get_recommended_modalities(
        self,
        target_info: TargetInfo,
        disease: DiseaseType,
        priority_score: float,
    ) -> List[str]:
        """Get recommended modalities for a target"""
        modalities = []
        
        # Get target class modality preferences
        class_key = target_info.target_class.value
        class_prefs = TARGET_CLASS_MODALITY.get(class_key, {})
        
        # Get disease modality preferences
        disease_enum = Disease(disease.value)
        disease_prefs = MODALITY_PREFERENCES.get(disease_enum, {})
        
        # Combine and score
        combined_scores = {}
        for modality, class_score in class_prefs.items():
            disease_score = disease_prefs.get(modality, 0.5)
            combined_scores[modality] = class_score * 0.6 + disease_score * 0.4
        
        # Sort and return top modalities
        sorted_modalities = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Return only those with score > 0.5
        modalities = [m for m, s in sorted_modalities if s > 0.5][:3]
        
        # Boost based on priority score
        if priority_score >= 0.80:
            # High priority - include all reasonable options
            modalities = [m for m, s in sorted_modalities if s > 0.4][:4]
        
        return modalities


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def prioritize_masld_targets(
    score_overrides: Optional[Dict[str, Dict[str, float]]] = None,
) -> TargetPrioritizationResult:
    """Convenience function for MASLD target prioritization"""
    engine = DiseaseEngine()
    return engine.prioritize_targets(
        disease=DiseaseType.MASLD,
        score_overrides=score_overrides or {},
    )


def prioritize_sarcopenia_targets(
    score_overrides: Optional[Dict[str, Dict[str, float]]] = None,
) -> TargetPrioritizationResult:
    """Convenience function for Sarcopenia target prioritization"""
    engine = DiseaseEngine()
    return engine.prioritize_targets(
        disease=DiseaseType.SARCOPENIA,
        score_overrides=score_overrides or {},
    )


def prioritize_lung_fibrosis_targets(
    score_overrides: Optional[Dict[str, Dict[str, float]]] = None,
) -> TargetPrioritizationResult:
    """Convenience function for Lung Fibrosis target prioritization"""
    engine = DiseaseEngine()
    return engine.prioritize_targets(
        disease=DiseaseType.LUNG_FIBROSIS,
        score_overrides=score_overrides or {},
    )
