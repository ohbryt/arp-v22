#!/usr/bin/env python3
"""
ARP v22 - CLI Entry Point

Usage:
    python cli.py masld
    python cli.py sarcopenia
    python cli.py lung-fibrosis
    python cli.py --list-diseases
    python cli.py --list-targets masld
"""

import argparse
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core import TargetScorer, DiseaseEngine
from core.schema import DiseaseType, ScoringEngineConfig
from core.weights import DISEASE_WEIGHTS, Disease
from disease_packs.masld import MASLDTargets, get_masld_ontology
from disease_packs.sarcopenia import SarcopeniaTargets, get_sarcopenia_ontology


DISEASE_MAP = {
    "masld": DiseaseType.MASLD,
    "sarcopenia": DiseaseType.SARCOPENIA,
    "lung_fibrosis": DiseaseType.LUNG_FIBROSIS,
    "lung-fibrosis": DiseaseType.LUNG_FIBROSIS,
    "heart_failure": DiseaseType.HEART_FAILURE,
    "heart-failure": DiseaseType.HEART_FAILURE,
    "cancer": DiseaseType.CANCER,
}


def list_diseases():
    """List all available diseases"""
    print("\n📋 Available Diseases in ARP v22:")
    print("-" * 50)
    for disease in DiseaseType:
        weights = DISEASE_WEIGHTS.get(Disease(disease.value))
        print(f"\n  {disease.value.upper()}")
        if weights:
            print(f"    Primary weights:")
            print(f"      - Disease Context: {weights.disease_context:.0%}")
            print(f"      - Perturbation Rescue: {weights.perturbation_rescue:.0%}")
            print(f"      - Safety: {weights.safety:.0%}")
            print(f"      - Tissue Specificity: {weights.tissue_specificity:.0%}")
    print("\n")


def list_targets(disease_name: str):
    """List all targets for a disease"""
    disease_key = disease_name.lower().replace("-", "_")
    
    print(f"\n🎯 Targets for {disease_name.upper()}")
    print("-" * 60)
    
    if disease_key == "masld":
        targets = MASLDTargets.get_all_masld_targets()
        for gene, config in targets.items():
            print(f"\n  {gene} ({config.protein_name})")
            print(f"    Evidence Level: {config.evidence_level}")
            print(f"    Priority Score: {config.priority_score:.3f}")
            print(f"    Key Axes: steatosis={config.steatosis_relevance:.2f}, "
                  f"inflammation={config.inflammation_relevance:.2f}, "
                  f"fibrosis={config.fibrosis_relevance:.2f}")
    elif disease_key == "sarcopenia":
        targets = SarcopeniaTargets.get_all_sarcopenia_targets()
        for gene, config in targets.items():
            print(f"\n  {gene} ({config.protein_name})")
            print(f"    Evidence Level: {config.evidence_level}")
            print(f"    Priority Score: {config.priority_score:.3f}")
            print(f"    Key Axes: anabolism={config.anabolism_relevance:.2f}, "
                  f"catabolism={config.catabolism_relevance:.2f}, "
                  f"mitoch={config.mitochondrial_relevance:.2f}")
    else:
        print(f"  Target list for {disease_name} not yet implemented")
        print("  Use Engine 1 scoring to get target priorities")


def run_engine1(disease_name: str, top_n: int = 10, output_json: bool = False):
    """Run Engine 1: Disease → Target prioritization"""
    disease_key = disease_name.lower().replace("-", "_")
    
    if disease_key not in ["masld", "sarcopenia", "lung_fibrosis"]:
        print(f"  Engine 1 for {disease_name} not yet fully implemented")
        print("  Available: masld, sarcopenia, lung_fibrosis")
        return
    
    disease_type = DISEASE_MAP[disease_key]
    
    print(f"\n🚀 Running Engine 1: {disease_name.upper()} Target Prioritization")
    print("=" * 60)
    
    # Run prioritization
    engine = DiseaseEngine()
    result = engine.prioritize_targets(disease=disease_type)
    
    print(f"\n📊 Results Summary:")
    print(f"   Total targets evaluated: {result.total_candidates_evaluated}")
    print(f"   Targets returned: {len(result.targets)}")
    print(f"   Quality gate passed: {'✅' if result.quality_gate_passed else '❌'}")
    print(f"   Scoring time: {result.scoring_time_seconds:.2f}s")
    
    print(f"\n🏆 Top {top_n} Prioritized Targets:")
    print("-" * 60)
    
    top_targets = result.get_top_targets(top_n)
    for i, target in enumerate(top_targets, 1):
        print(f"\n  {i}. {target.gene_name} ({target.protein_name})")
        print(f"     Priority Score: {target.priority_score:.3f}")
        print(f"     Confidence: {target.confidence:.2f}")
        print(f"     Recommended Modalities: {', '.join(target.recommended_modalities[:3])}")
        
        if target.scores:
            print(f"     Scores:")
            print(f"       - Disease Context: {target.scores.disease_context:.2f}")
            print(f"       - Perturbation Rescue: {target.scores.perturbation_rescue:.2f}")
            print(f"       - Safety: {target.scores.safety:.2f}")
            print(f"       - Tissue Specificity: {target.scores.tissue_specificity:.2f}")
    
    if output_json:
        output_file = f"arp22_{disease_key}_targets_{len(top_targets)}.json"
        with open(output_file, "w") as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"\n💾 Results saved to: {output_file}")
    
    return result


def show_weights(disease_name: str):
    """Show weight configuration for a disease"""
    disease_key = disease_name.lower().replace("-", "_")
    
    try:
        disease_enum = Disease(disease_key)
    except ValueError:
        print(f"Unknown disease: {disease_name}")
        return
    
    weights = DISEASE_WEIGHTS.get(disease_enum)
    
    if not weights:
        print(f"Weights not available for: {disease_name}")
        return
    
    print(f"\n⚖️ Weight Configuration for {disease_name.upper()}")
    print("=" * 60)
    print(f"\n  Dimension                  Weight")
    print(f"  " + "-" * 35)
    print(f"  Genetic Causality          {weights.genetic_causality:.2f}")
    print(f"  Disease Context            {weights.disease_context:.2f}")
    print(f"  Perturbation Rescue        {weights.perturbation_rescue:.2f}")
    print(f"  Tissue Specificity         {weights.tissue_specificity:.2f}")
    print(f"  Druggability               {weights.druggability:.2f}")
    print(f"  Safety                     {weights.safety:.2f}")
    print(f"  Translation                {weights.translation:.2f}")
    print(f"  Competitive Novelty        {weights.competitive_novelty:.2f}")
    print(f"  " + "-" * 35)
    print(f"  TOTAL                      1.00")


def main():
    parser = argparse.ArgumentParser(
        description="ARP v22 - Disease-to-Target Drug Discovery Pipeline"
    )
    
    parser.add_argument(
        "disease",
        nargs="?",
        help="Disease to run (masld, sarcopenia, lung_fibrosis, heart_failure, cancer)"
    )
    
    parser.add_argument(
        "--list-diseases",
        action="store_true",
        help="List all available diseases"
    )
    
    parser.add_argument(
        "--list-targets",
        metavar="DISEASE",
        help="List all targets for a disease"
    )
    
    parser.add_argument(
        "--weights",
        metavar="DISEASE",
        help="Show weight configuration for a disease"
    )
    
    parser.add_argument(
        "-n", "--top-n",
        type=int,
        default=10,
        help="Number of top targets to display (default: 10)"
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Save results as JSON"
    )
    
    args = parser.parse_args()
    
    # Handle commands
    if args.list_diseases:
        list_diseases()
    elif args.list_targets:
        list_targets(args.list_targets)
    elif args.weights:
        show_weights(args.weights)
    elif args.disease:
        run_engine1(args.disease, top_n=args.top_n, output_json=args.json)
    else:
        parser.print_help()
        list_diseases()


if __name__ == "__main__":
    main()
