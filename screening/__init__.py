"""
ARP v22 - Screening Module

Virtual screening methods:
- QSAR (Chemprop - directed message passing neural network)
- Docking (AutoDock Vina, GNINA, DiffDock)

Usage:
    python -m screening --method qsar --targets data/targets.parquet --library data/compounds.parquet
    python -m screening --method vina --targets data/targets.parquet --library data/compounds.parquet
"""

__version__ = "1.0.0"

__all__ = [
    "QSARScreener",
    "VinaScreener",
    "run_screening",
]

from .qsar import QSARScreener
from .docking import VinaScreener


def run_screening(
    method: str,
    targets: str,
    library: str,
    output: str = "data/screening_hits.parquet",
    **kwargs,
) -> bool:
    """
    Run virtual screening.
    
    Args:
        method: "qsar", "vina", or "consensus"
        targets: Path to targets parquet
        library: Path to compound library
        output: Output path for hits
        **kwargs: Method-specific parameters
    """
    if method.lower() == "qsar":
        screener = QSARScreener(**kwargs)
        return screener.screen(targets, library, output)
    elif method.lower() == "vina":
        screener = VinaScreener(**kwargs)
        return screener.screen(targets, library, output)
    elif method.lower() == "consensus":
        # Run both and combine
        qsar = QSARScreener(**kwargs)
        vina = VinaScreener(**kwargs)
        
        qsar_output = output.replace(".parquet", "_qsar.parquet")
        vina_output = output.replace(".parquet", "_vina.parquet")
        
        qsar_ok = qsar.screen(targets, library, qsar_output)
        vina_ok = vina.screen(targets, library, vina_output)
        
        if qsar_ok and vina_ok:
            import pandas as pd
            qsar_df = pd.read_parquet(qsar_output)
            vina_df = pd.read_parquet(vina_output)
            
            combined = qsar_df.merge(
                vina_df[["candidate_id", "vina_score"]],
                on="candidate_id",
                how="outer",
                suffixes=("", "_vina")
            )
            
            if "pchembl_value" in combined.columns and "vina_score" in combined.columns:
                combined["qsar_norm"] = (combined["pchembl_value"] - combined["pchembl_value"].min()) / (combined["pchembl_value"].max() - combined["pchembl_value"].min() + 1e-10)
                combined["vina_norm"] = 1 - (combined["vina_score"] - combined["vina_score"].min()) / (combined["vina_score"].max() - combined["vina_score"].min() + 1e-10)
                combined["consensus_score"] = (combined["qsar_norm"] + combined["vina_norm"]) / 2
                
                combined.to_parquet(output, index=False)
                return True
        
        return False
    else:
        raise ValueError(f"Unknown method: {method}")
