# ARP v22 - Production Drug Discovery Pipeline

**Version**: 22.2.0  
**Status**: Foundation + Data Ingest + Screening MVP  
**Architecture**: 3-Engine + Data Contracts + Virtual Screening

---

## Overview

ARP v22 is a production-ready drug discovery pipeline with:

1. **Engine 1**: Disease → Target (target prioritization)
2. **Engine 2**: Target → Modality (modality routing)
3. **Engine 3**: Modality → Candidate (candidate generation)
4. **Data Ingest**: ChEMBL, PubChem, UniProt ingestion
5. **Virtual Screening**: QSAR (Chemprop) + Docking (AutoDock Vina)
6. **Data Contracts**: JSON Schema + CI validation + DVC pipelines

---

## Quick Start

```bash
cd /Users/ocm/.openclaw/workspace/arp-v22

# Run target prioritization
python3 -c "from pipeline import run_pipeline; r = run_pipeline('masld', 5)"

# Run data ingestion
python3 -m ingest.chembl --version 34 --output data/chembl.parquet

# Run QSAR screening
python3 -m screening --method qsar --targets data/targets.parquet --library data/compounds.parquet

# Validate pipeline output
python3 validate_pipeline.py --run-dir runs/2026-04-15_masld_run01
```

---

## Project Structure

```
arp-v22/
├── core/                           # Core engines
│   ├── scoring_engine.py           # Engine 1: Target prioritization
│   ├── modality_routing.py         # Engine 2: Modality routing
│   ├── candidate_engine.py         # Engine 3: Candidate generation
│   ├── de_novo_generator.py       # De novo compound generation
│   ├── literature_integrator.py     # PubMed/ClinicalTrials integration
│   └── dashboard.py               # HTML report generation
│
├── ingest/                         # Data ingestion
│   ├── chembl.py                   # ChEMBL REST API client
│   ├── pubchem.py                  # PubChem PUG REST client
│   └── uniprot.py                  # UniProt REST client
│
├── screening/                      # Virtual screening
│   ├── qsar.py                    # QSAR (Chemprop/RDKit)
│   └── docking.py                  # AutoDock Vina
│
├── schemas/                        # Data contracts
│   └── definitions.py             # JSON Schema definitions
│
├── dvc.yaml                        # DVC pipeline config
├── config.py                       # Configuration
├── validate_pipeline.py             # CI validation gate
├── pipeline.py                    # Main orchestrator
├── cli.py                          # CLI entry point
└── README.md
```

---

## Data Contracts (P0)

### JSON Schema Validation

All pipeline outputs are validated against schemas:

| Schema | Description |
|--------|-------------|
| `TargetSchema` | Drug target with scores and evidence |
| `CompoundSchema` | Chemical compound with properties |
| `AssaySchema` | Assay results |
| `CandidateScoreSchema` | Ranked candidate with all scores |
| `ManifestSchema` | Run manifest with provenance |

### Manifest Example

```json
{
  "run_id": "2026-04-15_masld_abc12345",
  "git_commit": "abc1234",
  "data_snapshots": {
    "chembl": "34@sha256:...",
    "uniprot": "2024_01"
  },
  "models": {
    "qsar": "chemprop_v1@sha256:..."
  },
  "params": {
    "screening.method": "consensus",
    "admet.thresholds.logp_max": 5.0
  }
}
```

---

## Data Ingestion (P0)

### ChEMBL
```python
from ingest import ChEMBLClient

client = ChEMBLClient()
client.ingest(
    version="34",
    target_genes=["THRB", "NR1H4", "PPARA"],
    output="data/chembl_activities.parquet"
)
```

### PubChem
```python
from ingest import PubChemClient

client = PubChemClient()
client.fetch_by_inchikey("XXXXXXXXXXXXXX")
```

### UniProt
```python
from ingest import UniProtClient

client = UniProtClient()
client.ingest(
    genes=["THRB", "NR1H4", "PPARA"],
    output="data/uniprot_proteins.parquet"
)
```

---

## Virtual Screening (P1)

### QSAR Screening
```python
from screening import QSARScreener

screener = QSARScreener(
    model_path="models/qsar_model.pt",
    confidence_threshold=0.7
)
screener.screen(
    targets="data/targets.parquet",
    library="data/compounds.parquet",
    output="data/qsar_hits.parquet"
)
```

### Docking
```python
from screening import VinaScreener

screener = VinaScreener(
    exhaustiveness=8,
    num_poses=10
)
screener.screen(
    targets="data/targets.parquet",
    library="data/compounds.parquet",
    output="data/docking_hits.parquet"
)
```

---

## DVC Pipeline

```bash
# Run full pipeline
dvc repro

# Run specific stage
dvc repro target_prioritization

# Compare metrics
dvc metrics diff
```

---

## CI Validation Gate

```bash
# Validate a run
python3 validate_pipeline.py --run-dir runs/2026-04-15_masld_run01

# Exit codes
# 0: Validation passed
# 1: Validation failed
# 2: Warnings only (with --strict: treated as failure)
```

---

## Disease Packs (5 Diseases)

| Disease | Targets | Status |
|---------|---------|--------|
| MASLD | 10 | ✅ |
| Sarcopenia | 10 | ✅ |
| Lung Fibrosis | 8 | ✅ |
| Heart Failure | 8 | ✅ |
| Cancer (NSCLC) | 8 | ✅ |

---

## Recommended Tools

| Tool | Purpose | Install |
|------|---------|---------|
| **Chemprop** | D-MPNN QSAR | `pip install chemprop` |
| **AutoDock Vina** | Docking | `conda install -c bioconda vina` |
| **RDKit** | Molecular descriptors | `conda install -c rdkit rdkit` |
| **DVC** | Data versioning | `pip install dvc` |
| **MLflow** | Experiment tracking | `pip install mlflow` |

---

## Development Status

| Component | Status | Version |
|-----------|--------|---------|
| Engine 1 (Target Prioritization) | ✅ Complete | v22.0 |
| Engine 2 (Modality Routing) | ✅ Complete | v22.0 |
| Engine 3 (Candidate Generation) | ✅ Complete | v22.0 |
| JSON Schema + Validation | ✅ Complete | v22.2 |
| DVC Pipeline Config | ✅ Complete | v22.2 |
| ChEMBL Ingestion | ✅ Complete | v22.2 |
| PubChem Ingestion | ✅ Complete | v22.2 |
| UniProt Ingestion | ✅ Complete | v22.2 |
| QSAR Screening | ✅ Complete | v22.2 |
| Vina Docking | ✅ Complete | v22.2 |
| Literature Integration | ✅ Complete | v22.1 |
| De Novo Generation | ✅ Complete | v22.1 |
| Dashboard/Reports | ✅ Complete | v22.1 |

---

## Implementation Roadmap

Based on Deep Research MVP Expansion Report:

| Phase | Duration | Priority | Goal |
|-------|----------|----------|------|
| Foundation | 2-3 weeks | P0 | Data contracts + DVC + CI |
| Data Ingest v1 | 2-4 weeks | P0 | ChEMBL + PubChem + UniProt |
| Screening MVP | 3-5 weeks | P1 | Chemprop + Vina |
| ADMET Gate | 2-3 weeks | P1 | PAINS + ADMET filters |
| Generative v1 | 4-6 weeks | P2 | REINVENT 4 |

---

## Key References

### Databases & Licensing
- ChEMBL (CC BY-SA 3.0)
- PubChem (Public Domain)
- UniProt (CC BY 4.0)
- PDB (CC0 1.0)
- AlphaFold (CC BY 4.0)

### Tools & Papers
- Chemprop: Liu et al. (2021) J Chem Inf Model
- AutoDock Vina: Trott & Olson (2010) J Comput Chem
- GNINA: McNutt et al. (2021) J Cheminform
- DiffDock: Corso et al. (2022) NeurIPS

---

*Document Version: 3.0*
*Last Updated: 2026-04-15*
