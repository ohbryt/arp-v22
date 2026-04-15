"""
ARP v22 - JSON Schemas for Data Contracts

These schemas define the data contract for each module in the pipeline.
All outputs should pass schema validation before being passed to the next stage.
"""

from .definitions import (
    TargetSchema,
    CompoundSchema,
    AssaySchema,
    CandidateScoreSchema,
    EvidenceItem,
    DataSourceInfo,
    ManifestSchema,
    validate_manifest,
    validate_candidate,
    validate_pipeline_output,
)

__all__ = [
    "TargetSchema",
    "CompoundSchema",
    "AssaySchema",
    "CandidateScoreSchema",
    "EvidenceItem",
    "DataSourceInfo",
    "ManifestSchema",
    "validate_manifest",
    "validate_candidate",
    "validate_pipeline_output",
]
