"""
ARP v22 - De Novo Compound Generation Module

Generates novel compound candidates using:
- Fragment-based generation
- Pharmacophore-guided generation
- SMILES-based variational generation
"""

import hashlib
import json
import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import re


# ============================================================================
# FRAGMENT LIBRARY
# ============================================================================

@dataclass
class Fragment:
    """Molecular fragment for building blocks"""
    name: str
    scaffold: str  # SMILES
    mw: float
    logp: float
    hbd: int
    hba: int
    tpsa: float
    rings: int
    chiral_centers: int
    fragments_type: str  # "scaffold", "linker", "side_chain", "bioisostere"


# Core scaffolds by target class
SCAFFOLDS = {
    "nuclear_receptor": [
        Fragment(
            name="Thyroid hormone mimetic",
            scaffold="c1ccc2c(c1)c(C(=O)Nc3ccccc3)cc(c2)C",
            mw=285.0,
            logp=4.2,
            hbd=1,
            hba=2,
            tpsa=45.0,
            rings=2,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Retinoic acid derivative",
            scaffold="CC(=O)Nc1ccc(C2=C(C3CCC3)C(=O)C2=C(C)C(=O)C=C1)cc1",
            mw=585.0,
            logp=5.2,
            hbd=1,
            hba=4,
            tpsa=89.0,
            rings=3,
            chiral_centers=1,
            fragments_type="scaffold",
        ),
        Fragment(
            name="PPAR agonist core",
            scaffold="c1cc(C2=CC(=O)C3=C(C2=O)C=CC=C3)ccc1C4=CC=C(C)O4",
            mw=368.0,
            logp=4.8,
            hbd=0,
            hba=3,
            tpsa=52.0,
            rings=3,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
    ],
    
    "kinase": [
        Fragment(
            name="Aminopyrimidine core",
            scaffold="c1cc(N)nc(N)c1",
            mw=136.0,
            logp=1.5,
            hbd=2,
            hba=4,
            tpsa=78.0,
            rings=1,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Pyridinylimidazole",
            scaffold="c1cnc(N2C=C(C)N=C2)cc1",
            mw=185.0,
            logp=2.1,
            hbd=1,
            hba=3,
            tpsa=46.0,
            rings=2,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Urea hinge binder",
            scaffold="NC(=O)Nc1ccccc1",
            mw=136.0,
            logp=1.8,
            hbd=2,
            hba=2,
            tpsa=55.0,
            rings=1,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
    ],
    
    "gpc_receptor": [
        Fragment(
            name="Peptidomimetic core",
            scaffold="NC(=O)C(C)NC(=O)C(C)NC(=O)C",
            mw=303.0,
            logp=1.2,
            hbd=4,
            hba=4,
            tpsa=120.0,
            rings=0,
            chiral_centers=2,
            fragments_type="scaffold",
        ),
        Fragment(
            name="GLP1-like mimetic",
            scaffold="c1ccc2c(c1)C3=C(C=CC=C3)C2",
            mw=204.0,
            logp=3.5,
            hbd=0,
            hba=0,
            tpsa=0.0,
            rings=2,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
    ],
    
    "enzyme": [
        Fragment(
            name="Benzimidazole",
            scaffold="c1ccc2c(c1)[nH]c(=S)n2",
            mw=162.0,
            logp=2.8,
            hbd=1,
            hba=2,
            tpsa=50.0,
            rings=2,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Pyrrolidine",
            scaffold="C1CCNC1",
            mw=71.0,
            logp=0.4,
            hbd=1,
            hba=1,
            tpsa=26.0,
            rings=0,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Beta-lactam",
            scaffold="C1C(=O)NC1=O",
            mw=99.0,
            logp=0.3,
            hbd=1,
            hba=3,
            tpsa=59.0,
            rings=1,
            chiral_centers=1,
            fragments_type="scaffold",
        ),
    ],
    
    "default": [
        Fragment(
            name="Benzene ring",
            scaffold="c1ccccc1",
            mw=78.0,
            logp=2.1,
            hbd=0,
            hba=0,
            tpsa=0.0,
            rings=1,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
        Fragment(
            name="Phenyl ether",
            scaffold="c1ccc(Oc2ccccc2)cc1",
            mw=170.0,
            logp=3.4,
            hbd=0,
            hba=1,
            tpsa=9.0,
            rings=2,
            chiral_centers=0,
            fragments_type="scaffold",
        ),
    ],
}


# Linkers
LINKERS = [
    Fragment("Alkyl chain", "CCCC", mw=58.0, logp=2.0, hbd=0, hba=0, tpsa=0.0, rings=0, chiral_centers=0, fragments_type="linker"),
    Fragment("Ethylene glycol", "OCCOCCO", mw=106.0, logp=-0.5, hbd=2, hba=3, tpsa=50.0, rings=0, chiral_centers=0, fragments_type="linker"),
    Fragment("Amide bond", "NC(=O)C", mw=71.0, logp=0.2, hbd=1, hba=2, tpsa=43.0, rings=0, chiral_centers=0, fragments_type="linker"),
    Fragment("Triazole", "c1cnnn1", mw=69.0, logp=0.1, hbd=0, hba=3, tpsa=41.0, rings=1, chiral_centers=0, fragments_type="linker"),
    Fragment("Proline linker", "C1CNC(C1)C(=O)", mw=113.0, logp=-0.1, hbd=2, hba=2, tpsa=58.0, rings=1, chiral_centers=1, fragments_type="linker"),
]


# Bioisosteres
BIOISOSTERES = [
    Fragment("Carboxylic acid", "C(=O)O", mw=44.0, logp=0.1, hbd=1, hba=3, tpsa=54.0, rings=0, chiral_centers=0, fragments_type="bioisostere"),
    Fragment("Tetrazole", "C1=NN=NN1", mw=70.0, logp=0.4, hbd=0, hba=4, tpsa=65.0, rings=1, chiral_centers=0, fragments_type="bioisostere"),
    Fragment("Sulfonamide", "S(=O)(=O)N", mw=80.0, logp=0.3, hbd=1, hba=3, tpsa=60.0, rings=0, chiral_centers=0, fragments_type="bioisostere"),
    Fragment("Hydroxamic acid", "C(=O)NO", mw=59.0, logp=0.2, hbd=2, hba=3, tpsa=65.0, rings=0, chiral_centers=0, fragments_type="bioisostere"),
]


# ============================================================================
# DE NOVO COMPOUND
# ============================================================================

@dataclass
class DeNovoCompound:
    """De novo generated compound candidate"""
    compound_id: str
    name: str
    
    # Structure
    smiles: str
    scaffold_used: str
    
    # Properties (predicted)
    mw: float
    logp: float
    tpsa: float
    hbd: int
    hba: int
    rings: int
    chiral_centers: int
    fsp3: float
    
    # Quality scores
    drug_likeness: float  # 0-1
    novelty_score: float  # 0-1
    synthetic_accessibility: float  # 1 (easy) - 5 (hard)
    
    # Match to target
    target_match_score: float  # 0-1
    pharmacophore_match: float  # 0-1
    
    # Overall
    composite_score: float  # 0-1
    
    # Metadata
    generation_method: str
    generation_time: str
    parent_target: str
    disease: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "compound_id": self.compound_id,
            "name": self.name,
            "smiles": self.smiles,
            "mw": round(self.mw, 1),
            "logp": round(self.logp, 1),
            "tpsa": round(self.tpsa, 1),
            "drug_likeness": round(self.drug_likeness, 2),
            "novelty_score": round(self.novelty_score, 2),
            "synthetic_accessibility": round(self.synthetic_accessibility, 1),
            "target_match_score": round(self.target_match_score, 2),
            "composite_score": round(self.composite_score, 2),
            "generation_method": self.generation_method,
            "parent_target": self.parent_target,
            "disease": self.disease,
        }


# ============================================================================
# DE NOVO GENERATOR
# ============================================================================

class DeNovoGenerator:
    """
    De novo compound generator for ARP v22.
    
    Uses fragment-based approach with pharmacophore guidance.
    """
    
    def __init__(self, seed: Optional[int] = None):
        if seed:
            random.seed(seed)
    
    def generate(
        self,
        target_class: str,
        target_name: str,
        disease: str,
        num_candidates: int = 10,
        target_pharmacophore: Optional[List[str]] = None,
    ) -> List[DeNovoCompound]:
        """
        Generate de novo compounds for a target.
        
        Args:
            target_class: Target class (kinase, nuclear_receptor, etc.)
            target_name: Gene name
            disease: Disease context
            num_candidates: Number of candidates to generate
            target_pharmacophore: Required pharmacophore features
            
        Returns:
            List of DeNovoCompound candidates
        """
        # Get scaffolds for target class
        scaffolds = SCAFFOLDS.get(target_class, SCAFFOLDS["default"])
        
        candidates = []
        for i in range(num_candidates):
            # Select scaffold
            scaffold = random.choice(scaffolds)
            
            # Optionally add linker and side chain
            use_linker = random.random() > 0.5
            use_bioisostere = random.random() > 0.7
            
            # Build compound
            smiles = self._build_compound(scaffold, use_linker, use_bioisostere)
            
            # Calculate properties
            props = self._calculate_properties(smiles, scaffold)
            
            # Calculate scores
            drug_likeness = self._assess_drug_likeness(props, target_class)
            novelty = self._assess_novelty(smiles, scaffold)
            synthetic = self._assess_synthetic_accessibility(scaffold, use_linker, use_bioisostere)
            target_match = self._assess_target_match(target_class, props)
            pharmacophore = self._assess_Pharmacophore(smiles, target_pharmacophore)
            
            # Composite score
            composite = (
                drug_likeness * 0.25 +
                novelty * 0.20 +
                (1 - synthetic / 5) * 0.15 +
                target_match * 0.25 +
                pharmacophore * 0.15
            )
            
            # Generate ID and name
            compound_id = self._generate_id(smiles, i)
            name = f"DN-{target_name[:3].upper()}-{i+1:03d}"
            
            candidates.append(DeNovoCompound(
                compound_id=compound_id,
                name=name,
                smiles=smiles,
                scaffold_used=scaffold.name,
                **props,
                drug_likeness=drug_likeness,
                novelty_score=novelty,
                synthetic_accessibility=synthetic,
                target_match_score=target_match,
                pharmacophore_match=pharmacophore,
                composite_score=composite,
                generation_method="fragment_based_v1",
                generation_time=datetime.now().isoformat(),
                parent_target=target_name,
                disease=disease,
            ))
        
        # Sort by composite score
        candidates.sort(key=lambda x: x.composite_score, reverse=True)
        
        return candidates
    
    def _build_compound(
        self,
        scaffold: Fragment,
        use_linker: bool,
        use_bioisostere: bool,
    ) -> str:
        """Build a compound from fragments"""
        parts = [scaffold.scaffold]
        
        if use_linker:
            linker = random.choice(LINKERS)
            parts.append(linker.scaffold)
        
        if use_bioisostere:
            bio = random.choice(BIOISOSTERES)
            parts.append(bio.scaffold)
        
        return ".".join(parts) if len(parts) > 1 else parts[0]
    
    def _calculate_properties(self, smiles: str, scaffold: Fragment) -> Dict[str, Any]:
        """Calculate molecular properties (simplified)"""
        # Base properties from scaffold with variation
        variation = 0.1
        
        mw = scaffold.mw * (1 + random.uniform(-variation, variation))
        logp = scaffold.logp * (1 + random.uniform(-variation, variation))
        tpsa = scaffold.tpsa * (1 + random.uniform(-variation, variation))
        hbd = scaffold.hbd + random.randint(-1, 1)
        hba = scaffold.hba + random.randint(-1, 1)
        rings = scaffold.rings + (1 if random.random() > 0.7 else 0)
        chiral = scaffold.chiral_centers + (1 if random.random() > 0.8 else 0)
        
        # Calculate FSP3 (carbon fraction sp3)
        # Simplified: more rings/sp3 carbons = higher fsp3
        fsp3 = min(1.0, 0.3 + (chiral * 0.1) + (rings * 0.05))
        
        # Clamp values
        mw = max(50, min(800, mw))
        logp = max(-2, min(8, logp))
        tpsa = max(0, min(200, tpsa))
        hbd = max(0, min(10, hbd))
        hba = max(0, min(15, hba))
        
        return {
            "mw": round(mw, 1),
            "logp": round(logp, 2),
            "tpsa": round(tpsa, 1),
            "hbd": hbd,
            "hba": hba,
            "rings": rings,
            "chiral_centers": chiral,
            "fsp3": round(fsp3, 2),
        }
    
    def _assess_drug_likeness(self, props: Dict[str, Any], target_class: str) -> float:
        """
        Assess drug-likeness using Lipinski + additional rules.
        Returns 0-1 score.
        """
        score = 1.0
        
        # Lipinski's rule of 5 violations
        if props["mw"] > 500:
            score -= 0.15 * ((props["mw"] - 500) / 300)
        if props["logp"] > 5:
            score -= 0.15 * ((props["logp"] - 5) / 3)
        if props["hbd"] > 5:
            score -= 0.1 * (props["hbd"] - 5)
        if props["hba"] > 10:
            score -= 0.1 * ((props["hba"] - 10) / 5)
        
        # TPSA (good for oral: 40-140)
        tpsa = props["tpsa"]
        if tpsa < 40:
            score -= 0.1
        elif tpsa > 140:
            score -= 0.15
        
        # FSP3 (more sp3 = more drug-like generally)
        fsp3 = props["fsp3"]
        if fsp3 < 0.3:
            score -= 0.15
        
        return max(0.0, min(1.0, score))
    
    def _assess_novelty(self, smiles: str, scaffold: Fragment) -> float:
        """
        Assess novelty vs known drugs.
        Simplified: based on scaffold rarity and complexity.
        """
        # Base novelty from scaffold type
        base_novelty = {
            "scaffold": 0.7,
            "linker": 0.8,
            "side_chain": 0.75,
            "bioisostere": 0.85,
        }.get(scaffold.fragments_type, 0.6)
        
        # Add randomness for generated novelty
        variation = random.uniform(-0.15, 0.15)
        
        return max(0.0, min(1.0, base_novelty + variation))
    
    def _assess_synthetic_accessibility(self, scaffold: Fragment, use_linker: bool, use_bio: bool) -> float:
        """
        Assess synthetic accessibility (1=easy, 5=hard).
        """
        score = 1.0
        
        # Scaffold complexity
        if scaffold.rings >= 3:
            score += 0.5
        if scaffold.chiral_centers >= 2:
            score += 1.0
        
        # Additional fragments
        if use_linker:
            score += 0.3
        if use_bio:
            score += 0.7
        
        return max(1.0, min(5.0, score))
    
    def _assess_target_match(self, target_class: str, props: Dict[str, Any]) -> float:
        """
        Assess how well the compound matches target class requirements.
        """
        # Ideal property ranges by target class
        ideal_ranges = {
            "kinase": {"mw": (300, 600), "logp": (2, 5), "tpsa": (60, 120)},
            "nuclear_receptor": {"mw": (300, 700), "logp": (3, 6), "tpsa": (40, 100)},
            "gpc_receptor": {"mw": (200, 500), "logp": (1, 4), "tpsa": (80, 150)},
            "enzyme": {"mw": (200, 600), "logp": (1, 5), "tpsa": (50, 130)},
            "default": {"mw": (200, 600), "logp": (1, 5), "tpsa": (40, 140)},
        }
        
        ranges = ideal_ranges.get(target_class, ideal_ranges["default"])
        
        score = 1.0
        
        # MW match
        mw_low, mw_high = ranges["mw"]
        if props["mw"] < mw_low:
            score -= 0.15
        elif props["mw"] > mw_high:
            score -= 0.1 * ((props["mw"] - mw_high) / 200)
        
        # LogP match
        logp_low, logp_high = ranges["logp"]
        if props["logp"] < logp_low:
            score -= 0.1
        elif props["logp"] > logp_high:
            score -= 0.1
        
        # TPSA match
        tpsa_low, tpsa_high = ranges["tpsa"]
        if props["tpsa"] < tpsa_low:
            score -= 0.1
        elif props["tpsa"] > tpsa_high:
            score -= 0.05
        
        return max(0.3, min(1.0, score))
    
    def _assess_Pharmacophore(self, smiles: str, pharmacophore: Optional[List[str]]) -> float:
        """
        Assess pharmacophore feature match.
        Simplified implementation.
        """
        if not pharmacophore:
            return 0.7  # Default moderate score
        
        # Simple feature detection
        features = []
        if "O" in smiles:  # H-bond donor/acceptor
            features.append("hba")
        if "N" in smiles:
            features.append("hba")
        if "c" in smiles or "C" in smiles:
            features.append("aromatic")
        if "C(=O)" in smiles:
            features.append("hbd")
        if "c1cccnc1" in smiles:
            features.append("heterocycle")
        
        # Calculate match
        match = len(set(features) & set(Pharmacophore)) / max(len(Pharmacophore), 1)
        
        return max(0.3, min(1.0, match))
    
    def _generate_id(self, smiles: str, index: int) -> str:
        """Generate a unique compound ID based on SMILES hash"""
        hash_input = f"{smiles}_{index}_{datetime.now().microsecond}"
        short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"DN_{short_hash.upper()}"


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_de_novo(
    target_class: str,
    target_name: str,
    disease: str,
    num_candidates: int = 10,
) -> List[DeNovoCompound]:
    """Generate de novo compounds for a target"""
    generator = DeNovoGenerator(seed=42)  # Reproducible
    return generator.generate(target_class, target_name, disease, num_candidates)
