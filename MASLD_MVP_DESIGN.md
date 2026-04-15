# MASLD Disease Pack - MVP Design

## Disease Overview

**MASLD** (Metabolic dysfunction-associated steatotic liver disease)
- Formerly NAFLD (Non-alcoholic fatty liver disease)
- Spectrum: Steatosis → MASH → Fibrosis → Cirrhosis → HCC

## Biological Question

**MVP Question**: 
"What liver-relevant targets can reduce fibrosis progression while improving steatosis/inflammation?"

## Disease Axes

```
MASLD Spectrum
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Steatosis ──→ Inflammation ──→ Fibrosis ──→ Cirrhosis ──→ HCC
   ↓              ↓              ↓
 SREBP1c      NLRP3/        Stellate        Hepatocyte
 (lipid)       NFκB        cell (TGF-β)    transformation
              
Lipogenesis   Inflammasome   ECM            Malignant
                             remodeling      potential
```

## Target Priority Matrix

| Target | Gene | Steatosis | Inflammation | Fibrosis | Priority Score |
|--------|------|-----------|--------------|----------|---------------|
| **THR-β** | THRB | ★★★ | ★★ | ★★ | **0.871** |
| **FXR** | NR1H4 | ★★★ | ★★ | ★★ | **0.824** |
| **PPARA** | PPARA | ★★★ | ★★ | ★ | **0.854** |
| **GLP1R** | GLP1R | ★★★ | ★★ | ★★ | **0.798** |
| **SGLT2** | SLC5A2 | ★★ | ★★ | ★★ | **0.764** |
| **NLRP3** | NLRP3 | ★ | ★★★ | ★★ | **0.737** |
| **ACC** | ACACA | ★★★ | ★ | ★ | **0.712** |
| **SREBP1c** | SREBF1 | ★★★ | ★ | ★ | **0.705** |

## Weight Configuration

```python
MASLD_WEIGHTS = {
    "genetic_causality": 0.15,    # GWAS, eQTL evidence
    "disease_context": 0.20,         # Liver tissue specificity
    "perturbation_rescue": 0.20,     # MASH preclinical models
    "network_centrality": 0.10,     # Metabolic network position
    "druggability": 0.15,           # Small molecule tractability
    "safety": 0.15,                 # Metabolic organ safety
    "tissue_specificity": 0.20,      # Hepatocyte selectivity
    "translation": 0.10,            # Clinical biomarker linked
}
```

## Modality Routing

| Target Class | Example | Modality | Rationale |
|--------------|---------|----------|-----------|
| Nuclear Receptor | THR-β, FXR, PPARA | Small molecule | Nuclear penetration, oral |
| GPCR | GLP1R | Peptide/Small molecule | Metabolic hormone |
| Transporter | SGLT2 | Small molecule | Kidney-limited |
| Inflammasome | NLRP3 | Small molecule | Cytosolic target |
| Enzyme | ACC, DGAT | Small molecule | Catalytic site |

## Approved/Advanced Pipeline

| Drug | Target | Modality | Stage | Status |
|------|--------|----------|-------|--------|
| **Resmetirom** | THR-β | Small molecule | Phase III | ✅ FDA Approved 2024 |
| **Semaglutide** | GLP1R | Peptide | Phase III | ✅ FDA Approved 2025 |
| **Obeticholic acid** | FXR | Small molecule | Approved | ✅ NASH fibrosis |
| **Lanifibranor** | PPAR α/δ/γ | Small molecule | Phase III | NDA submitted |
| **Pegozafermin** | FGF21 | Biologic | Phase II | Ended |
| **Efruxifermin** | FGF21 | Biologic | Phase II | Ended |

## MVP Implementation Checklist

### Phase 1: Target Discovery
- [ ] Implement weight matrix
- [ ] Add THR-β, FXR, PPARA, GLP1R, SGLT2, NLRP3 targets
- [ ] Link to MASLD GWAS catalog
- [ ] Tissue specificity scoring (hepatocyte snRNA-seq)

### Phase 2: Evidence Integration
- [ ] Connect Resmetirom/Semaglutide trial data
- [ ] Fibrosis stage stratification
- [ ] Biomarker linkages (ALT, AST, HbA1c, NFS, FIB-4)

### Phase 3: Modality Routing
- [ ] Small molecule preference for nuclear receptors
- [ ] Peptide preference for GLP1R
- [ ] Hepatocyte delivery scoring

### Phase 4: Candidate Generation
- [ ] Retrieve known actives
- [ ] DE_NOVO generation for novel targets
- [ ] ADMET filtering
- [ ] Development roadmap

## Example Output

```yaml
MASLD Target Report
==================

Question: Fibrosis progression reduction + steatosis/inflammation improvement

Top 5 Targets:
1. THR-β (Score: 0.871)
   - Axis: Lipid metabolism, bile acid
   - Modality: Small molecule agonist
   - Evidence: Resmetirom FDA approved
   - Biomarkers: LDL-C, liver fat (MRS)
   
2. PPARA (Score: 0.854)
   - Axis: β-oxidation, lipophagy
   - Modality: Small molecule agonist
   - Evidence: Fenofibrate trials (mixed)
   - Biomarkers: Triglycerides, ALT
   
3. FXR (Score: 0.824)
   - Axis: Bile acid, glucose, fibrosis
   - Modality: Small molecule agonist/antagonist
   - Evidence: OCA approved (NASH)
   - Biomarkers: ALP, bilirubin

4. GLP1R (Score: 0.798)
   - Axis: Metabolic, inflammation
   - Modality: Peptide agonist (semaglutide)
   - Evidence: FDA approved (MASLD)
   - Biomarkers: HbA1c, weight, ALT

5. SGLT2 (Score: 0.764)
   - Axis: Metabolic, cardiorenal
   - Modality: Small molecule inhibitor
   - Evidence: Cardiorenal benefits
   - Biomarkers: HbA1c, eGFR, ALT

Development Recommendations:
- THR-β: First-line for lipogenesis
- GLP1R: Comorbidity benefit (obesity/diabetes)
- FXR: Anti-fibrotic axis
- Combination potential: THR-β + GLP1R
```

## Key Files to Create

```
disease_pack_masld/
├── __init__.py
├── ontology.py          # Disease definitions, stages
├── targets.py           # MASLD-specific targets + weights
├── tissue_weights.py    # Hepatocyte weighting
├── biomarkers.py        # ALT, AST, NFS, FIB-4, elastography
├── contraindications.py # Thyroid (THR-β), renal (SGLT2)
├── assays.py            # Lipid content, fibrosis scores
├── data_sources.py      # MASLD cohorts, liver snRNA-seq
└── modality_routes.py  # Small molecule > oligo > peptide
```

## Next Steps

1. Create `disease_pack_masld/targets.py`
2. Implement MASLD weight matrix
3. Add THR-β as index target
4. Run Engine 1 with MASLD question

---

*Document Version: 1.0*
*Generated: 2026-04-15*
*Status: MVP Draft*
