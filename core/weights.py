"""
Disease-Specific Weight Configurations for ARP v22

Each disease has a unique weight matrix for the 8 scoring dimensions.
Weights sum to 1.0 for each disease.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
from enum import Enum


class Disease(Enum):
    MASLD = "masld"
    SARCOPENIA = "sarcopenia"
    LUNG_FIBROSIS = "lung_fibrosis"
    HEART_FAILURE = "heart_failure"
    CANCER = "cancer"
    GENERIC = "generic"


class Modality(Enum):
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    OLIGO = "oligo"
    ANTIBODY = "antibody"
    ADC = "adc"
    DEGRADER = "degrader"
    INHALED = "inhaled"
    CELL_THERAPY = "cell_therapy"


@dataclass
class WeightConfig:
    """Weight configuration for a single scoring dimension"""
    genetic_causality: float = 0.10
    disease_context: float = 0.15
    perturbation_rescue: float = 0.20
    tissue_specificity: float = 0.10
    druggability: float = 0.10
    safety: float = 0.15
    translation: float = 0.10
    competitive_novelty: float = 0.10

    def validate(self) -> bool:
        """Ensure weights sum to 1.0"""
        total = (
            self.genetic_causality
            + self.disease_context
            + self.perturbation_rescue
            + self.tissue_specificity
            + self.druggability
            + self.safety
            + self.translation
            + self.competitive_novelty
        )
        return abs(total - 1.0) < 0.001


# ============================================================================
# DISEASE-SPECIFIC WEIGHT CONFIGURATIONS
# ============================================================================

DISEASE_WEIGHTS: Dict[Disease, WeightConfig] = {
    Disease.MASLD: WeightConfig(
        genetic_causality=0.05,
        disease_context=0.25,      # Hepatocyte + stellate + Kupffer
        perturbation_rescue=0.15,
        tissue_specificity=0.20,  # Liver/hepatocyte selectivity critical
        druggability=0.10,
        safety=0.20,             # Chronic metabolic disease
        translation=0.05,
        competitive_novelty=0.00,
    ),
    
    Disease.SARCOPENIA: WeightConfig(
        genetic_causality=0.05,
        disease_context=0.15,     # Anabolism vs catabolism
        perturbation_rescue=0.25, # Functional rescue paramount
        tissue_specificity=0.20,  # Skeletal muscle selectivity
        druggability=0.10,
        safety=0.20,             # Chronic geriatric dosing
        translation=0.05,
        competitive_novelty=0.00,
    ),
    
    Disease.LUNG_FIBROSIS: WeightConfig(
        genetic_causality=0.05,
        disease_context=0.25,     # Fibroblast vs epithelial
        perturbation_rescue=0.20,
        tissue_specificity=0.15,  # Lung selectivity, inhaled option
        druggability=0.10,
        safety=0.15,             # Wound healing liability
        translation=0.10,
        competitive_novelty=0.00,
    ),
    
    Disease.HEART_FAILURE: WeightConfig(
        genetic_causality=0.05,
        disease_context=0.20,     # HFrEF vs HFpEF context
        perturbation_rescue=0.20,  # Reverse remodeling
        tissue_specificity=0.10,
        druggability=0.05,
        safety=0.25,             # QT/hERG, hemodynamic
        translation=0.15,         # BNP, imaging biomarkers
        competitive_novelty=0.00,
    ),
    
    Disease.CANCER: WeightConfig(
        genetic_causality=0.20,   # Driver oncogene dependency
        disease_context=0.20,      # Subtype-specific
        perturbation_rescue=0.20, # CRISPR dependency
        tissue_specificity=0.00,
        druggability=0.05,
        safety=0.15,             # Therapeutic window
        translation=0.15,         # Patient stratification
        competitive_novelty=0.05,
    ),
    
    Disease.GENERIC: WeightConfig(
        genetic_causality=0.15,
        disease_context=0.15,
        perturbation_rescue=0.20,
        tissue_specificity=0.10,
        druggability=0.15,
        safety=0.15,
        translation=0.05,
        competitive_novelty=0.05,
    ),
}


# ============================================================================
# PENALTY DEFINITIONS PER DISEASE
# ============================================================================

@dataclass
class PenaltyConfig:
    name: str
    description: str
    default_severity: float  # 0-1
    applicable_diseases: List[Disease]


DISEASE_PENALTIES: Dict[Disease, List[PenaltyConfig]] = {
    Disease.MASLD: [
        PenaltyConfig(
            name="dyslipidemia_worsening",
            description="Worsening blood lipid profile",
            default_severity=0.15,
            applicable_diseases=[Disease.MASLD],
        ),
        PenaltyConfig(
            name="hypertriglyceridemia",
            description="Elevated triglycerides",
            default_severity=0.10,
            applicable_diseases=[Disease.MASLD],
        ),
        PenaltyConfig(
            name="weight_gain",
            description="Unwanted weight gain",
            default_severity=0.10,
            applicable_diseases=[Disease.MASLD],
        ),
        PenaltyConfig(
            name="hepatotoxicity",
            description="Drug-induced liver injury",
            default_severity=0.20,
            applicable_diseases=[Disease.MASLD],
        ),
        PenaltyConfig(
            name="steatosis_only",
            description="Reduces fat but not inflammation/fibrosis",
            default_severity=0.10,
            applicable_diseases=[Disease.MASLD],
        ),
    ],
    
    Disease.SARCOPENIA: [
        PenaltyConfig(
            name="systemic_anabolic_liability",
            description="Off-target anabolic effects",
            default_severity=0.15,
            applicable_diseases=[Disease.SARCOPENIA],
        ),
        PenaltyConfig(
            name="tumor_growth_concern",
            description="Potential to promote cancer",
            default_severity=0.20,
            applicable_diseases=[Disease.SARCOPENIA, Disease.CANCER],
        ),
        PenaltyConfig(
            name="cardiac_adverse_effects",
            description="Cardiovascular side effects",
            default_severity=0.10,
            applicable_diseases=[Disease.SARCOPENIA, Disease.HEART_FAILURE],
        ),
        PenaltyConfig(
            name="neuromuscular_mismatch",
            description="Disconnection between muscle building and function",
            default_severity=0.10,
            applicable_diseases=[Disease.SARCOPENIA],
        ),
        PenaltyConfig(
            name="immunosuppression",
            description="Immune system suppression",
            default_severity=0.15,
            applicable_diseases=[Disease.SARCOPENIA],
        ),
    ],
    
    Disease.LUNG_FIBROSIS: [
        PenaltyConfig(
            name="wound_healing_inhibition",
            description="Impairing tissue repair",
            default_severity=0.20,
            applicable_diseases=[Disease.LUNG_FIBROSIS],
        ),
        PenaltyConfig(
            name="epithelial_regeneration_impairment",
            description="Preventing lung epithelial repair",
            default_severity=0.20,
            applicable_diseases=[Disease.LUNG_FIBROSIS],
        ),
        PenaltyConfig(
            name="systemic_immunosuppression",
            description="Broad immune suppression",
            default_severity=0.15,
            applicable_diseases=[Disease.LUNG_FIBROSIS],
        ),
        PenaltyConfig(
            name="vascular_pulmonary_tox",
            description="Pulmonary vascular toxicity",
            default_severity=0.10,
            applicable_diseases=[Disease.LUNG_FIBROSIS],
        ),
    ],
    
    Disease.HEART_FAILURE: [
        PenaltyConfig(
            name="qtc_herg_risk",
            description="QT prolongation, arrhythmia risk",
            default_severity=0.20,
            applicable_diseases=[Disease.HEART_FAILURE],
        ),
        PenaltyConfig(
            name="contractility_worsening",
            description="Negative inotropic effect",
            default_severity=0.15,
            applicable_diseases=[Disease.HEART_FAILURE],
        ),
        PenaltyConfig(
            name="renal_hemodynamic_instability",
            description="Kidney function deterioration",
            default_severity=0.15,
            applicable_diseases=[Disease.HEART_FAILURE],
        ),
        PenaltyConfig(
            name="pro_arrhythmia",
            description="Pro-arrhythmic potential",
            default_severity=0.20,
            applicable_diseases=[Disease.HEART_FAILURE],
        ),
        PenaltyConfig(
            name="excessive_fibrosis_blockade",
            description="Blocking necessary tissue repair",
            default_severity=0.10,
            applicable_diseases=[Disease.HEART_FAILURE, Disease.LUNG_FIBROSIS],
        ),
    ],
    
    Disease.CANCER: [
        PenaltyConfig(
            name="pan_essential_gene",
            description="Essential in normal tissues",
            default_severity=0.25,
            applicable_diseases=[Disease.CANCER],
        ),
        PenaltyConfig(
            name="poor_normal_tissue_window",
            description="Narrow therapeutic window",
            default_severity=0.20,
            applicable_diseases=[Disease.CANCER],
        ),
        PenaltyConfig(
            name="resistance_bypass_likely",
            description="Cancer will likely bypass mechanism",
            default_severity=0.15,
            applicable_diseases=[Disease.CANCER],
        ),
        PenaltyConfig(
            name="crowded_target",
            description="No differentiation path",
            default_severity=0.10,
            applicable_diseases=[Disease.CANCER],
        ),
    ],
}


# ============================================================================
# MODALITY PREFERENCES PER DISEASE
# ============================================================================

MODALITY_PREFERENCES: Dict[Disease, Dict[str, float]] = {
    Disease.MASLD: {
        "small_molecule": 0.90,
        "liver_targeted_oligo": 0.80,
        "peptide_analog": 0.60,
        "biologic": 0.50,
        "inhaled": 0.10,
    },
    
    Disease.SARCOPENIA: {
        "biologic": 0.85,
        "peptide": 0.80,
        "small_molecule": 0.70,
        "oligo": 0.50,
        "inhaled": 0.10,
    },
    
    Disease.LUNG_FIBROSIS: {
        "inhaled_small_molecule": 0.90,
        "small_molecule": 0.80,
        "biologic": 0.70,
        "antibody": 0.65,
        "oligo": 0.30,
    },
    
    Disease.HEART_FAILURE: {
        "small_molecule": 0.90,
        "biologic": 0.70,
        "antibody": 0.65,
        "oligo": 0.40,
    },
    
    Disease.CANCER: {
        "small_molecule": 0.85,
        "degrader": 0.80,
        "antibody": 0.75,
        "adc": 0.70,
        "biologic": 0.60,
        "cell_therapy": 0.50,
    },
}


# ============================================================================
# TARGET CLASS TO MODALITY MAPPING
# ============================================================================

TARGET_CLASS_MODALITY: Dict[str, Dict[str, float]] = {
    "extracellular_ligand_receptor": {
        "biologic": 0.95,
        "peptide": 0.85,
        "small_molecule": 0.40,
    },
    "kinase_enzyme": {
        "small_molecule": 0.90,
        "biologic": 0.50,
        "degrader": 0.60,
    },
    "transcription_factor": {
        "oligo": 0.75,
        "degrader": 0.70,
        "small_molecule": 0.40,
        "indirect_small_molecule": 0.65,
    },
    "nuclear_receptor": {
        "small_molecule": 0.95,
        "peptide": 0.30,
    },
    "gpc_receptor": {
        "small_molecule": 0.85,
        "peptide": 0.75,
        "biologic": 0.60,
    },
    "transporter": {
        "small_molecule": 0.90,
    },
    "ion_channel": {
        "small_molecule": 0.90,
    },
    "myostatin_axis": {
        "antibody": 0.95,
        "ligand_trap": 0.90,
        "peptide": 0.70,
    },
    "cell_surface_antigen": {
        "antibody": 0.95,
        "adc": 0.90,
    },
    "synthetic_lethality": {
        "small_molecule": 0.80,
        "degrader": 0.75,
    },
}


def get_disease_weights(disease: Disease) -> WeightConfig:
    """Get weight configuration for a disease"""
    return DISEASE_WEIGHTS.get(disease, DISEASE_WEIGHTS[Disease.GENERIC])


def get_modality_score(disease: Disease, modality: str) -> float:
    """Get modality preference score for a disease"""
    prefs = MODALITY_PREFERENCES.get(disease, {})
    return prefs.get(modality, 0.5)


def get_penalties_for_disease(disease: Disease) -> List[PenaltyConfig]:
    """Get applicable penalties for a disease"""
    return DISEASE_PENALTIES.get(disease, [])
