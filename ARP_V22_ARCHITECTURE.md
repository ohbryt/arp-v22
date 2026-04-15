# ARP v22 - Architecture Design

## Vision
A modular drug discovery pipeline with disease-specific biological question framing, target prioritization with modality routing, and candidate triage.

---

## 3-Engine Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ENGINE 1: Disease → Target               │
│                                                             │
│  INPUT                                                      │
│  ├── disease (e.g., MASLD, Sarcopenia, Lung Fibrosis)      │
│  ├── subtype (e.g., HFrEF vs HFpEF, IPF vs post-inflam)  │
│  ├── tissue context                                        │
│  └── biological question                                   │
│                                                             │
│  PROCESS                                                    │
│  ├── evidence ingestion (literature, genomics, preclinical)│
│  ├── target scoring (disease-specific weight matrix)       │
│  ├── network analysis                                      │
│  └── novelty assessment                                    │
│                                                             │
│  OUTPUT                                                     │
│  └── prioritized targets with evidence tables              │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                  ENGINE 2: Target → Modality               │
│                                                             │
│  INPUT                                                      │
│  ├── target biology (localization, class, tractability)  │
│  ├── tissue delivery requirements                          │
│  └── safety liabilities                                    │
│                                                             │
│  PROCESS                                                    │
│  ├── modality scoring (small mol, peptide, biologic, oligo)│
│  ├── assay strategy recommendation                         │
│  └── liability assessment                                   │
│                                                             │
│  OUTPUT                                                     │
│  └── modality recommendations per target                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│               ENGINE 3: Modality → Candidate               │
│                                                             │
│  INPUT                                                      │
│  ├── target + modality pair                               │
│  ├── chemical constraints                                  │
│  └── developability requirements                           │
│                                                             │
│  PROCESS                                                    │
│  ├── retrieval/generation                                   │
│  ├── ADMET prediction                                      │
│  ├── novelty scoring (DE_NOVO candidates)                  │
│  └── risk assessment                                       │
│                                                             │
│  OUTPUT                                                     │
│  ├── ranked shortlist                                     │
│  └── dossier (evidence, synthesis, risk)                   │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Modules

### Evidence Ingestion
- Literature mining (PubMed, semantic search)
- Genomics data (GWAS, eQTL, CRISPR screens)
- Preclinical evidence (animal models, cell assays)
- Clinical biomarkers (genetic associations)

### Target Scoring Engine
- Disease-specific weight matrices
- Network centrality analysis
- Tractability assessment
- Safety liability scoring

### Novelty Assessment
- Patent landscape
- Competitive pipeline
- Mechanism novelty (first-in-class vs fast-follower)
- DE_NOVO candidate generation

### Candidate Scoring
- ADMET prediction (blood-brain, hERG, CYP)
- Developability scoring
- Synthesis feasibility
- Risk classification

### Dossier Generator
- Target rationale
- Evidence summary
- Development roadmap
- Risk mitigation

---

## Disease Packs

Each disease pack contains:

```
disease_pack_{disease}/
├── __init__.py
├── ontology.py          # Disease definitions, subtypes
├── targets.py          # Target priors, weight matrix
├── tissue_weights.py    # Tissue-specific scoring
├── biomarkers.py       # Clinical biomarker mappings
├── contraindications.py # Safety flags, liability penalties
├── assays.py           # Assay templates, readouts
├── data_sources.py     # Required datasets
└── modality_routes.py  # Disease-specific modality preferences
```

### Disease Pack: MASLD
- **Subtypes**: Simple steatosis, MASH, fibrosis stages F1-F4
- **Axes**: Lipogenesis, inflammation, fibrosis
- **Priority targets**: THR-β, FXR, PPARA, GLP1R, NLRP3, SGLT2
- **Modality**: Small molecule > Liver-targeted oligo
- **Key biomarkers**: ALT, AST, HbA1c, fibrosis scores

### Disease Pack: Sarcopenia
- **Subtypes**: Aging-related, cachexia, disuse
- **Axes**: Anabolism, catabolism, mitochondrial, neuromuscular
- **Priority targets**: MTOR, FOXO1/3, AMPK, MYOD1, MSTN
- **Modality**: Small molecule > Peptide > Biologic
- **Key biomarkers**: Muscle mass (DXA), strength, frailty scores

### Disease Pack: Lung Fibrosis
- **Subtypes**: IPF, post-inflammatory, autoimmune-related
- **Axes**: Fibroblast activation, epithelial repair, ECM
- **Priority targets**: TGF-β, COL1A1, MMP7, integrin αvβ6
- **Modality**: Small molecule > Inhaled > Biologic
- **Key biomarkers**: FVC, DLCO, HRCT scores

### Disease Pack: Heart Failure
- **Subtypes**: HFrEF, HFpEF, RV failure
- **Axes**: Remodeling, fibrosis, contractility, metabolism
- **Priority targets**: SGLT2, ARNI, MCR2, NFKB1
- **Modality**: Small molecule > Biologic
- **Key biomarkers**: EF, NT-proBNP, hospitalization

### Disease Pack: Cancer
- **Subtypes**: NSCLC EGFR-mutant (index), CRC, TNBC
- **Axes**: Oncogenic dependency, resistance, immune evasion
- **Priority targets**: EGFR, ALK, ROS1, MET
- **Modality**: Small molecule (TKI) > ADC > Biologic
- **Key biomarkers**: Mutation status, ctDNA, PD-L1

---

## Data Sources by Disease

| Disease | Required Datasets | Priority |
|---------|-----------------|---------|
| **MASLD** | Liver snRNA-seq, fibrosis cohorts, lipidomics | Tier 1 |
| **Sarcopenia** | Muscle bulk/scRNA-seq, aging cohorts, frailty data | Tier 1 |
| **Lung Fibrosis** | IPF scRNA-seq, fibroblast subpopulations | Tier 1 |
| **Heart Failure** | Heart snRNA-seq, HFrEF/HFpEF cohorts | Tier 2 |
| **Cancer** | NSCLC cohorts, CRISPR screens, mutation databases | Tier 2 |

---

## Implementation Roadmap

### Phase 1: Foundation (ARP v22.1)
- [ ] Core scoring engine
- [ ] Disease pack structure
- [ ] MASLD pack implementation
- [ ] Engine 1 complete for MASLD

### Phase 2: Modality (ARP v22.2)
- [ ] Engine 2: Target → Modality
- [ ] Modality scoring matrix
- [ ] Assay recommendations

### Phase 3: Candidates (ARP v22.3)
- [ ] Engine 3: Candidate generation
- [ ] ADMET integration
- [ ] Dossier generator

### Phase 4: Expansion (ARP v22.4+)
- [ ] Sarcopenia pack
- [ ] Lung fibrosis pack
- [ ] Heart failure pack
- [ ] Cancer pack (NSCLC EGFR)

---

## File Structure

```
arp-v22/
├── core/
│   ├── __init__.py
│   ├── scoring_engine.py
│   ├── evidence_ingestion.py
│   ├── novelty_assessment.py
│   ├── candidate_scorer.py
│   └── dossier_generator.py
│
├── engines/
│   ├── engine1_disease_to_target.py
│   ├── engine2_target_to_modality.py
│   └── engine3_modality_to_candidate.py
│
├── disease_packs/
│   ├── __init__.py
│   ├── base_disease_pack.py
│   ├── masld/
│   │   ├── ontology.py
│   │   ├── targets.py
│   │   ├── tissue_weights.py
│   │   ├── biomarkers.py
│   │   ├── contraindications.py
│   │   └── modality_routes.py
│   ├── sarcopenia/
│   ├── lung_fibrosis/
│   ├── heart_failure/
│   └── cancer/
│
├── data/
│   ├── target_db/
│   ├── compound_db/
│   └── evidence_db/
│
├── utils/
│   ├── network_analysis.py
│   ├── admet_predictor.py
│   └── literature_miner.py
│
├── cli.py
├── pipeline.py
├── config.py
└── main.py
```

---

## Quality Gates

Each engine has exit criteria:

### Engine 1 Exit
- [ ] ≥10 prioritized targets
- [ ] Evidence table with citations
- [ ] Score breakdown per target
- [ ] Novelty assessment complete

### Engine 2 Exit
- [ ] Modality recommendation per target
- [ ] Assay strategy defined
- [ ] Liability flags raised
- [ ] Risk classification assigned

### Engine 3 Exit
- [ ] Top 10 candidates ranked
- [ ] ADMET profiles generated
- [ ] Development roadmap drafted
- [ ] Dossier complete

---

## Example Output: MASLD

### Engine 1: Disease → Target
```
TARGET PRIORITIZATION FOR MASLD
================================

1. THRβ (THRB)
   - Score: 0.871
   - Evidence: GWAS (LDL), MASH trials (resmetirom)
   - Modality Fit: Small molecule agonist
   
2. FXR (NR1H4)
   - Score: 0.824
   - Evidence: Obeticholic acid approval
   - Modality Fit: Small molecule agonist
   
3. PPARA (NR1C3)
   - Score: 0.854
   - Evidence: Fenofibrate trials
   - Modality Fit: Small molecule agonist

...
```

### Engine 2: Target → Modality
```
MODALITY ROUTING FOR THRβ
==========================

Recommended: Small molecule (★★★)
Alternative: Liver-targeted oligo (★★)

Assay Strategy:
- TR-FRET for agonist activity
- Hepatocyte lipid content (Nile red)
- FGF21 secretion biomarker

Liability Flags:
- CYP3A4 induction risk
- Thyroid axis (T3/T4 monitoring)

Development: 3-5 years to IND
```

### Engine 3: Modality → Candidate
```
CANDIDATE RANKING FOR THRβ AGONISTS
====================================

1. Resmetirom (MGL-3196)
   - Score: 0.92
   - Status: Phase III, FDA approved
   - ADMET: Oral, low hERG risk
   - Development: Fast-follower space

2. ASC-41
   - Score: 0.87
   - Status: Phase II
   - ADMET: Oral, liver-targeted
   
3. TERN-101
   - Score: 0.82
   - Status: Phase II
   - ADMET: FXR agonist, combination potential

...
```

---

## Key Differentiators from ARP v21

| Feature | ARP v21 | ARP v22 |
|---------|---------|---------|
| Disease specificity | Generic | Disease packs with weights |
| Target scoring | Single matrix | Disease-specific matrices |
| Modality routing | Not implemented | Engine 2 |
| Output | Ranked compounds | Dossier with roadmap |
| Evidence | Literature-based | Genomics + literature |
| Novelty | Hash-based | Patent + mechanism analysis |

---

## Next Immediate Action

Create MASLD disease pack as proof-of-concept:
1. Define ontology (steatosis → MASH → fibrosis)
2. Implement target weight matrix
3. Add THR-β, FXR, PPARA, GLP1R targets
4. Run Engine 1 for MASLD

---

*Document Version: 1.0*
*Generated: 2026-04-15*
*Status: Draft for Review*
