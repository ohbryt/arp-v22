"""
ARP v22 - Schema Definitions

JSON Schema definitions for data contracts.
These schemas are used to validate all pipeline inputs/outputs.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum
import json
import hashlib


# ============================================================================
# ENUMS
# ============================================================================

class DataSource(Enum):
    CHEMBL = "chembl"
    PUBCHEM = "pubchem"
    UNIPROT = "uniprot"
    ENSEMBL = "ensembl"
    ALPHAFOLD = "alphafold"
    PDB = "pdb"
    OPEN_TARGETS = "open_targets"
    GWAS_CATALOG = "gwas_catalog"
    DRUGBANK = "drugbank"
    INTERNAL = "internal"


class LicenseType(Enum):
    CC_BY_SA_30 = "CC BY-SA 3.0"
    CC_BY_40 = "CC BY 4.0"
    CC0_10 = "CC0 1.0"
    APACHE_20 = "Apache 2.0"
    PROPRIETARY = "proprietary"
    PUBLIC_DOMAIN = "public_domain"


class DeterminismLevel(Enum):
    FULL = "full"           # Completely deterministic
    PARTIAL = "partial"     # Some stochastic elements
    NON_DETERMINISTIC = "non_deterministic"  # Random sampling, etc.


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class DataSourceInfo:
    """Information about a data source used in the pipeline"""
    source: str
    version: str                    # e.g., "34" for ChEMBL 34
    license: str
    access_date: str                # ISO date
    url: Optional[str] = None
    citation: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class EvidenceItem:
    """A single piece of evidence supporting a finding"""
    evidence_id: str
    source: str                      # e.g., "chembl", "pubmed"
    source_id: str                   # e.g., PMID, ChEMBL ID
    evidence_type: str               # "bioactivity", "genetic_association", etc.
    value: Any                       # The actual evidence value
    unit: Optional[str] = None
    p_value: Optional[float] = None
    direction: Optional[str] = None  # "positive", "negative", "neutral"
    confidence: Optional[float] = None  # 0-1
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TargetSchema:
    """Schema for a drug target"""
    target_id: str                  # Internal canonical ID (e.g., "THRB_HUMAN")
    gene_name: str                  # Gene symbol (e.g., "THRB")
    uniprot_id: str                 # UniProt accession (e.g., "P10828")
    protein_name: str               # Protein name
    target_class: str = "unknown"   # e.g., "nuclear_receptor", "kinase"
    ensembl_id: Optional[str] = None
    priority_score: float = 0.0     # 0-1
    confidence: float = 0.0        # 0-1
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    
    # Evidence
    evidence: List[EvidenceItem] = field(default_factory=list)
    
    # Data sources
    data_sources: List[DataSourceInfo] = field(default_factory=list)
    
    # Validation
    schema_version: str = "1.0"
    validated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["validated_at"] = datetime.now().isoformat()
        return d
    
    def validate(self) -> bool:
        """Basic validation of required fields"""
        required = ["target_id", "gene_name", "uniprot_id", "protein_name", "priority_score"]
        for field in required:
            if not getattr(self, field, None):
                return False
        return True


@dataclass
class CompoundSchema:
    """Schema for a chemical compound"""
    compound_id: str                 # Internal canonical ID (e.g., "INCHIKEY:XXXXX")
    inchi_key: str                  # Standard InChIKey
    canonical_smiles: str             # Canonical SMILES
    
    # Names/IDs
    names: List[str] = field(default_factory=list)
    chembl_id: Optional[str] = None
    pubchem_cid: Optional[str] = None
    drugbank_id: Optional[str] = None
    
    # Properties
    molecular_weight: Optional[float] = None
    logp: Optional[float] = None
    tpsa: Optional[float] = None
    hbd: int = 0
    hba: int = 0
    num_rotatable_bonds: int = 0
    num_aromatic_rings: int = 0
    fsp3: Optional[float] = None
    
    # Quality flags
    pains_flags: List[str] = field(default_factory=list)
    structural_alerts: List[str] = field(default_factory=list)
    validity_check: str = "unknown"   # "valid", "invalid", "unknown"
    
    # Data sources
    data_sources: List[DataSourceInfo] = field(default_factory=list)
    
    # Validation
    schema_version: str = "1.0"
    validated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["validated_at"] = datetime.now().isoformat()
        return d
    
    def validate(self) -> bool:
        """Basic validation of compound"""
        if not self.inchi_key or len(self.inchi_key) != 27:
            return False
        if self.inchi_key.count("-") != 2:
            return False
        return True
    
    @staticmethod
    def generate_id_from_smiles(smiles: str) -> str:
        """Generate a deterministic ID from SMILES"""
        return hashlib.md5(smiles.encode()).hexdigest()[:16].upper()


@dataclass
class AssaySchema:
    """Schema for assay results"""
    assay_id: str
    assay_name: str
    assay_type: str                  # "binding", "functional", "cell_based", etc.
    target_id: str                  # Link to target
    source: str
    source_id: str
    
    # Conditions
    species: str = "human"
    tissue: Optional[str] = None
    cell_line: Optional[str] = None
    
    # Results
    activity_value: Optional[float] = None
    activity_type: Optional[str] = None  # "IC50", "Ki", "Kd", "EC50", etc.
    unit: Optional[str] = None
    
    # Quality
    quality_flags: List[str] = field(default_factory=list)
    z_factor: Optional[float] = None
    data_sources: List[DataSourceInfo] = field(default_factory=list)
    
    schema_version: str = "1.0"
    validated_at: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["validated_at"] = datetime.now().isoformat()
        return d


@dataclass
class CandidateScoreSchema:
    """Schema for a candidate compound with scores"""
    candidate_id: str                # UUID
    compound: CompoundSchema
    target: str
    
    # Scores
    priority_score: float            # Overall composite score
    qsar_score: Optional[float] = None
    docking_score: Optional[float] = None
    dti_score: Optional[float] = None
    admet_score: Optional[float] = None
    novelty_score: Optional[float] = None
    synthetic_accessibility_score: Optional[float] = None
    
    # Score breakdown
    dimension_scores: Dict[str, float] = field(default_factory=dict)
    
    # Filters
    passed_filters: List[str] = field(default_factory=list)
    failed_filters: List[str] = field(default_factory=list)
    fail_reasons: Dict[str, str] = field(default_factory=dict)
    
    # Evidence
    evidence: List[EvidenceItem] = field(default_factory=list)
    
    # Provenance
    data_sources: List[DataSourceInfo] = field(default_factory=list)
    determinism_level: str = "partial"
    
    # Metadata
    rank: Optional[int] = None
    pipeline_version: str = "1.0"
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        d = {
            "candidate_id": self.candidate_id,
            "compound": self.compound.to_dict() if isinstance(self.compound, CompoundSchema) else self.compound,
            "target": self.target,
            "priority_score": self.priority_score,
            "qsar_score": self.qsar_score,
            "docking_score": self.docking_score,
            "dti_score": self.dti_score,
            "admet_score": self.admet_score,
            "novelty_score": self.novelty_score,
            "synthetic_accessibility_score": self.synthetic_accessibility_score,
            "dimension_scores": self.dimension_scores,
            "passed_filters": self.passed_filters,
            "failed_filters": self.failed_filters,
            "fail_reasons": self.fail_reasons,
            "evidence": [e.to_dict() for e in self.evidence],
            "data_sources": [ds.to_dict() for ds in self.data_sources],
            "determinism_level": self.determinism_level,
            "rank": self.rank,
            "pipeline_version": self.pipeline_version,
            "generated_at": self.generated_at,
        }
        return d


@dataclass
class ManifestSchema:
    """Schema for pipeline run manifest"""
    run_id: str
    git_commit: str
    python_version: str
    environment_hash: str           # Hash of requirements/environment
    
    # Optional fields
    git_branch: Optional[str] = None
    container_image: Optional[str] = None
    
    # Data snapshots
    data_snapshots: Dict[str, str] = field(default_factory=dict)  # source -> DVC hash or version
    
    # Models
    models: Dict[str, str] = field(default_factory=dict)  # model_name -> version/hash
    
    # Parameters
    params: Dict[str, Any] = field(default_factory=dict)
    
    # Results summary
    total_candidates: int = 0
    top_candidates_file: Optional[str] = None
    evidence_file: Optional[str] = None
    
    # License compliance
    data_licenses: Dict[str, str] = field(default_factory=dict)  # source -> license
    
    # Quality
    schema_validation_passed: bool = True
    determinism_level: str = "partial"
    
    # Timestamps
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    schema_version: str = "1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["completed_at"] = datetime.now().isoformat()
        return d
    
    def to_json(self, filepath: str):
        """Save manifest to JSON file"""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def from_json(cls, filepath: str) -> "ManifestSchema":
        """Load manifest from JSON file"""
        with open(filepath, "r") as f:
            d = json.load(f)
        return cls(**d)
    
    def generate_run_id(cls, disease: str, date_str: Optional[str] = None) -> str:
        """Generate a deterministic run ID"""
        if date_str is None:
            date_str = datetime.now().strftime("%Y-%m-%d")
        hash_input = f"{disease}_{date_str}_{datetime.now().microsecond}"
        short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"{date_str}_{disease}_{short_hash}"


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_manifest(manifest: ManifestSchema) -> tuple[bool, List[str]]:
    """Validate a manifest for required fields"""
    errors = []
    
    required = ["run_id", "git_commit", "python_version", "environment_hash"]
    for field in required:
        if not getattr(manifest, field, None):
            errors.append(f"Missing required field: {field}")
    
    if manifest.data_snapshots:
        for source, version in manifest.data_snapshots.items():
            if not version:
                errors.append(f"Empty version for data source: {source}")
    
    return len(errors) == 0, errors


def validate_candidate(candidate: CandidateScoreSchema) -> tuple[bool, List[str]]:
    """Validate a candidate for required fields and quality gates"""
    errors = []
    
    # Required fields
    if not candidate.candidate_id:
        errors.append("Missing candidate_id")
    if not candidate.compound:
        errors.append("Missing compound")
    if not candidate.target:
        errors.append("Missing target")
    
    # Compound validation
    if isinstance(candidate.compound, CompoundSchema):
        if not candidate.compound.validate():
            errors.append("Invalid compound structure")
    
    # Score validation
    if candidate.priority_score < 0 or candidate.priority_score > 1:
        errors.append(f"Priority score out of range: {candidate.priority_score}")
    
    # Fail reasons should have explanations
    for fail in candidate.failed_filters:
        if fail not in candidate.fail_reasons:
            errors.append(f"Failed filter '{fail}' missing reason")
    
    return len(errors) == 0, errors


def validate_pipeline_output(
    candidates: List[CandidateScoreSchema],
    manifest: ManifestSchema,
) -> Dict[str, Any]:
    """
    Validate the complete pipeline output.
    Returns a validation report.
    """
    report = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "candidate_count": len(candidates),
        "manifest_valid": False,
        "schema_validation_passed": True,
    }
    
    # Validate manifest
    manifest_valid, manifest_errors = validate_manifest(manifest)
    report["manifest_valid"] = manifest_valid
    if not manifest_valid:
        report["valid"] = False
        report["errors"].extend([f"Manifest: {e}" for e in manifest_errors])
    
    # Validate candidates
    for i, candidate in enumerate(candidates):
        valid, errors = validate_candidate(candidate)
        if not valid:
            report["valid"] = False
            report["errors"].extend([f"Candidate {i} ({candidate.candidate_id}): {e}" for e in errors])
    
    # Check quality gates
    if len(candidates) == 0:
        report["warnings"].append("No candidates generated")
    
    failed_counts = {}
    for c in candidates:
        for fail in c.failed_filters:
            failed_counts[fail] = failed_counts.get(fail, 0) + 1
    
    if failed_counts:
        report["filter_summary"] = failed_counts
    
    return report
