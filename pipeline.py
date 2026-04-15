"""
ARP v22 - Main Pipeline Orchestrator

This module provides a unified interface to all three engines:
- Engine 1: Disease → Target (target prioritization)
- Engine 2: Target → Modality (modality routing)
- Engine 3: Modality → Candidate (candidate generation)
- Literature: PubMed/ClinicalTrials integration
- De Novo: Novel compound generation
- Dashboard: HTML report generation
"""

import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path

from core.scoring_engine import DiseaseEngine, DiseaseType, TargetScorer
from core.modality_routing import ModalityRouter, AssayEngine
from core.candidate_engine import CandidateEngine, CandidateRankingResult
from core.schema import TargetDossier, ScoringEngineConfig
from core.literature_integrator import LiteratureIntegrator
from core.de_novo_generator import DeNovoGenerator
from core.dashboard import DashboardGenerator


@dataclass
class PipelineResult:
    """Complete result from running the full pipeline"""
    disease: str
    targets: List[TargetDossier]
    total_targets_evaluated: int
    execution_time_seconds: float
    
    # Engine results
    engine1_result: Any = None
    engine2_results: Dict[str, Any] = field(default_factory=dict)
    engine3_results: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "disease": self.disease,
            "total_targets_evaluated": self.total_targets_evaluated,
            "targets_returned": len(self.targets),
            "execution_time_seconds": round(self.execution_time_seconds, 2),
            "top_targets": [
                {
                    "gene": t.gene_name,
                    "score": round(t.priority_score, 3),
                    "rank": t.rank,
                    "modalities": t.recommended_modalities[:2],
                }
                for t in self.targets[:10]
            ],
            "engine2_runs": len(self.engine2_results),
            "engine3_runs": len(self.engine3_results),
        }
    
    def save_json(self, filepath: str):
        """Save result to JSON file"""
        with open(filepath, "w") as f:
            json.dump(self.to_dict(), f, indent=2)


class ARPv22Pipeline:
    """
    Main pipeline orchestrator for ARP v22.
    
    Usage:
        pipeline = ARPv22Pipeline()
        result = pipeline.run(disease="masld", top_n=10)
    """
    
    def __init__(self, config: Optional[ScoringEngineConfig] = None):
        self.config = config or ScoringEngineConfig()
        self.engine1 = DiseaseEngine(self.config)
        self.engine2 = ModalityRouter()
        self.engine3 = CandidateEngine()
        self.assay_engine = AssayEngine()
    
    def run(
        self,
        disease: str,
        top_n: int = 10,
        run_engine2: bool = True,
        run_engine3: bool = True,
        disease_pack_scores: Optional[Dict[str, Dict[str, float]]] = None,
    ) -> PipelineResult:
        """
        Run the full pipeline for a disease.
        
        Args:
            disease: Disease name (masld, sarcopenia, etc.)
            top_n: Number of top targets to process through engines 2 and 3
            run_engine2: Whether to run modality routing
            run_engine3: Whether to run candidate generation
            disease_pack_scores: Pre-computed target scores from disease pack
            
        Returns:
            PipelineResult with all engine outputs
        """
        start_time = time.time()
        
        # Convert disease string to DiseaseType
        disease_type = self._str_to_disease(disease)
        
        # Run Engine 1: Disease → Target
        print(f"🎯 Engine 1: Running target prioritization for {disease}...")
        engine1_result = self.engine1.prioritize_targets(
            disease=disease_type,
            score_overrides=disease_pack_scores or {},
        )
        
        targets = engine1_result.get_top_targets(top_n)
        
        print(f"   Found {len(targets)} targets")
        
        # Run Engine 2: Target → Modality
        engine2_results = {}
        if run_engine2:
            print(f"🔄 Engine 2: Routing targets to modalities...")
            for target in targets[:5]:  # Top 5 only
                routing_result = self.engine2.route_target(target, disease_type)
                engine2_results[target.gene_name] = routing_result.to_dict()
                print(f"   {target.gene_name} → {routing_result.get_top_modality()}")
        
        # Run Engine 3: Modality → Candidate
        engine3_results = {}
        if run_engine3:
            print(f"💊 Engine 3: Generating candidates...")
            for target in targets[:5]:  # Top 5 only
                top_modality = target.recommended_modalities[0] if target.recommended_modalities else "small_molecule"
                candidates_result = self.engine3.generate_candidates(
                    gene_name=target.gene_name,
                    disease=disease,
                    modality=top_modality,
                )
                engine3_results[target.gene_name] = candidates_result.to_dict()
                print(f"   {target.gene_name}: {len(candidates_result.candidates)} candidates")
        
        elapsed = time.time() - start_time
        
        print(f"\n✅ Pipeline complete in {elapsed:.1f}s")
        
        return PipelineResult(
            disease=disease,
            targets=targets,
            total_targets_evaluated=engine1_result.total_candidates_evaluated,
            execution_time_seconds=elapsed,
            engine1_result=engine1_result,
            engine2_results=engine2_results,
            engine3_results=engine3_results,
        )
    
    def run_engine1_only(
        self,
        disease: str,
        disease_pack_scores: Optional[Dict[str, Dict[str, float]]] = None,
    ):
        """Run only Engine 1 (target prioritization)"""
        disease_type = self._str_to_disease(disease)
        return self.engine1.prioritize_targets(
            disease=disease_type,
            score_overrides=disease_pack_scores or {},
        )
    
    def run_target_full(
        self,
        gene_name: str,
        disease: str,
    ) -> Dict[str, Any]:
        """
        Run full pipeline for a single target.
        
        Returns comprehensive analysis including:
        - Target dossier
        - Modality recommendations
        - Assay recommendations
        - Candidate compounds
        """
        disease_type = self._str_to_disease(disease)
        
        # Create a minimal target dossier
        target = self._create_minimal_target(gene_name, disease_type)
        
        # Engine 1 score (from registry if available)
        scorer = TargetScorer()
        from core.scoring_engine import TARGET_REGISTRY, TARGET_CLASS_MODALITY
        target_info = TARGET_REGISTRY.get(disease, {}).get(gene_name)
        
        if target_info:
            scores, penalties, priority_score = scorer.score_target(target_info, disease_type)
            target.scores = scores
            target.priority_score = priority_score
            target.penalties = penalties
        
        # Engine 2: Modality routing
        modality_result = self.engine2.route_target(target, disease_type)
        
        # Get assays
        assays = self.assay_engine.get_assays(disease_type)
        
        # Engine 3: Candidate generation
        top_modality = modality_result.get_top_modality() or "small_molecule"
        candidates_result = self.engine3.generate_candidates(
            gene_name=gene_name,
            disease=disease,
            modality=top_modality,
        )
        
        return {
            "target": target.to_dict(),
            "modality_routing": modality_result.to_dict(),
            "assays": [
                {
                    "name": a.assay_name,
                    "type": a.assay_type,
                    "readout": a.readout,
                    "priority": a.priority,
                }
                for a in assays[:5]
            ],
            "candidates": candidates_result.to_dict(),
        }
    
    def _str_to_disease(self, disease: str) -> DiseaseType:
        """Convert disease string to DiseaseType"""
        mapping = {
            "masld": DiseaseType.MASLD,
            "sarcopenia": DiseaseType.SARCOPENIA,
            "lung_fibrosis": DiseaseType.LUNG_FIBROSIS,
            "lung-fibrosis": DiseaseType.LUNG_FIBROSIS,
            "heart_failure": DiseaseType.HEART_FAILURE,
            "heart-failure": DiseaseType.HEART_FAILURE,
            "cancer": DiseaseType.CANCER,
        }
        normalized = disease.lower().strip()
        if normalized not in mapping:
            raise ValueError(f"Unsupported disease: {disease!r}. Supported: {list(mapping.keys())}")
        return mapping[normalized]
    
    def get_literature(
        self,
        gene_name: str,
        disease: str,
        max_articles: int = 10,
    ) -> Dict[str, Any]:
        """
        Get literature for a target using PubMed and ClinicalTrials.gov.
        """
        import asyncio
        
        integrator = LiteratureIntegrator()
        
        # Run async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                integrator.get_target_literature(gene_name, disease, max_articles)
            )
        finally:
            loop.close()
        
        return result
    
    def generate_de_novo(
        self,
        target_class: str,
        target_name: str,
        disease: str,
        num_candidates: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Generate de novo compound candidates.
        """
        generator = DeNovoGenerator(seed=42)
        candidates = generator.generate(
            target_class=target_class,
            target_name=target_name,
            disease=disease,
            num_candidates=num_candidates,
        )
        return [c.to_dict() for c in candidates]
    
    def generate_dashboard(
        self,
        disease: str,
        engine1_result: Any,
        engine2_results: Dict[str, Any],
        engine3_results: Dict[str, Any],
        output_path: str = "arp22_report.html",
    ) -> str:
        """
        Generate an HTML dashboard report.
        """
        generator = DashboardGenerator()
        
        # Convert engine1 result to dict
        e1_dict = engine1_result.to_dict() if hasattr(engine1_result, 'to_dict') else engine1_result
        
        html = generator.generate_pipeline_report(
            disease=disease,
            engine1_result=e1_dict,
            engine2_results=engine2_results,
            engine3_results=engine3_results,
        )
        generator.save_report(html, output_path)
        return output_path
    
    def _create_minimal_target(self, gene_name: str, disease: DiseaseType) -> TargetDossier:
        """Create a minimal target dossier for a gene"""
        from core.schema import TargetClass, Status
        from datetime import date
        
        return TargetDossier(
            target_id=f"{gene_name}_{disease.value}",
            gene_name=gene_name,
            disease=disease,
            status=Status.PRIORITIZED,
            created_date=date.today(),
            last_updated=date.today(),
        )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def run_pipeline(
    disease: str,
    top_n: int = 10,
) -> PipelineResult:
    """Run the full ARP v22 pipeline for a disease"""
    pipeline = ARPv22Pipeline()
    return pipeline.run(disease=disease, top_n=top_n)


def analyze_target(
    gene_name: str,
    disease: str,
) -> Dict[str, Any]:
    """Analyze a single target in depth"""
    pipeline = ARPv22Pipeline()
    return pipeline.run_target_full(gene_name=gene_name, disease=disease)


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <disease> [top_n]")
        print("  disease: masld, sarcopenia, lung_fibrosis, heart_failure, cancer")
        sys.exit(1)
    
    disease = sys.argv[1]
    top_n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    print(f"\n{'='*60}")
    print(f"ARP v22 Pipeline - {disease.upper()}")
    print(f"{'='*60}\n")
    
    result = run_pipeline(disease=disease, top_n=top_n)
    
    print(f"\n{'='*60}")
    print("TOP TARGETS")
    print(f"{'='*60}")
    for t in result.targets[:top_n]:
        print(f"\n  {t.rank}. {t.gene_name} (Score: {t.priority_score:.3f})")
        print(f"     Modalities: {t.recommended_modalities[:3]}")
    
    # Save result
    output_file = f"arp22_{disease}_pipeline_result.json"
    result.save_json(output_file)
    print(f"\n💾 Results saved to: {output_file}")
