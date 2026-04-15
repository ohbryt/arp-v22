"""
Data Schemas for ARP v22
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import date
from enum import Enum


class DiseaseType(Enum):
    MASLD = "masld"
    SARCOPENIA = "sarcopenia"
    LUNG_FIBROSIS = "lung_fibrosis"
    HEART_FAILURE = "heart_failure"
    CANCER = "cancer"


class ModalityType(Enum):
    SMALL_MOLECULE = "small_molecule"
    BIOLOGIC = "biologic"
    PEPTIDE = "peptide"
    OLIGO = "oligo"
    ANTIBODY = "antibody"
    ADC = "adc"
    DEGRADER = "degrader"
    INHALED = "inhaled"
    CELL_THERAPY = "cell_therapy"


class TargetClass(Enum):
    KINASE = "kinase"
    NUCLEAR_RECEPTOR = "nuclear_receptor"
    GPCR = "gpc_receptor"
    TRANSPORTER = "transporter"
    ENZYME = "enzyme"
    TRANSCRIPTION_FACTOR = "transcription_factor"
    EXTRACELLULAR_LIGAND = "extracellular_ligand"
    ION_CHANNEL = "ion_channel"
    CELL_SURFACE_ANTIGEN = "cell_surface_antigen"


class Status(Enum):
    PRIORITIZED = "prioritized"
    REJECTED = "rejected"
    DEPRIORITIZED = "deprioritized"
    ACTIVE = "active"
    TERMINATED = "terminated"


# ============================================================================
# TARGET SCORING SCHEMA
# ============================================================================

@dataclass
class TargetScores:
    """8-dimensional scoring for a target"""
    genetic_causality: float = 0.0   # 0-1
    disease_context: float = 0.0      # 0-1
    perturbation_rescue: float = 0.0  # 0-1
    tissue_specificity: float = 0.0   # 0-1
    druggability: float = 0.0         # 0-1
    safety: float = 0.0               # 0-1
    translation: float = 0.0          # 0-1
    competitive_novelty: float = 0.0   # 0-1
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "genetic_causality": self.genetic_causality,
            "disease_context": self.disease_context,
            "perturbation_rescue": self.perturbation_rescue,
            "tissue_specificity": self.tissue_specificity,
            "druggability": self.druggability,
            "safety": self.safety,
            "translation": self.translation,
            "competitive_novelty": self.competitive_novelty,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> "TargetScores":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Penalty:
    """Penalty applied to target score"""
    name: str
    severity: float  # 0-1 (higher = more severe)
    rationale: str
    evidence: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "severity": self.severity,
            "rationale": self.rationale,
            "evidence": self.evidence,
        }


@dataclass
class DiseaseContextData:
    """Disease-specific context for target"""
    disease: DiseaseType
    subtype: Optional[str] = None
    stage: Optional[str] = None
    primary_axis: Optional[str] = None  # e.g., "fibrosis", "inflammation"
    secondary_axes: List[str] = field(default_factory=list)
    tissue_focus: List[str] = field(default_factory=list)  # e.g., ["hepatocyte", "stellate"]
    patient_population: Optional[str] = None


@dataclass
class EvidenceSource:
    """Evidence supporting a score dimension"""
    source_type: str  # "gwas", "crispr", "literature", "clinical_trial"
    identifier: str   # PubMed ID, NCT number, etc.
    relevance: str
    strength: float = 0.5  # 0-1


@dataclass
class BiomarkerInfo:
    """Biomarker information"""
    name: str
    type: str  # "diagnostic", "prognostic", "predictive", "pharmacodynamic"
    sample_type: str
    assay_method: str
    status: str  # "validated", "exploratory"


@dataclass
class AssayRecommendation:
    """Recommended assay for target validation"""
    assay_name: str
    assay_type: str
    readout: str
    gold_standard: bool = False
    development_status: str = "established"


@dataclass
class TargetDossier:
    """Complete target dossier"""
    target_id: str
    gene_name: str
    protein_name: Optional[str] = None
    disease: Optional[DiseaseType] = None
    disease_context: Optional[DiseaseContextData] = None
    
    # Scores
    scores: Optional[TargetScores] = None
    penalties: List[Penalty] = field(default_factory=list)
    priority_score: float = 0.0
    confidence: float = 0.0
    
    # Evidence
    evidence: Dict[str, List[EvidenceSource]] = field(default_factory=dict)
    
    # Recommendations
    recommended_modalities: List[str] = field(default_factory=list)
    assay_recommendations: List[AssayRecommendation] = field(default_factory=list)
    biomarkers: List[BiomarkerInfo] = field(default_factory=list)
    
    # Metadata
    rank: Optional[int] = None
    status: Status = Status.PRIORITIZED
    created_date: Optional[date] = None
    last_updated: Optional[date] = None
    
    # Target properties
    target_class: Optional[TargetClass] = None
    is_extracellular: bool = False
    is_liver_specific: bool = False
    has_known_pocket: bool = False
    has_degradation_logic: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_id": self.target_id,
            "gene_name": self.gene_name,
            "protein_name": self.protein_name,
            "disease": self.disease.value if self.disease else None,
            "scores": self.scores.to_dict() if self.scores else {},
            "penalties": [p.to_dict() for p in self.penalties],
            "priority_score": round(self.priority_score, 3),
            "confidence": round(self.confidence, 2),
            "recommended_modalities": self.recommended_modalities,
            "rank": self.rank,
            "status": self.status.value,
            "target_class": self.target_class.value if self.target_class else None,
            "biomarkers": [
                {"name": b.name, "type": b.type, "status": b.status}
                for b in self.biomarkers
            ],
        }


# ============================================================================
# TARGET PRIORITIZATION RESULT
# ============================================================================

@dataclass
class TargetPrioritizationResult:
    """Result from running target prioritization"""
    disease: DiseaseType
    targets: List[TargetDossier]
    total_candidates_evaluated: int
    scoring_time_seconds: float
    quality_gate_passed: bool
    
    def get_top_targets(self, n: int = 10) -> List[TargetDossier]:
        """Get top N targets by priority score"""
        sorted_targets = sorted(self.targets, key=lambda t: t.priority_score, reverse=True)
        return sorted_targets[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "disease": self.disease.value,
            "total_evaluated": self.total_candidates_evaluated,
            "targets_returned": len(self.targets),
            "top_10": [
                {"gene": t.gene_name, "score": t.priority_score, "rank": t.rank}
                for t in self.get_top_targets(10)
            ],
            "quality_gate_passed": self.quality_gate_passed,
            "scoring_time_seconds": round(self.scoring_time_seconds, 2),
        }


# ============================================================================
# DISEASE PACK INTERFACE
# ============================================================================

@dataclass
class DiseasePackConfig:
    """Configuration for a disease pack"""
    disease: DiseaseType
    name: str
    description: str
    subtypes: List[str]
    stages: List[str]
    priority_targets: List[str]  # Gene names
    data_sources: List[str]
    tissue_focus: List[str]
    key_pathways: List[str]


# ============================================================================
# SCORING ENGINE CONFIG
# ============================================================================

@dataclass
class ScoringEngineConfig:
    """Configuration for the scoring engine"""
    min_priority_score: float = 0.50
    min_confidence: float = 0.60
    require_genetic_evidence: bool = False
    require_perturbation_evidence: bool = True
    penalty_severity_threshold: float = 0.30
    max_targets_returned: int = 50
    tissue_specificity_required: bool = True
    weight_override: Optional[Dict[str, float]] = None
