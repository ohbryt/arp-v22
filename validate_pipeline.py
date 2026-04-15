#!/usr/bin/env python3
"""
ARP v22 - Pipeline Validation CI Gate

This script validates pipeline outputs against schemas and quality gates.
Run as part of CI/CD pipeline to ensure output quality.

Usage:
    python validate_pipeline.py --run-dir runs/2026-04-15_masld_run01
    python validate_pipeline.py --candidates candidates.parquet --manifest manifest.json
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent))

from schemas.definitions import (
    ManifestSchema,
    CandidateScoreSchema,
    CompoundSchema,
    validate_manifest,
    validate_candidate,
    validate_pipeline_output,
)


def load_candidates_from_parquet(filepath: str) -> List[CandidateScoreSchema]:
    """Load candidates from parquet file"""
    try:
        import pandas as pd
        df = pd.read_parquet(filepath)
        
        candidates = []
        for _, row in df.iterrows():
            try:
                # Build CompoundSchema from row
                compound_data = {}
                for field in ["compound_id", "inchi_key", "canonical_smiles"]:
                    if field in row and pd.notna(row[field]):
                        compound_data[field] = row[field]
                
                if compound_data:
                    compound = CompoundSchema(**compound_data)
                    
                    # Build CandidateScoreSchema from row
                    candidate_data = {
                        "candidate_id": row.get("candidate_id", str(row.name)),
                        "compound": compound,
                        "target": row.get("target", "unknown"),
                        "priority_score": row.get("priority_score", 0.0),
                    }
                    
                    # Optional fields
                    for opt_field in ["qsar_score", "docking_score", "dti_score", 
                                       "admet_score", "novelty_score"]:
                        if opt_field in row and pd.notna(row[opt_field]):
                            candidate_data[opt_field] = row[opt_field]
                    
                    candidates.append(CandidateScoreSchema(**candidate_data))
            except Exception:
                continue
        
        return candidates
    except ImportError:
        print("pandas/pyarrow not installed, skipping parquet loading")
        return []


def load_candidates_from_json(filepath: str) -> List[CandidateScoreSchema]:
    """Load candidates from JSON/JSONL file"""
    candidates = []
    
    if filepath.endswith(".jsonl"):
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    d = json.loads(line)
                    # Skip evidence entries (they have 'source', 'source_id', 'evidence_type' but no 'compound')
                    if "compound" not in d:
                        continue
                    # Convert dict to CandidateScoreSchema
                    if isinstance(d.get("compound"), dict):
                        d["compound"] = CompoundSchema(**d["compound"])
                    try:
                        candidates.append(CandidateScoreSchema(**d))
                    except (TypeError, KeyError) as e:
                        warnings.append(f"Skipping invalid candidate entry: {e}")
                        continue
    elif filepath.endswith(".json"):
        with open(filepath, "r") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if "compound" not in item:
                        continue
                    if isinstance(item.get("compound"), dict):
                        item["compound"] = CompoundSchema(**item["compound"])
                    try:
                        candidates.append(CandidateScoreSchema(**item))
                    except (TypeError, KeyError) as e:
                        warnings.append(f"Skipping invalid candidate entry: {e}")
                        continue
            elif isinstance(data, dict) and "compound" in data:
                if isinstance(data.get("compound"), dict):
                    data["compound"] = CompoundSchema(**data["compound"])
                try:
                    return [CandidateScoreSchema(**data)]
                except (TypeError, KeyError):
                    pass
    
    return candidates


def load_evidence_log(filepath: str) -> List[Dict]:
    """Load evidence from JSONL evidence log file (not candidates!)"""
    evidence = []
    
    if filepath.endswith(".jsonl"):
        with open(filepath, "r") as f:
            for line in f:
                if line.strip():
                    d = json.loads(line)
                    # Evidence logs typically have: source, source_id, evidence_type
                    # vs candidates which have: compound, target, priority_score
                    if "source" in d and "evidence_type" in d:
                        evidence.append(d)
    
    return evidence


def load_manifest(filepath: str) -> ManifestSchema:
    """Load manifest from JSON file"""
    return ManifestSchema.from_json(filepath)


def run_validation(run_dir: str) -> Dict[str, Any]:
    """Run validation on a complete pipeline run"""
    run_path = Path(run_dir)
    
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT: {run_dir}")
    print(f"{'='*60}\n")
    
    errors = []
    warnings = []
    
    # Check manifest
    manifest_path = run_path / "manifest.json"
    if not manifest_path.exists():
        errors.append(f"Manifest not found: {manifest_path}")
        manifest = None
    else:
        print("📋 Loading manifest...")
        try:
            manifest = load_manifest(str(manifest_path))
            manifest_valid, manifest_errors = validate_manifest(manifest)
            if manifest_valid:
                print(f"   ✅ Manifest valid")
                print(f"   Run ID: {manifest.run_id}")
                print(f"   Git commit: {manifest.git_commit}")
                print(f"   Data sources: {list(manifest.data_snapshots.keys())}")
            else:
                errors.extend([f"Manifest error: {e}" for e in manifest_errors])
        except Exception as e:
            errors.append(f"Failed to load manifest: {e}")
            manifest = None
    
    # Check candidates (in priority order)
    candidates_path = run_path / "candidates.parquet"
    candidates_json_path = run_path / "candidates.json"
    candidates_jsonl_path = run_path / "candidates.jsonl"
    evidence_jsonl_path = run_path / "evidence.jsonl"
    
    candidates = []
    
    # Note: evidence.jsonl is evidence logs, NOT candidates
    # Candidates should be in candidates.parquet, candidates.json, or candidates.jsonl
    if candidates_jsonl_path.exists():
        print("📋 Loading candidates from candidates.jsonl...")
        candidates = load_candidates_from_json(str(candidates_jsonl_path))
        print(f"   Loaded {len(candidates)} candidates")
    elif candidates_json_path.exists():
        print("📋 Loading candidates from candidates.json...")
        candidates = load_candidates_from_json(str(candidates_json_path))
        print(f"   Loaded {len(candidates)} candidates")
    elif candidates_path.exists():
        print("📋 Loading candidates from candidates.parquet...")
        candidates = load_candidates_from_parquet(str(candidates_path))
        print(f"   Loaded {len(candidates)} candidates")
    elif evidence_jsonl_path.exists():
        warnings.append("Found evidence.jsonl but no candidates file - evidence logs are not candidates")
        print("   ⚠️ Found evidence.jsonl but no candidates file")
    else:
        warnings.append("No candidates file found")
        print("   ⚠️ No candidates file found")
    
    # Check evidence log separately (if it exists)
    if evidence_jsonl_path.exists():
        print("📋 Loading evidence log (for reference)...")
        evidence = load_evidence_log(str(evidence_jsonl_path))
        print(f"   Found {len(evidence)} evidence entries")
    
    # Validate candidates
    if candidates:
        candidate_errors = []
        for i, candidate in enumerate(candidates):
            valid, errs = validate_candidate(candidate)
            if not valid:
                candidate_errors.extend([f"Candidate {i}: {e}" for e in errs])
        
        if candidate_errors:
            errors.extend(candidate_errors)
            print(f"   ❌ {len(candidate_errors)} candidate validation errors")
        else:
            print(f"   ✅ All {len(candidates)} candidates valid")
        
        # Check rank ordering
        ranks = [c.rank for c in candidates if c.rank is not None]
        if ranks and ranks != sorted(ranks):
            warnings.append("Candidates not properly ordered by rank")
        
        # Check fail reasons
        fail_without_reason = []
        for c in candidates:
            for fail in c.failed_filters:
                if fail not in c.fail_reasons:
                    fail_without_reason.append(f"{c.candidate_id}: {fail}")
        
        if fail_without_reason:
            warnings.append(f"{len(fail_without_reason)} failures without explanations")
    
    # Run full validation
    if manifest and candidates:
        print("\n📋 Running pipeline validation...")
        report = validate_pipeline_output(candidates, manifest)
        
        if report["valid"]:
            print("   ✅ Pipeline validation passed")
        else:
            errors.extend(report["errors"])
        
        warnings.extend(report.get("warnings", []))
        
        if "filter_summary" in report:
            print("   Filter summary:")
            for filter_name, count in report["filter_summary"].items():
                print(f"      - {filter_name}: {count}")
    
    # Check license metadata
    if manifest and not manifest.data_licenses:
        warnings.append("No license metadata in manifest")
    
    # Print summary
    print(f"\n{'='*60}")
    print("VALIDATION SUMMARY")
    print(f"{'='*60}")
    
    if errors:
        print(f"\n❌ VALIDATION FAILED ({len(errors)} errors)")
        for error in errors:
            print(f"   ERROR: {error}")
        return {"valid": False, "errors": errors, "warnings": warnings}
    
    if warnings:
        print(f"\n⚠️  VALIDATION PASSED WITH WARNINGS ({len(warnings)} warnings)")
        for warning in warnings:
            print(f"   WARNING: {warning}")
        return {"valid": True, "errors": [], "warnings": warnings, "warnings_count": len(warnings)}
    
    print("\n✅ VALIDATION PASSED")
    return {"valid": True, "errors": [], "warnings": []}


def validate_direct_files(candidates_path: str, manifest_path: str) -> Dict[str, Any]:
    """Validate directly specified candidates and manifest files"""
    print(f"\n{'='*60}")
    print(f"DIRECT FILE VALIDATION")
    print(f"{'='*60}\n")
    
    errors = []
    warnings = []
    
    # Load manifest
    print("📋 Loading manifest...")
    try:
        manifest = load_manifest(manifest_path)
        manifest_valid, manifest_errors = validate_manifest(manifest)
        if manifest_valid:
            print(f"   ✅ Manifest valid: {manifest.run_id}")
        else:
            errors.extend([f"Manifest: {e}" for e in manifest_errors])
            print(f"   ❌ Manifest errors: {len(manifest_errors)}")
    except Exception as e:
        errors.append(f"Failed to load manifest: {e}")
        manifest = None
    
    # Load candidates based on file extension
    candidates = []
    if candidates_path.endswith(".parquet"):
        print("📋 Loading candidates from parquet...")
        candidates = load_candidates_from_parquet(candidates_path)
    elif candidates_path.endswith(".jsonl"):
        print("📋 Loading candidates from JSONL...")
        candidates = load_candidates_from_json(candidates_path)
    elif candidates_path.endswith(".json"):
        print("📋 Loading candidates from JSON...")
        candidates = load_candidates_from_json(candidates_path)
    else:
        errors.append(f"Unsupported candidates file format: {candidates_path}")
    
    if candidates:
        print(f"   Loaded {len(candidates)} candidates")
        
        # Validate each candidate
        candidate_errors = []
        for i, candidate in enumerate(candidates):
            valid, errs = validate_candidate(candidate)
            if not valid:
                candidate_errors.extend([f"Candidate {i}: {e}" for e in errs])
        
        if candidate_errors:
            errors.extend(candidate_errors)
            print(f"   ❌ {len(candidate_errors)} validation errors")
        else:
            print(f"   ✅ All candidates valid")
    else:
        if not errors:
            warnings.append("No candidates loaded")
    
    # Print summary
    if errors:
        print(f"\n❌ VALIDATION FAILED ({len(errors)} errors)")
        for e in errors[:10]:
            print(f"   ERROR: {e}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more")
        return {"valid": False, "errors": errors, "warnings": warnings}
    elif warnings:
        print(f"\n⚠️  VALIDATION PASSED WITH WARNINGS")
        for w in warnings:
            print(f"   WARNING: {w}")
        return {"valid": True, "errors": [], "warnings": warnings}
    else:
        print(f"\n✅ VALIDATION PASSED")
        return {"valid": True, "errors": [], "warnings": []}


def main():
    parser = argparse.ArgumentParser(description="Validate ARP v22 pipeline outputs")
    parser.add_argument("--run-dir", help="Pipeline run directory")
    parser.add_argument("--candidates", help="Candidates file (parquet/json)")
    parser.add_argument("--manifest", help="Manifest file")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    
    args = parser.parse_args()
    
    if args.run_dir:
        result = run_validation(args.run_dir)
    elif args.candidates and args.manifest:
        result = validate_direct_files(args.candidates, args.manifest)
    else:
        parser.print_help()
        sys.exit(1)
    
    if args.strict and result.get("warnings"):
        sys.exit(1)
    elif not result.get("valid"):
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
