# Cardiac Fibrosis Screening Assays
## IL-11 and LOXL2 Drug Discovery Assays

**Date:** 2026-04-18  
**Targets:** IL-11, LOXL2  
**Purpose:** Experimental designs for anti-fibrotic drug screening

---

## 1. IL-11 Screening Assays

### Target: Interleukin-11 (IL-11) / IL11RA1

**Background:** IL-11 is downstream of TGF-β1 in cardiac fibroblast activation. Unlike pan-TGF-β inhibition, IL-11 targeting offers specificity with less toxicity.

---

### Assay 1.1: IL-11/TGF-β1-Induced Fibroblast Activation

**Purpose:** Primary screening assay for IL-11 pathway inhibitors

**Cell Model:** Primary Adult Human Cardiac Fibroblasts (HCF)

**Induction:** 
- Recombinant human IL-11 (10 ng/mL) OR
- TGF-β1 (2 ng/mL) as positive control

**Endpoints:**
| Endpoint | Method |readout |
|---------|--------|--------|
| α-SMA expression | Immunofluorescence / qPCR | ACTA2 |
| Collagen I | ELISA (COL1A1) | Secreted protein |
| Fibroblast proliferation | EdU incorporation | DNA synthesis |
| Myofibroblast differentiation | Gel contraction assay | Contractility |

**Protocol:**
```
Day 0: Seed HCF (5,000 cells/well, 96-well)
Day 1: Serum starve (0.1% FBS, 24h)
Day 2: Add test compounds (10-point titration) + IL-11 (10 ng/mL)
Day 4: Fix and stain OR harvest supernatant
Day 5: Read endpoints
```

**Positive Controls:**
- Anti-IL-11 antibody (Research)
- SB-431542 (TGFβR1 inhibitor, for TGF-β1 condition)

**Hit Criteria:**
- IC50 < 10 μM (small molecules)
- IC50 < 100 nM (peptides/proteins)
- Cytotoxicity > 80% at 10 μM = toxic

**Validation:**
- Confirm in TGF-β1-induced condition (IL-11 should not inhibit)
- Test in mouse cardiac fibroblasts (species cross-validation)

---

### Assay 1.2: IL-11/STAT3 Phosphorylation

**Purpose:** Mechanistic assay for pathway engagement

**Method:** AlphaLisa or Western Blot

**Protocol:**
```
Treatment: Test compounds + IL-11 (10 ng/mL)
Time points: 0, 15, 30, 60 min
Target: p-STAT3 (Tyr705)
Loading control: Total STAT3
```

**Readout:** p-STAT3/STAT3 ratio

**Expected:** IL-11 pathway inhibitors block STAT3 phosphorylation

---

### Assay 1.3: IL-11 Secretion Assay

**Purpose:** Measure endogenous IL-11 inhibition (for upstream targets)

**Stimulus:** TGF-β1 (2 ng/mL) or IL-1β (10 ng/mL)

**Detection:** IL-11 ELISA (human)

**Utility:** Identify compounds that reduce IL-11 production

---

### Assay 1.4: In Vivo Validation - Mouse TAC Model

**Model:** Transverse Aortic Constriction (TAC)

**Treatment Schedule:**
- Compounds: Daily IP injection or oral gavage
- Duration: 4 weeks post-TAC
- Doses: 3 dose levels (e.g., 3, 10, 30 mg/kg)

**Endpoints:**
| Endpoint | Method |
|---------|--------|
| Cardiac fibrosis | Masson's trichrome, Picrosirius red |
| Myofibroblast markers | α-SMA, POSTN IHC |
| Cardiac function | Echocardiography (EF%, FS%) |
| Collagen content | Hydroxyproline assay |
| Molecular markers | qPCR (Col1a1, Acta2, Postn) |

---

## 2. LOXL2 Screening Assays

### Target: Lysyl Oxidase-Like 2 (LOXL2)

**Background:** LOXL2 mediates collagen crosslinking, making fibrosis stiff and irreversible. SNT-5382 (2025) demonstrated strong anti-fibrotic efficacy.

---

### Assay 2.1: LOXL2 Enzymatic Activity

**Purpose:** Primary biochemical screening assay

**Method:** Amiloride-resistant fluorometric assay

**Substrate:** BODIPY-conjugated collagen-like peptide (or commercial LOXL2 substrate)

**Protocol:**
```
Reaction: LOXL2 (5 nM) + substrate (10 μM) + test compound
Buffer: PBS, pH 7.4, 37°C
Time: 60 min
Readout: Fluorescence (ex 485/em 528)

Reactions:
- Positive control: Known LOXL2 inhibitor
- Negative control: No enzyme
- Background: No inhibitor, no enzyme
```

**Hit Criteria:**
- IC50 < 1 μM (potent inhibitors)
- Selectivity over LOX (100-fold)

**Counter-screen:** LOX, LOXL1, LOXL3 selectivity

---

### Assay 2.2: Collagen Crosslinking in Fibroblasts

**Purpose:** Cellular assay for LOXL2 functional inhibition

**Model:** Human cardiac fibroblasts

**Detection:** PYR（pyridinolines）in ECM via LC-MS/MS

**Protocol:**
```
Day 0: Seed HCF (20,000 cells/cm²)
Day 1: Add ascorbic acid (100 μM) + test compounds
Day 4-7: Collect ECM fraction
Day 8: Hydrolyze ECM (6M HCl, 110°C, 18h)
Analysis: LC-MS/MS for pyridinoline crosslinks
```

**Endpoints:**
- Total collagen (hydroxyproline)
- Pyridinoline crosslinks (DPD, HP)
- Crosslink density (PYR/collagen ratio)

---

### Assay 2.3: Fibroblast Activation Markers

**Purpose:** Secondary cellular assay

**Endpoints:**
| Endpoint | Method |
|---------|--------|
| α-SMA | IF, qPCR |
| Collagen I | ELISA, qPCR |
| LOXL2 expression | qPCR, Western blot |
| Fibronectin | ELISA |

**Protocol:**
```
Treatment: TGF-β1 (2 ng/mL) + test compounds
Duration: 72h
Analysis: α-SMA, COL1A1, LOXL2
```

---

### Assay 2.4: ECM Stiffness Assay

**Purpose:** Measure functional impact of LOXL2 inhibition

**Method:** Atomic Force Microscopy (AFM) or hydrogel stiffness

**Model:** Fibroblasts on collagen-coated hydrogels

**Protocol:**
```
Day 0: Seed fibroblasts on soft (1 kPa) or stiff (30 kPa) gels
Day 1-4: Treatment with test compounds
Day 5: AFM measurement of substrate stiffness
        OR
        Measure traction forces (FRET-based)
```

**Readout:** Substrate stiffness, traction forces

**Expected:** LOXL2 inhibition prevents stiffness increase

---

### Assay 2.5: In Vivo Validation - Mouse Fibrosis Models

**Model 1: TAC (Pressure Overload)**
```
Procedure: Transverse aortic constriction
Treatment: Start day 0 or day 7 post-TAC
Duration: 4-8 weeks
Endpoints: Same as Assay 1.4 + LOXL2 activity
```

**Model 2: Angiotensin II Infusion**
```
Procedure: Mini-osmotic pump (1.1 mg/kg/day AngII)
Treatment: Concurrent with test compounds
Duration: 4 weeks
Endpoints: Same as above
```

---

## 3. Multi-Parameter Profiling

### Assay 3.1: Fibroblast Activation Panel

**Platform:** 96-well or 384-well multiplex

**Markers:**
- α-SMA (ACTA2)
- Collagen I (COL1A1)
- Fibronectin (FN1)
- Periostin (POSTN)
- LOXL2
- CTGF

**Utility:** Broad profiling of anti-fibrotic compounds

---

### Assay 3.2: Safety Pharmacology

**Cardiac Safety:**
- hERG channel assay (IKr)
- Nav1.5 (ICa)
- Cytotoxicity in cardiomyocytes

**Off-target screens:**
- CYP450 inhibition
- Binding assays for major receptors

---

## 4. High-Content Screening (HCS) Protocol

### Assay 4.1: Phenotypic Multi-Parameter

**Platform:** Opera Phenix or similar HCS

**Cells:** Human cardiac fibroblasts

**Staining:**
- Phalloidin (F-actin)
- DAPI (nuclei)
- α-SMA (Alexa 488)
- Collagen I (Cy3)

**Analysis:**
- Cell count
- Morphology (shape factor)
- α-SMA intensity per cell
- Collagen area

**Protocol:**
```
Seed: 3,000 cells/well (384-well)
Starve: 24h (0.1% FBS)
Treat: Compounds + TGF-β1 (2 ng/mL)
Fix: 72h
Stain: Multiplex immunofluorescence
Read: Opera Phenix (20x)
Analyze: Columbus or similar
```

---

## 5. Chemical Library Screening

### Primary Screen: 10,000+ compounds

**Library Options:**
- FDA-approved drug library (repurposing)
- Natural product library
- Focused kinase inhibitor library
- Fragment library

**Assay:** IL-11/TGF-β1-induced α-SMA (384-well)

**Hit Rate:** Typically 0.5-2%

### Secondary Screening: 50-200 hits

**Confirm in:**
- Dose-response (10-point)
- Counter-screen (toxicity)
- Alternative endpoint (Collagen I ELISA)
- Selectivity panel

### Hit-to-Lead: 10-20 compounds

**Follow-up:**
- LOXL2 assay (if IL-11)
- Cross-target selectivity
- ADMET prediction
- Structural similarity search

---

## 6. Reference Compounds

### IL-11 Pathway
| Compound | Type | Activity | Source |
|----------|------|----------|--------|
| Anti-IL-11 mAb | Antibody | Neutralizing | Research |
| IL11RA siRNA | siRNA | Knockdown | Research |
| SB-431542 | Small molecule | TGFβR1 inhibitor | Tocris |
| A83-01 | Small molecule | TGFβR1 inhibitor | Tocris |

### LOXL2
| Compound | Type | Activity | Source |
|----------|------|----------|--------|
| SNT-5382 | Small molecule | LOXL2 inhibitor | From paper |
| BAPN | Small molecule | LOX inhibitor | Sigma |
| Copper chelation | Mechanism | LOX inhibition | Various |

### General Anti-Fibrotics
| Compound | Type | Activity | Source |
|----------|------|----------|--------|
| Pirfenidone | Small molecule | Multi-pathway | Already approved |
| Nintedanib | Small molecule | Multi-kinase | Already approved |
| Verteporfin | Small molecule | YAP-TEAD | FDA-approved |

---

## 7. Success Metrics

### Primary Hits
- **Hit rate:** 0.5-2% of library
- **Confirmation rate:** >80% confirmed in dose-response
- **Potency:** IC50 < 10 μM (small molecules)

### Lead Optimization
- **Potency:** IC50 < 1 μM
- **Selectivity:** >50-fold over off-targets
- **ADMET:** Solubility > 90%, Microsomal stability > 30 min

### Preclinical Candidate
- **In vitro:** Efficacy in 3+ assays
- **In vivo:** Efficacy in mouse model at <10 mg/kg
- **Safety:** No hERG block, acceptable tox profile

---

## 8. Timeline

| Phase | Duration | Activities |
|-------|----------|------------|
| Assay Development | 4-6 weeks | HCS assay optimization |
| Primary Screen | 2-3 weeks | 10K+ compounds |
| Hit Confirmation | 2-3 weeks | Dose-response |
| Secondary Screening | 4-6 weeks | Selectivity, ADMET |
| Lead Optimization | 12-16 weeks | SAR, ADMET improvement |
| In Vivo Efficacy | 8-12 weeks | Mouse studies |

**Total:** 8-12 months to candidate

---

**Document Version:** 1.0  
**Last Updated:** 2026-04-18  
**Prepared by:** Enhanced ARP v22 Pipeline