# Sarcopenia Disease Pack - MVP Design

## Disease Overview

**Sarcopenia**: Age-related loss of skeletal muscle mass and function
- Primary (aging-related): anabolic resistance, mitochondrial dysfunction
- Secondary: disuse, disease (cancer cachexia, CHF)

## Biological Question

**MVP Question**: 
"What muscle-specific tractable targets can improve muscle function decline?"

## Disease Axes

```
Sarcopenia Biology
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Anabolic Resistance ←→ Catabolic Activation
      ↓                    ↓
   mTORC1              FOXO1/3
   (protein syn)       (Ubiquitin-proteasome)
                      Muscle atrophy
   
Mitochondrial ←→ Satellite Cell ←→ Inflammation
 Dysfunction     Dysfunction        (NLRP3, NFκB)
      ↓                ↓                 ↓
  ATP depletion    Muscle stem       Cytokine-mediated
                   cell decline      muscle wasting
```

## Target Priority Matrix

| Target | Gene | Anabolism | Catabolism | Mitoch. | Function | Priority Score |
|--------|------|-----------|------------|---------|----------|---------------|
| **MTOR** | MTOR | ★★★ | ★ | ★★ | ★★ | **0.847** |
| **FOXO1/3** | FOXO1 | ★ | ★★★ | ★★ | ★★★ | **0.828** |
| **AMPK** | PRKAA1 | ★★ | ★★ | ★★★ | ★★ | **0.796** |
| **MSTN** | MSTN | ★★ | ★★★ | ★ | ★★★ | **0.824** |
| **AKT1** | AKT1 | ★★★ | ★ | ★★ | ★★ | **0.794** |
| **MYOD1** | MYOD1 | ★★ | ★ | ★ | ★★★ | **0.776** |
| **SIRT1** | SIRT1 | ★★ | ★★ | ★★★ | ★★ | **0.729** |
| **PGC1A** | PPARGC1A | ★★ | ★ | ★★★ | ★★ | **0.719** |

## Weight Configuration

```python
SARCOPENIA_WEIGHTS = {
    "genetic_causality": 0.15,     # GWAS, muscle strength heritability
    "disease_context": 0.10,        # Muscle tissue context
    "perturbation_rescue": 0.25,   # KO/KD rescue in preclinical (CRITICAL)
    "network_centrality": 0.10,    # mTOR/AMPK/FOXO network
    "druggability": 0.15,          # Kinase, enzyme tractability
    "safety": 0.20,               # Chronic administration safety (CRITICAL)
    "tissue_specificity": 0.20,    # Skeletal muscle selectivity (CRITICAL)
    "translation": 0.10,          # Functional endpoint linkage
}
```

## Modality Routing

| Target Class | Example | Modality | Rationale |
|--------------|---------|----------|-----------|
| Kinase | MTOR, AMPK, AKT | Small molecule | Oral, chronic |
| Transcription Factor | FOXO1/3, MYOD1 | Small molecule | Nuclear penetration |
| Myostatin axis | MSTN, ACVR2B | Biologic (antibody) | Extracellular, large |
| Sirtuin | SIRT1 | Small molecule (resveratrol) | NAD+ dependent |
| Mitochondrial | PGC1A | Small molecule | Mitochondrial targets |

## Approved/Advanced Pipeline

| Drug | Target | Modality | Stage | Status |
|------|--------|----------|-------|--------|
| **Biomark** | Myostatin Ab | Biologic | Phase II/III | Sarcopenia/cancer |
| **Apitegromab** | MSTN | Biologic | Phase II | SMA |
| **Reldesemtiv** | Fast troponin | Small molecule | Phase II | ALS (futility) |
| **Captomorf** | mTORC1 | Small molecule | Preclinical | Sarcopenia |
| **Sarm Spartalizumab** | MSTN | Biologic | Phase I | Sarcopenia |

## MVP Implementation Checklist

### Phase 1: Target Discovery
- [ ] Implement weight matrix
- [ ] Add MTOR, FOXO1/3, AMPK, MSTN, MYOD1 targets
- [ ] Link to muscle strength GWAS
- [ ] Skeletal muscle snRNA-seq weighting

### Phase 2: Evidence Integration
- [ ] Preclinical rescue data (mTOR inhibition, FOXO KO)
- [ ] Muscle mass vs function distinction
- [ ] Biomarker linkages (DXA, grip strength, SPPB)

### Phase 3: Modality Routing
- [ ] Small molecule preference (chronic oral)
- [ ] Biologic for myostatin axis
- [ ] Tissue specificity scoring

### Phase 4: Candidate Generation
- [ ] Retrieve known actives (rapamycin, resveratrol)
- [ ] DE_NOVO for novel scaffolds
- [ ] Safety filtering (immunosuppression risk)
- [ ] Development roadmap

## Example Output

```yaml
Sarcopenia Target Report
=======================

Question: Muscle function improvement in age-related sarcopenia

Top 5 Targets:
1. MTOR (Score: 0.847)
   - Axis: Anabolic protein synthesis
   - Modality: Small molecule inhibitor
   - Evidence: Rapamycin preclinical, longevity
   - Limitation: Immunosuppression risk
   - Biomarkers: Muscle protein synthesis (D3-creatine)
   
2. FOXO1/3 (Score: 0.828)
   - Axis: Atrogen activation, ubiquitin-proteasome
   - Modality: Small molecule
   - Evidence: FOXO1/3 KO in mice preserves muscle
   - Challenge: Nuclear transcription factor
   - Biomarkers: Atrogen expression (MuRF1, MAFbx)

3. MSTN (Score: 0.824)
   - Axis: Negative regulator of muscle growth
   - Modality: Biologic (antibody)
   - Evidence: Bimagrumab Phase II/III
   - Advantage: Muscle-selective
   - Biomarkers: Myostatin levels, muscle mass (DXA)

4. AMPK (Score: 0.796)
   - Axis: Energy sensor, mitochondrial biogenesis
   - Modality: Small molecule activator
   - Evidence: AICAR, metformin preclinical
   - Advantage: Metabolic benefits
   - Biomarkers: AMPK activation, mitochondrial markers

5. AKT1 (Score: 0.794)
   - Axis: Muscle hypertrophy signaling
   - Modality: Small molecule
   - Evidence: AKT1 overexpression in mice
   - Challenge: Cancer risk (mTOR pathway)
   - Biomarkers: Phospho-AKT, muscle protein synthesis

Functional Endpoint Mapping:
- Muscle mass: DXA, BIA → MTOR, MSTN, AKT1
- Muscle strength: Grip strength, SPPB → FOXO1/3, MYOD1
- Physical performance: Gait speed, chair stand → AMPK, SIRT1

Development Recommendations:
- MSTN antibody: Best safety/efficacy profile
- MTOR: Repurpose from longevity (metformin combo?)
- AMPK: Metabolic comorbidity benefit
```

## Key Files to Create

```
disease_pack_sarcopenia/
├── __init__.py
├── ontology.py          # Disease definitions, subtypes
├── targets.py           # Sarcopenia-specific targets + weights
├── tissue_weights.py    # Skeletal muscle weighting
├── biomarkers.py        # DXA, grip strength, SPPB, frailty
├── contraindications.py # Immunosuppression, cancer risk
├── assays.py            # Protein synthesis, atrogen expression
├── data_sources.py      # Muscle snRNA-seq, aging cohorts
└── modality_routes.py  # Small molecule > Biologic
```

## Next Steps

1. Create `disease_pack_sarcopenia/targets.py`
2. Implement Sarcopenia weight matrix
3. Add MSTN as index target (biologic)
4. Run Engine 1 with Sarcopenia question

---

*Document Version: 1.0*
*Generated: 2026-04-15*
*Status: MVP Draft*
