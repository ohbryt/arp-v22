"""
ARP v22 - Engine 3: Modality → Candidate Generation

This module implements candidate prioritization given a target and modality.
It retrieves or generates candidate compounds and ranks them.
"""

import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum
import json


@dataclass
class CandidateCompound:
    """A candidate compound for a target"""
    compound_id: str
    name: str
    smiles: Optional[str] = None
    modality: str = "small_molecule"
    
    # Source
    source: str = "literature"  # "literature", "de_novo", "database"
    development_stage: str = "preclinical"  # discovery, lead_opt, preclinical, phase1, phase2, phase3, approved
    
    # Target engagement
    target_name: str = ""
    binding_mode: str = "unknown"  # agonist, antagonist, inhibitor, etc.
    affinity: Optional[float] = None  # Kd/Ki/IC50 in nM
    modality_fit_score: float = 1.0  # 0-1, how well this matches preferred modality
    
    # ADMET (0-1 scores)
    admet_score: float = 0.50
    absorption_score: float = 0.50
    distribution_score: float = 0.50
    metabolism_score: float = 0.50
    excretion_score: float = 0.50
    safety_score: float = 0.50
    
    # Developability
    solubility: float = 0.50
    permeability: float = 0.50
    metabolic_stability: float = 0.50
    herg_liability: float = 0.50  # 0 = safe, 1 = risky
    
    # Efficacy
    efficacy_score: float = 0.50
    potency_score: float = 0.50
    
    # Composite scores
    composite_score: float = 0.0
    admet_composite: float = 0.0
    
    # Clinical data
    clinical_trials: List[str] = field(default_factory=list)
    approved_indications: List[str] = field(default_factory=list)
    
    # Development
    estimated_timeline: str = "3-5 years"
    estimated_cost: str = "moderate"
    
    # Metadata
    references: List[str] = field(default_factory=list)
    notes: str = ""
    
    def calculate_scores(self):
        """Calculate composite scores"""
        # ADMET composite: blend of explicit admet_score and component average
        admet_components = (
            self.absorption_score * 0.20 +
            self.distribution_score * 0.15 +
            self.metabolism_score * 0.20 +
            self.excretion_score * 0.10 +
            self.safety_score * 0.35
        )
        # If admet_score was explicitly set (not default), blend it
        if self.admet_score != 0.50:  # Not default value
            self.admet_composite = (admet_components * 0.7 + self.admet_score * 0.3)
        else:
            self.admet_composite = admet_components
        
        # Developability
        developability = (
            self.solubility * 0.25 +
            self.permeability * 0.25 +
            self.metabolic_stability * 0.25 +
            (1 - self.herg_liability) * 0.25  # Invert hERG
        )
        
        # Composite
        self.composite_score = (
            self.admet_composite * 0.35 +
            self.efficacy_score * 0.35 +
            developability * 0.20 +
            self.potency_score * 0.10
        )
    
    def to_dict(self) -> Dict[str, Any]:
        self.calculate_scores()
        return {
            "compound_id": self.compound_id,
            "name": self.name,
            "smiles": self.smiles,
            "modality": self.modality,
            "source": self.source,
            "development_stage": self.development_stage,
            "target": self.target_name,
            "binding_mode": self.binding_mode,
            "affinity_nM": self.affinity,
            "admet_score": round(self.admet_composite, 3),
            "efficacy_score": round(self.efficacy_score, 3),
            "composite_score": round(self.composite_score, 3),
            "development_stage": self.development_stage,
            "approved_indications": self.approved_indications,
            "references": self.references[:3],
        }


@dataclass
class CandidateRankingResult:
    """Result from ranking candidates"""
    target_id: str
    gene_name: str
    disease: str
    modality: str
    candidates: List[CandidateCompound]
    total_candidates: int
    ranking_time_seconds: float = 0.0
    
    def get_top_candidates(self, n: int = 10) -> List[CandidateCompound]:
        """Get top N candidates by composite score"""
        sorted_candidates = sorted(self.candidates, key=lambda c: c.composite_score, reverse=True)
        return sorted_candidates[:n]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_id": self.target_id,
            "gene_name": self.gene_name,
            "disease": self.disease,
            "modality": self.modality,
            "total_candidates": self.total_candidates,
            "top_10": [
                {
                    "name": c.name,
                    "composite_score": round(c.composite_score, 3),
                    "admet_score": round(c.admet_composite, 3),
                    "stage": c.development_stage,
                }
                for c in self.get_top_candidates(10)
            ],
            "ranking_time_seconds": round(self.ranking_time_seconds, 3),
        }


# ============================================================================
# KNOWN COMPOUNDS DATABASE
# ============================================================================

# MASLD known compounds
MASLD_COMPOUNDS = {
    "THRB": [
        {"name": "Resmetirom", "smiles": "CC(=O)Nc1ccc(C2=C(C3CCC3)C(=O)C2=C(C)C(=O)C=C1)cc1", 
         "stage": "approved", "affinity": 0.21, "source": "literature"},
        {"name": "ASC-41", "stage": "phase2", "source": "literature"},
        {"name": "TERN-101", "stage": "phase2", "source": "literature"},
    ],
    "NR1H4": [
        {"name": "Obeticholic acid", "smiles": "CC(C)[C@H]1[C@H]2C[C@@H]3[C@@H]4C[C@@H](C)C(C)=C[C@]4(C)[C@@H]3[C@@H]1[C@@H]2C(C)=O", 
         "stage": "approved", "affinity": 90.0, "source": "literature"},
        {"name": "Cilofexor", "stage": "phase2", "source": "literature"},
        {"name": "Tropifexor", "stage": "phase2", "source": "literature"},
    ],
    "GLP1R": [
        {"name": "Semaglutide", "stage": "approved", "affinity": 0.015, "source": "literature"},
        {"name": "Liraglutide", "stage": "approved", "affinity": 0.038, "source": "literature"},
        {"name": "Tirzepatide", "stage": "approved", "affinity": 0.025, "source": "literature"},
    ],
    "SLC5A2": [
        {"name": "Empagliflozin", "stage": "approved", "affinity": 3.1, "source": "literature"},
        {"name": "Dapagliflozin", "stage": "approved", "affinity": 1.2, "source": "literature"},
        {"name": "Canagliflozin", "stage": "approved", "affinity": 2.6, "source": "literature"},
    ],
}

# Sarcopenia known compounds
SARCOPENIA_COMPOUNDS = {
    "MSTN": [
        {"name": "Bimagrumab", "stage": "phase2", "source": "literature"},
        {"name": "Apitegromab", "stage": "phase2", "source": "literature"},
        {"name": "Domagrozumab", "stage": "discontinued", "source": "literature"},
    ],
    "MTOR": [
        {"name": "Rapamycin", "stage": "approved", "affinity": 0.1, "source": "literature"},
        {"name": "Everolimus", "stage": "approved", "affinity": 0.3, "source": "literature"},
    ],
    "FOXO1": [
        {"name": "AS1842856", "stage": "preclinical", "affinity": 89.0, "source": "literature"},
    ],
    "SIRT1": [
        {"name": "Resveratrol", "stage": "preclinical", "affinity": 100.0, "source": "literature"},
        {"name": "SRT2104", "stage": "phase1", "source": "literature"},
    ],
    "PRKAA1": [
        {"name": "Metformin", "stage": "approved", "affinity": 100.0, "source": "literature"},
        {"name": "AICAR", "stage": "preclinical", "source": "literature"},
    ],
}

# Lung fibrosis known compounds
LUNG_FIBROSIS_COMPOUNDS = {
    "TGFB1": [
        {"name": "Pirfenidone", "stage": "approved", "affinity": None, "source": "literature"},
        {"name": "Nintedanib", "stage": "approved", "affinity": 80.0, "source": "literature"},
        {"name": "Pamrevlumab", "stage": "phase2", "source": "literature"},
    ],
    "CTGF": [
        {"name": "Pamrevlumab", "stage": "phase2", "source": "literature"},
    ],
    "PDGFRA": [
        {"name": "Nintedanib", "stage": "approved", "affinity": 34.0, "source": "literature"},
    ],
}

# Heart failure known compounds
HEART_FAILURE_COMPOUNDS = {
    "SLC5A2": [
        {"name": "Empagliflozin", "stage": "approved", "affinity": 3.1, "source": "literature"},
        {"name": "Dapagliflozin", "stage": "approved", "affinity": 1.2, "source": "literature"},
    ],
    "NPPA": [
        {"name": "Nesiritide", "stage": "approved", "affinity": 0.1, "source": "literature"},
    ],
    "ARNI": [
        {"name": "Sacubitril/Valsartan", "stage": "approved", "affinity": 0.6, "source": "literature"},
    ],
    "AGTR1": [
        {"name": "Losartan", "stage": "approved", "affinity": 1.3, "source": "literature"},
        {"name": "Valsartan", "stage": "approved", "affinity": 2.6, "source": "literature"},
    ],
}

# Cancer known compounds
CANCER_COMPOUNDS = {
    "EGFR": [
        {"name": "Osimertinib", "stage": "approved", "affinity": 0.7, "source": "literature"},
        {"name": "Erlotinib", "stage": "approved", "affinity": 2.0, "source": "literature"},
        {"name": "Gefitinib", "stage": "approved", "affinity": 1.0, "source": "literature"},
        {"name": "Afatinib", "stage": "approved", "affinity": 0.5, "source": "literature"},
        {"name": "Amivantamab", "stage": "approved", "affinity": 0.05, "source": "literature"},
    ],
    "ALK": [
        {"name": "Alectinib", "stage": "approved", "affinity": 1.9, "source": "literature"},
        {"name": "Lorlatinib", "stage": "approved", "affinity": 0.7, "source": "literature"},
        {"name": "Brigatinib", "stage": "approved", "affinity": 0.9, "source": "literature"},
    ],
    "MET": [
        {"name": "Capmatinib", "stage": "approved", "affinity": 0.6, "source": "literature"},
        {"name": "Tepotinib", "stage": "approved", "affinity": 3.0, "source": "literature"},
    ],
    "KRAS": [
        {"name": "Sotorasib", "stage": "approved", "affinity": 10.0, "source": "literature"},
        {"name": "Adagrasib", "stage": "approved", "affinity": 5.0, "source": "literature"},
    ],
    "PD-L1": [
        {"name": "Pembrolizumab", "stage": "approved", "affinity": 0.1, "source": "literature"},
        {"name": "Atezolizumab", "stage": "approved", "affinity": 0.1, "source": "literature"},
        {"name": "Durvalumab", "stage": "approved", "affinity": 0.1, "source": "literature"},
    ],
}


# ============================================================================
# COMPOUND DATABASE REGISTRY
# ============================================================================

COMPOUND_DATABASE = {
    "masld": MASLD_COMPOUNDS,
    "sarcopenia": SARCOPENIA_COMPOUNDS,
    "lung_fibrosis": LUNG_FIBROSIS_COMPOUNDS,
    "heart_failure": HEART_FAILURE_COMPOUNDS,
    "cancer": CANCER_COMPOUNDS,
}


# ============================================================================
# CANDIDATE GENERATION ENGINE
# ============================================================================

class CandidateEngine:
    """
    Engine 3: Modality → Candidate Generation
    
    Given a target, modality, and disease, retrieves or generates candidate compounds.
    """
    
    def __init__(self):
        self.db = COMPOUND_DATABASE
    
    def generate_candidates(
        self,
        gene_name: str,
        disease: str,
        modality: str = "small_molecule",
        include_de_novo: bool = False,
    ) -> CandidateRankingResult:
        """
        Generate candidates for a target.
        
        Args:
            gene_name: Target gene name
            disease: Disease context
            modality: Preferred modality
            include_de_novo: Whether to include de novo generated candidates
            
        Returns:
            CandidateRankingResult with ranked candidates
        """
        start_time = time.time()
        
        candidates = []
        
        # Retrieve from database
        disease_db = self.db.get(disease, {})
        target_compounds = disease_db.get(gene_name, [])
        
        for i, compound_data in enumerate(target_compounds):
            compound = self._create_candidate(
                compound_id=f"{gene_name}_{i+1}",
                gene_name=gene_name,
                disease=disease,
                modality_hint=modality,  # Pass preferred modality for fit scoring
                **compound_data
            )
            candidates.append(compound)
        
        # Sort by composite score with modality fit adjustment
        for c in candidates:
            c.calculate_scores()
            # Apply modality fit penalty if it doesn't match preferred modality
            # This ensures Engine 2 routing is respected
            c.composite_score *= c.modality_fit_score
        
        candidates.sort(key=lambda x: x.composite_score, reverse=True)
        
        elapsed = time.time() - start_time
        
        return CandidateRankingResult(
            target_id=f"{gene_name}_{disease}",
            gene_name=gene_name,
            disease=disease,
            modality=modality,
            candidates=candidates,
            total_candidates=len(candidates),
            ranking_time_seconds=elapsed,
        )
    
    def _create_candidate(
        self,
        compound_id: str,
        gene_name: str,
        disease: str,
        name: str,
        smiles: str = None,
        stage: str = "preclinical",
        affinity: float = None,
        source: str = "literature",
        modality_hint: str = None,
    ) -> CandidateCompound:
        """
        Create a candidate compound from data.
        
        Args:
            modality_hint: Preferred modality from Engine 2 routing.
                          If provided, modality_fit will be calculated.
        """
        # Default scores based on stage and disease
        base_scores = self._get_base_scores(stage)
        
        # Determine modality: use smarter inference if smiles provided
        # Note: In production, this should come from actual compound metadata
        actual_modality = self._infer_modality(smiles)
        
        compound = CandidateCompound(
            compound_id=compound_id,
            name=name,
            smiles=smiles,
            modality=actual_modality,
            source=source,
            development_stage=stage,
            target_name=gene_name,
            affinity=affinity,
            **base_scores
        )
        
        # Calculate modality fit if hint provided
        if modality_hint:
            compound.modality_fit_score = self._calculate_modality_fit(
                actual_modality, modality_hint
            )
        else:
            compound.modality_fit_score = 1.0  # No penalty if no hint
        
        # Set approved indications only if NOT already set (don't auto-generate)
        # Note: Auto-generating approved_indications from disease name is dangerous
        # It creates false metadata. Only set if provided or if explicitly known.
        if stage == "approved" and not compound.approved_indications:
            # Don't auto-fill - would create incorrect metadata
            # Real implementation should query DrugBank/API for actual indications
            pass
        
        return compound
    
    def _infer_modality(self, smiles: Optional[str]) -> str:
        """
        Infer compound modality from SMILES.
        
        This is a heuristic - in production, modality should come from
        actual compound metadata (molecule_type,分子量, etc.)
        
        Returns:
            Modality string: small_molecule, peptide, oligo, biologic
        """
        if not smiles:
            return "biologic"
        
        # Calculate basic properties for inference
        try:
            from rdkit import Chem
            from rdkit.Chem import Descriptors
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return "biologic"
            
            mol_wt = Descriptors.MolWt(mol)
            num_amino_acids = smiles.count('N') + smiles.count('n')  # Rough heuristic
            
            # Very rough heuristics for modality inference
            # Small molecules: typically < 1000 Da
            if mol_wt < 1500:
                # Check for peptide-like patterns
                if '(' in smiles and ')' in smiles and num_amino_acids > 3:
                    return "peptide"
                # Check for nucleotide-like patterns
                if smiles.count('O') > 5 and 'P' in smiles:
                    return "oligo"
                return "small_molecule"
            else:
                # > 1500 Da is likely biologic (peptide, protein, antibody fragment)
                if mol_wt > 5000:
                    return "biologic"
                else:
                    return "peptide"
        except ImportError:
            # RDKit not available, fall back to basic heuristic
            return "small_molecule" if smiles else "biologic"
    
    def _get_base_scores(self, stage: str) -> Dict[str, float]:
        """Get base scores based on development stage"""
        stage_scores = {
            "approved": {
                "admet_score": 0.85,
                "absorption_score": 0.85,
                "distribution_score": 0.80,
                "metabolism_score": 0.80,
                "excretion_score": 0.82,
                "safety_score": 0.80,
                "solubility": 0.82,
                "permeability": 0.80,
                "metabolic_stability": 0.82,
                "herg_liability": 0.15,
                "efficacy_score": 0.85,
                "potency_score": 0.85,
            },
            "phase3": {
                "admet_score": 0.78,
                "absorption_score": 0.80,
                "distribution_score": 0.75,
                "metabolism_score": 0.75,
                "excretion_score": 0.78,
                "safety_score": 0.75,
                "solubility": 0.78,
                "permeability": 0.75,
                "metabolic_stability": 0.75,
                "herg_liability": 0.20,
                "efficacy_score": 0.80,
                "potency_score": 0.80,
            },
            "phase2": {
                "admet_score": 0.70,
                "absorption_score": 0.72,
                "distribution_score": 0.68,
                "metabolism_score": 0.68,
                "excretion_score": 0.70,
                "safety_score": 0.68,
                "solubility": 0.70,
                "permeability": 0.70,
                "metabolic_stability": 0.68,
                "herg_liability": 0.25,
                "efficacy_score": 0.72,
                "potency_score": 0.75,
            },
            "phase1": {
                "admet_score": 0.65,
                "absorption_score": 0.68,
                "distribution_score": 0.62,
                "metabolism_score": 0.62,
                "excretion_score": 0.65,
                "safety_score": 0.60,
                "solubility": 0.65,
                "permeability": 0.65,
                "metabolic_stability": 0.60,
                "herg_liability": 0.30,
                "efficacy_score": 0.60,
                "potency_score": 0.70,
            },
            "preclinical": {
                "admet_score": 0.55,
                "absorption_score": 0.58,
                "distribution_score": 0.52,
                "metabolism_score": 0.52,
                "excretion_score": 0.55,
                "safety_score": 0.50,
                "solubility": 0.55,
                "permeability": 0.55,
                "metabolic_stability": 0.50,
                "herg_liability": 0.35,
                "efficacy_score": 0.50,
                "potency_score": 0.60,
            },
            "discovery": {
                "admet_score": 0.40,
                "absorption_score": 0.45,
                "distribution_score": 0.40,
                "metabolism_score": 0.38,
                "excretion_score": 0.42,
                "safety_score": 0.35,
                "solubility": 0.40,
                "permeability": 0.42,
                "metabolic_stability": 0.38,
                "herg_liability": 0.45,
                "efficacy_score": 0.35,
                "potency_score": 0.50,
            },
            "discontinued": {
                "admet_score": 0.30,
                "absorption_score": 0.35,
                "distribution_score": 0.30,
                "metabolism_score": 0.30,
                "excretion_score": 0.32,
                "safety_score": 0.25,
                "solubility": 0.35,
                "permeability": 0.32,
                "metabolic_stability": 0.30,
                "herg_liability": 0.50,
                "efficacy_score": 0.30,
                "potency_score": 0.40,
            },
        }
        
        return stage_scores.get(stage, stage_scores["discovery"])
    
    def _calculate_modality_fit(
        self,
        actual_modality: str,
        preferred_modality: str,
    ) -> float:
        """
        Calculate how well a compound's modality fits the preferred modality.
        
        Args:
            actual_modality: The compound's actual modality (small_molecule, biologic, etc.)
            preferred_modality: The modality recommended by Engine 2
            
        Returns:
            0-1 score where 1 = perfect match, 0 = complete mismatch
        """
        if actual_modality == preferred_modality:
            return 1.0
        
        # Define modality compatibility matrix
        # 1.0 = exact match, 0.7-0.9 = compatible, 0.3-0.6 = partial, 0.1-0.2 = stretch, 0 = incompatible
        compatibility = {
            # Format: (actual, preferred) -> fit_score
            ("small_molecule", "biologic"): 0.3,
            ("small_molecule", "peptide"): 0.6,
            ("small_molecule", "antibody"): 0.2,
            ("small_molecule", "oligo"): 0.5,
            ("small_molecule", "degrader"): 0.7,
            ("biologic", "small_molecule"): 0.3,
            ("biologic", "antibody"): 0.9,
            ("biologic", "peptide"): 0.8,
            ("peptide", "small_molecule"): 0.4,
            ("peptide", "biologic"): 0.7,
            ("oligo", "small_molecule"): 0.3,
            ("antibody", "biologic"): 0.9,
        }
        
        return compatibility.get((actual_modality, preferred_modality), 0.1)


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_candidates(
    gene_name: str,
    disease: str,
    modality: str = "small_molecule",
) -> CandidateRankingResult:
    """Convenience function for candidate generation"""
    engine = CandidateEngine()
    return engine.generate_candidates(gene_name, disease, modality)
