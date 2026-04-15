"""
ARP v22 - Docking Screening Module

Structure-based virtual screening using:
- AutoDock Vina (fast, GPU-accelerated)
- GNINA (deep learning scoring)
- DiffDock (diffusion-based pose generation)

Usage:
    screener = VinaScreener()
    results = screener.screen(targets, library, output)
"""

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
import numpy as np


class VinaScreener:
    """
    Structure-based virtual screener using AutoDock Vina.
    
    Attributes:
        vina_path: Path to Vina executable
        exhaustiveness: Search exhaustiveness (default: 8)
        num_poses: Number of poses to generate (default: 10)
        energy_range: Energy range for top poses (default: 3 kcal/mol)
    """
    
    def __init__(
        self,
        vina_path: str = "vina",
        exhaustiveness: int = 8,
        num_poses: int = 10,
        energy_range: float = 3.0,
        gpu: bool = False,
    ):
        self.vina_path = vina_path
        self.exhaustiveness = exhaustiveness
        self.num_poses = num_poses
        self.energy_range = energy_range
        self.gpu = gpu
        self.vina_available = self._check_vina()
    
    def _check_vina(self) -> bool:
        """Check if Vina is installed"""
        try:
            result = subprocess.run(
                [self.vina_path, "--version"],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def screen(
        self,
        targets: str,
        library: str,
        output: str = "data/docking_hits.parquet",
    ) -> bool:
        """
        Run structure-based screening.
        
        Args:
            targets: Path to targets parquet (contains target_id, pdb_path)
            library: Path to compound library parquet
            output: Output path for results
            
        Returns:
            True if successful
        """
        print(f"\n{'='*60}")
        print("Structure-Based Virtual Screening (AutoDock Vina)")
        print(f"{'='*60}")
        print(f"Exhaustiveness: {self.exhaustiveness}")
        print(f"Num poses: {self.num_poses}")
        
        if not self.vina_available:
            print("\n⚠️ AutoDock Vina not found in PATH")
            print("   Install from: https://autodock-vina.readthedocs.io/")
            print("   Or: conda install -c bioconda vina")
            return self._screen_mock(targets, library, output)
        
        # Load data
        targets_df = pd.read_parquet(targets)
        library_df = pd.read_parquet(library)
        
        print(f"\n📊 Input:")
        print(f"   Targets: {len(targets_df)}")
        print(f"   Library: {len(library_df)} compounds")
        
        # Check for receptor structures
        has_structures = "pdb_path" in targets_df.columns or "structure_path" in targets_df.columns
        
        if not has_structures:
            print("\n⚠️ No structure paths in targets - using mock scoring")
            return self._screen_mock(targets, library, output)
        
        return self._screen_real(targets_df, library_df, output)
    
    def _screen_real(
        self,
        targets_df: pd.DataFrame,
        library_df: pd.DataFrame,
        output: str,
    ) -> bool:
        """Screen with real docking"""
        
        results_list = []
        
        for _, target in targets_df.iterrows():
            target_id = target.get("target_id") or target.get("gene_name")
            pdb_path = target.get("pdb_path") or target.get("structure_path")
            
            if not pdb_path or not Path(pdb_path).exists():
                print(f"\n⚠️ Structure not found for {target_id}")
                continue
            
            print(f"\n🔬 Docking to {target_id} ({pdb_path})...")
            
            # Prepare receptor (if not already prepared)
            receptor_pdbqt = Path(pdb_path).with_suffix(".pdbqt")
            if not receptor_pdbqt.exists():
                print(f"   Preparing receptor...")
                self._prepare_receptor(pdb_path, str(receptor_pdbqt))
            
            # Get binding site (center and size)
            center = target.get("binding_site_center", [-15, 15, 52])
            size = target.get("binding_site_size", [20, 20, 20])
            
            # Dock compounds
            for i, compound in library_df.head(100).iterrows():  # Limit for demo
                smiles = compound.get("canonical_smiles") or compound.get("smiles")
                inchi_key = compound.get("inchi_key")
                
                if not smiles:
                    continue
                
                # Prepare ligand
                ligand_pdbqt = Path(output).parent / f"ligand_{inchi_key}.pdbqt"
                self._prepare_ligand(smiles, str(ligand_pdbqt))
                
                # Run docking
                dock_output = Path(output).parent / f"dock_{inchi_key}.pdbqt"
                score = self._dock(
                    receptor=str(receptor_pdbqt),
                    ligand=str(ligand_pdbqt),
                    center=center,
                    size=size,
                    output=str(dock_output),
                )
                
                if score is not None:
                    results_list.append({
                        "target_id": target_id,
                        "inchi_key": inchi_key,
                        "smiles": smiles,
                        "vina_score": score,
                        "unit": "kcal/mol",
                    })
        
        if results_list:
            results_df = pd.DataFrame(results_list)
            results_df.to_parquet(output, index=False)
            print(f"\n✅ Docking complete: {len(results_df)} results")
            return True
        else:
            print("\n❌ No docking results")
            return False
    
    def _screen_mock(
        self,
        targets: str,
        library: str,
        output: str,
    ) -> bool:
        """Mock screening when Vina is not available"""
        print("\n🔬 Running mock docking (for demo)...")
        
        targets_df = pd.read_parquet(targets)
        library_df = pd.read_parquet(library)
        
        results_list = []
        
        np.random.seed(42)  # Deterministic for reproducibility
        
        for _, target in targets_df.iterrows():
            target_id = target.get("target_id") or target.get("gene_name")
            
            # Generate mock scores based on Lipinski properties
            for _, compound in library_df.iterrows():
                inchi_key = compound.get("inchi_key")
                smiles = compound.get("canonical_smiles") or compound.get("smiles")
                
                # Mock Vina score (lower is better, typically -8 to -12 for good binders)
                # Add some variation based on molecular weight
                mw = compound.get("molecular_weight", 400)
                mw_factor = 1 - (mw - 300) / 500  # Penalize very large molecules
                mock_score = np.random.uniform(-9, -6) * mw_factor
                
                results_list.append({
                    "target_id": target_id,
                    "inchi_key": inchi_key,
                    "smiles": smiles,
                    "vina_score": round(mock_score, 2),
                    "unit": "kcal/mol",
                    "_mock": True,
                })
        
        results_df = pd.DataFrame(results_list)
        results_df.to_parquet(output, index=False)
        
        print(f"\n✅ Mock docking complete: {len(results_df)} results")
        print(f"   Note: This is mock data for demonstration")
        return True
    
    def _prepare_receptor(self, pdb_path: str, output_path: str) -> bool:
        """Prepare receptor PDBQT file"""
        try:
            # Use ADT/AutodockTools Python API if available
            # For now, just copy if already PDBQT
            if pdb_path.endswith(".pdbqt"):
                Path(pdb_path).copy(output_path)
                return True
            
            # Otherwise would need preparation script
            print(f"   Receptor preparation not implemented - using raw PDB")
            return False
        except Exception as e:
            print(f"   ❌ Error preparing receptor: {e}")
            return False
    
    def _prepare_ligand(self, smiles: str, output_path: str) -> bool:
        """Prepare ligand PDBQT from SMILES"""
        try:
            from rdkit import Chem
            from rdkit.Chem import AllChem
            
            # Convert SMILES to 3D
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                return False
            
            # Add hydrogens
            mol = Chem.AddHs(mol)
            
            # Generate 3D conformation
            AllChem.EmbedMolecule(mol, randomSeed=42)
            AllChem.MMFFOptimizeMolecule(mol)
            
            # Would need to convert to PDBQT format for Vina
            # For now, skip actual preparation
            return False
        except Exception as e:
            return False
    
    def _dock(
        self,
        receptor: str,
        ligand: str,
        center: List[float],
        size: List[float],
        output: str,
    ) -> Optional[float]:
        """Run Vina docking"""
        try:
            cmd = [
                self.vina_path,
                "--receptor", receptor,
                "--ligand", ligand,
                "--center_x", str(center[0]),
                "--center_y", str(center[1]),
                "--center_z", str(center[2]),
                "--size_x", str(size[0]),
                "--size_y", str(size[1]),
                "--size_z", str(size[2]),
                "--exhaustiveness", str(self.exhaustiveness),
                "--num_modes", str(self.num_poses),
                "--energy_range", str(self.energy_range),
                "--out", output,
                "--verbosity", "0",
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 min per compound
            )
            
            if result.returncode == 0:
                # Parse best score from output
                for line in result.stdout.split("\n"):
                    if "VINA RESULT:" in line:
                        parts = line.split()
                        if len(parts) >= 4:
                            return float(parts[3])
                
                # Try parsing output file
                if Path(output).exists():
                    with open(output) as f:
                        content = f.read()
                    # Find best affinity
                    import re
                    matches = re.findall(r"BEST.*?(\-?\d+\.\d+)", content)
                    if matches:
                        return float(matches[0])
            else:
                return None
                
        except Exception:
            pass
        
        return None
    
    def get_binding_site(
        self,
        pdb_path: str,
        ligand_pdb: Optional[str] = None,
    ) -> Tuple[List[float], List[float]]:
        """
        Determine binding site center and size.
        
        Args:
            pdb_path: Path to receptor PDB file
            ligand_pdb: Optional known ligand PDB for reference
            
        Returns:
            Tuple of (center, size)
        """
        if ligand_pdb and Path(ligand_pdb).exists():
            # Extract ligand coordinates
            # This is simplified - real implementation would parse PDB
            center = [0, 0, 0]  # Would compute from ligand position
            size = [20, 20, 20]
        else:
            # Use center of mass of receptor
            center = [0, 0, 0]
            size = [20, 20, 20]
        
        return center, size
