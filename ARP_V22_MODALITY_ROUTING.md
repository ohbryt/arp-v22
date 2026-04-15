# ARP v22 - Disease Modality Routing Matrix

## Overview
Modality recommendations for each disease indication based on target class, tissue localization, and development feasibility.

---

## Modality Definitions

| Modality | Characteristics | Development Timeline | Typical Indications |
|----------|---------------|---------------------|-------------------|
| **Small Molecule** | Oral bioavailability, good tissue penetration, off-target risk | 5-7 years | Most metabolic, CV, fibrotic diseases |
| **Peptide** | High selectivity, poor oral bioavailability, injectable | 7-10 years | Hormonal targets, metabolic peptides |
| **Biologic/Antibody** | High specificity, large分子, poor CNS penetration | 8-12 years | Extracellular targets, immune modulation |
| **Oligo/siRNA** | Gene silencing, liver-targeted delivery, stable | 8-10 years | Liver, genetic diseases |
| **ADC** | Targeted chemotherapy, payload delivery | 10-15 years | Oncology |
| **Inhaled** | Local delivery, minimal systemic exposure | 6-8 years | Lung diseases |

---

## Disease-Modality Routing

### 1. Sarcopenia

**Preferred Modality Hierarchy**:
1. Small molecule (★★★) - Oral, chronic dosing feasible
2. Peptide (★★★) - Muscle anabolic targets (myostatin analogs)
3. Biologic (★★) - Myostatin/activin antibodies

**Target-Class to Modality Mapping**:

| Target Class | Example Targets | Recommended Modality | Rationale |
|--------------|---------------|---------------------|-----------|
| Kinase | MTOR, AMPK, AKT | Small molecule | Oral, chronic dosing |
| Transcription Factor | FOXO1/3, MYOD1 | Small molecule | Nuclear penetration |
| Enzyme | SIRT1, GSK3B | Small molecule | Catalytic site druggable |
| Receptor (GPCR) | GPR39, MC3R | Small molecule/Peptide | GPCR agonists |
| Secreted Factor | MSTN, FST | Biologic (Antibody) | Extracellular, large target |
| Mitochondrial | PGC1A | Small molecule | Mitochondrial penetration |

**Specific Recommendations**:
- **MTOR inhibitors**: Small molecule (rapamycin analogs) - approved for other indications
- **Myostatin axis**: Biologic (antibody) - Bimagrumab in trials
- **FOXO modulation**: Small molecule - SIRT1 activators (resveratrol)
- **AMPK activation**: Small molecule (metformin) - off-label potential

---

### 2. Heart Failure (HFrEF)

**Preferred Modality Hierarchy**:
1. Small molecule (★★★) - Oral chronic therapy, hemodynamic safety
2. Biologic (★★) - Extracellular targets (fibrosis)
3. Peptide (★★) - Cardiac hormones (urocortin)

**Target-Class to Modality Mapping**:

| Target Class | Example Targets | Recommended Modality | Rationale |
|--------------|---------------|---------------------|-----------|
| Ion Channel | hERG, cardiac sodium | Small molecule | Cardiac specificity |
| Enzyme | Neprilysin, PDE5 | Small molecule | Oral, chronic |
| Receptor (GPCR) | ARNI, SGLT2 | Small molecule | Oral, proven efficacy |
| Extracellular Matrix | Collagen, fibronectin | Biologic (antibody) | Extracellular, large |
| Nuclear Receptor | PPAR, RXR | Small molecule | Nuclear penetration |
| Calcium Handling | SERCA2A | Gene therapy | AAV delivery |

**Specific Recommendations**:
- **SGLT2 inhibitors**: Small molecule - approved, guideline-based
- **ARNI**: Small molecule (sacubitril/valsartan) - approved
- **MCR2 agonists**: Biologic - novel mechanism
- ** SERCA2A**: Gene therapy (AAV) - experimental

---

### 3. MASLD/MASH

**Preferred Modality Hierarchy**:
1. Small molecule (★★★) - Oral, liver exposure
2. Liver-targeted Oligo/siRNA (★★★) - Direct hepatocyte delivery
3. Peptide (★★) - Metabolic hormones (GLP-1 analogs)

**Target-Class to Modality Mapping**:

| Target Class | Example Targets | Recommended Modality | Rationale |
|--------------|---------------|---------------------|-----------|
| Nuclear Receptor | THR-β, FXR, PPARA | Small molecule | Nuclear, liver-selective |
| Enzyme | ACC, DGAT, SCD | Small molecule | Lipid metabolism |
| Receptor (GPCR) | GLP1R, GPR119 | Small molecule/Peptide | Metabolic |
| Inflammasome | NLRP3 | Small molecule | Cytosolic, liver exposure |
| Transporter | SGLT2 | Small molecule | Kidney-limited |
| Secreted Factor | FGF19, FGF21 | Biologic (analog) | Hepatokine analogs |

**Specific Recommendations**:
- **THR-β agonists**: Small molecule - Resmetirom approved
- **GLP-1 analogs**: Peptide - Semaglutide approved
- **NLRP3 inhibitors**: Small molecule - MCC940, promising
- **FXR agonists**: Small molecule - Obeticholic acid approved
- **FGF21 analogs**: Biologic - Phase II/III

---

### 4. Lung Fibrosis (IPF)

**Preferred Modality Hierarchy**:
1. Small molecule (★★★) - Oral, lung exposure
2. Inhaled formulation (★★★) - Local lung delivery
3. Biologic (★★) - Extracellular targets

**Target-Class to Modality Mapping**:

| Target Class | Example Targets | Recommended Modality | Rationale |
|--------------|---------------|---------------------|-----------|
| Kinase | TGF-β R1, DDR2 | Small molecule | Oral, systemic + lung |
| Cytokine | TGF-β, CTGF | Biologic (antibody) | Extracellular, high MW |
| Integrin | αvβ6 | Small molecule | Lung epithelial |
| ECM | Collagen, Elastin | Biologic | Large, extracellular |
| Enzyme | MMP7, LOXL2 | Small molecule | Proteolytic targets |
| Receptor | PDGFR | Small molecule | Approved (nintedanib) |

**Specific Recommendations**:
- **TGF-β inhibitors**: Small molecule (oral) or Biologic (antibody)
- **Inhaled pirfenidone/nintedanib**: Local delivery enhancement
- **αvβ6 integrin**: Small molecule - epithelial preservation
- **MMP7**: Biomarker + potential target

---

### 5. Cancer (NSCLC EGFR-mutant)

**Preferred Modality Hierarchy**:
1. Small molecule (★★★) - Targeted therapy, oral
2. ADC (★★★) - Targeted payload delivery
3. Biologic (★★) - Immune checkpoint
4. Oligo/siRNA (★★) - Resistance mechanisms

**Target-Class to Modality Mapping**:

| Target Class | Example Targets | Recommended Modality | Rationale |
|--------------|---------------|---------------------|-----------|
| Kinase | EGFR, ALK, ROS1, MET | Small molecule (TKI) | Driver oncogene |
| Surface Antigen | HER2, TROP2 | ADC | Targeted cytotoxicity |
| Immune Checkpoint | PD-1, PD-L1, CTLA4 | Biologic (antibody) | IO |
| Epigenetic | EZH2, HDAC | Small molecule | Nuclear |
| DNA Repair | PARP, BRCA | Small molecule | Synthetic lethality |
| Transcription Factor | NRF2, MYC | Small molecule (PROTAC) | Degradation |

**Specific Recommendations**:
- **EGFR TKI**: Small molecule - 1st/2nd/3rd gen, resistance patterns
- **MET TKI**: Small molecule - capmatinib, tepotinib
- **TROP2 ADC**: ADC - datopotamab deruxtecan
- **EGFR/cMET bispecific**: Biologic - amivantamab
- **Resistance mechanisms**: Oligo/siRNA - EGFR exon 20, MET amplification

---

## Cross-Disease Modality Strategy

### Emerging Platforms

| Platform | Disease Applications | Status |
|----------|-------------------|--------|
| **GLP-1 analogs** | Sarcopenia, MASLD, CVD | Approved (semaglutide) |
| **RNA targeting** | MASLD (HSD17B13), Cancer | Phase I/II |
| **PROTACs** | Cancer, fibrosis | Preclinical/Phase I |
| **Bispecific antibodies** | Cancer, immune | Approved |
| **Inhaled small molecules** | Lung fibrosis | Approved (nintedanib) |
| **Gene therapy** | Heart failure (SERCA2A) | Phase II/III |

---

## Practical Scoring for Modality Selection

When routing a target to modality, consider:

```
Modality Score = 
  tractability (0.25) ×
  delivery_feasibility (0.25) ×
  tissue_penetration (0.20) ×
  development_timeline (0.15) ×
  competitive_advantage (0.15)
```

| Modality | Tractability | Delivery | Penetration | Timeline | Competitive |
|----------|-------------|----------|-------------|----------|--------------|
| Small Molecule | High | High | High | Moderate | Low |
| Peptide | High | Moderate | Moderate | Long | Moderate |
| Biologic | High | Low (IV) | Moderate | Long | High |
| Oligo/siRNA | High | Moderate (liver) | Moderate | Long | High |
| ADC | Moderate | Targeted | Moderate | Very Long | High |
| Inhaled | High | Local | Local only | Moderate | Moderate |

---

## Implementation

### For Engine 2 (Target → Modality)

```
Input: Target properties
├── localization: nuclear | cytosolic | membrane | extracellular
├── target_class: kinase | receptor | enzyme | TF | etc.
├── tissue_required: liver | lung | muscle | heart | tumor
└── mutation_status: hotspot | truncation | amplification

Output: Modality recommendations
├── modality_ranking: [small_molecule, biologic, oligo, ...]
├── assay_strategy: [binding, functional, cellular]
└── liability_flags: [CYP, hERG, immunogenicity]
```

---

## Next Steps

1. Implement Target → Modality scoring in Engine 2
2. Create disease_pack_{disease}/modality_routes.json
3. Validate with known target-modality pairs (e.g., EGFR→TKI, MSTN→antibody)

---

*Document Version: 1.0*
*Generated: 2026-04-15*
*Status: Draft for Review*
