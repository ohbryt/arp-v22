# ARP v22 - Disease Target Scoring Matrix

## Version
**Document**: Complete Target Scoring Matrix for 5 Priority Diseases  
**Updated**: 2026-04-15  
**Status**: Ready for Implementation

---

## 1. Common Scoring Dimensions (8 Axes)

Each target is scored 0-1 on these dimensions:

| Dimension | Description | Data Sources |
|----------|------------|--------------|
| **A. Genetic/Causal Evidence** | Proximity to disease cause or upstream driver | GWAS Catalog, OMIM, UK Biobank, Mendelian randomization |
| **B. Disease-Context Relevance** | Importance in core pathology (fibrosis, inflammation, metabolism, etc.) | snRNA-seq, pathology databases, literature |
| **C. Perturbation Rescue Evidence** | Phenotype improvement when target is modulated | CRISPR screens, siRNA, preclinical models, rescue experiments |
| **D. Tissue/Cell Specificity** | Meaningful activity in target tissue, low off-target burden | GTEx, HPA, single-cell datasets |
| **E. Druggability/Tractability** | Structurally/biologically accessible to intervention | ChEMBL, Pharos, structural databases |
| **F. Safety/Therapeutic Window** | Acceptable toxicity profile, essential gene outside target | ToxDB, FDA labels, CDER, on-target liability |
| **G. Translation/Biomarkerability** | Patient stratification, PK/PD, biomarker feasibility | ClinicalTrials.gov, biomarker databases |
| **H. Competitive Novelty** | Not overcrowded, not completely unworkable | Patent landscape, pipeline analysis |

---

## 2. Disease-Specific Weight Configurations

### 2.1 Sarcopenia

**Core Question**: "Does this target contribute to maintaining/improving muscle FUNCTION, not just mass? Is it safe for chronic dosing? Is it muscle-specific enough?"

**Recommended Weights**:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **C. Perturbation Rescue** | **0.25** | Functional rescue evidence is paramount |
| **D. Tissue Specificity** | **0.20** | Skeletal muscle selectivity critical |
| **F. Safety** | **0.20** | Chronic administration, geriatric population |
| **B. Disease Context** | **0.15** | Anabolism vs catabolism balance |
| **E. Druggability** | **0.10** | Small molecule/peptide tractability |
| **A. Genetic Evidence** | **0.05** | Heritability contributes but less critical |
| **G. Translation** | **0.05** | Biomarker/functional endpoint linkage |

**Penalty Items**:
- Systemic anabolic liability (-0.15)
- Tumor growth concern (-0.20)
- Cardiac/metabolic adverse effects (-0.10)
- Neuromuscular mismatch (-0.10)

---

### 2.2 Heart Failure

**Core Question**: "Does this target reduce subtype-specific pathology? Where in remodeling/fibrosis/contractility does it act? What are cardiac/off-target risks?"

**Recommended Weights**:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **F. Safety** | **0.25** | QT/hERG, hemodynamic liability paramount |
| **B. Disease Context** | **0.20** | HFrEF vs HFpEF vs RV-specific context |
| **C. Perturbation Rescue** | **0.20** | Reverse remodeling evidence |
| **G. Translation** | **0.15** | BNP, troponin, imaging, remodeling biomarkers |
| **D. Tissue Specificity** | **0.10** | Cardiac vs systemic exposure |
| **E. Druggability** | **0.05** | Cardiac ion channels tractable |
| **A. Genetic Evidence** | **0.05** | HF heritability moderate |

**Penalty Items**:
- QT/hERG risk (-0.20)
- Contractility worsening (-0.15)
- Renal-hemodynamic instability (-0.15)
- Pro-arrhythmia (-0.20)
- Excessive fibrosis blockade causing repair issues (-0.10)

---

### 2.3 MASLD/MASH

**Core Question**: "Does this target reduce just steatosis, or also inflammation/fibrosis progression? Is it liver-accessible? What are metabolic safety risks?"

**Recommended Weights**:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **B. Disease Context** | **0.25** | Hepatocyte + stellate + Kupffer context |
| **D. Tissue Specificity** | **0.20** | Liver/hepatocyte selectivity critical |
| **F. Safety** | **0.20** | Chronic metabolic disease, organ liability |
| **C. Perturbation Rescue** | **0.15** | NASH preclinical rescue models |
| **E. Druggability** | **0.10** | Nuclear receptors highly tractable |
| **G. Translation** | **0.05** | ALT, AST, HbA1c, fibrosis scores |
| **A. Genetic Evidence** | **0.05** | GWAS, eQTL colocalization |

**Penalty Items**:
- Worsening dyslipidemia (-0.15)
- Hypertriglyceridemia (-0.10)
- Weight gain (-0.10)
- Hepatotoxicity (-0.20)
- Fibrosis-independent steatosis-only effect (-0.10)

---

### 2.4 Lung Fibrosis (IPF)

**Core Question**: "Does this target reduce fibroblast activation WITHOUT impairing epithelial repair? Is lung delivery possible? Is it in the causal fibrosis layer?"

**Recommended Weights**:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **B. Disease Context** | **0.25** | Fibroblast vs epithelial dual-context |
| **C. Perturbation Rescue** | **0.20** | Fibrosis progression models critical |
| **D. Tissue Specificity** | **0.15** | Lung selectivity, inhaled option |
| **F. Safety** | **0.15** | Wound-healing liability penalty |
| **E. Druggability** | **0.10** | TGF-β family tractable |
| **G. Translation** | **0.10** | FVC, DLCO, HRCT biomarkers |
| **A. Genetic Evidence** | **0.05** | IPF genetics less strong |

**Penalty Items**:
- Wound-healing inhibition (-0.20)
- Epithelial regeneration impairment (-0.20)
- Systemic immunosuppression (-0.15)
- Vascular/pulmonary tox (-0.10)

---

### 2.5 Cancer (Subtype-Specific)

**Core Question**: "Is there strong dependency in a specific cancer subtype? Can we define a biomarker-selected population? Is there therapeutic window? Does it matter in resistance settings?"

**Recommended Weights**:

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| **A. Genetic/Causal Evidence** | **0.20** | Driver oncogene dependency paramount |
| **B. Disease Context** | **0.20** | Subtype-specific (EGFRm NSCLC, not "lung cancer") |
| **C. Perturbation/Dependency** | **0.20** | CRISPR/shRNA dependency in subtype models |
| **F. Safety/Window** | **0.15** | Therapeutic window vs normal tissue |
| **G. Translation/Biomarker** | **0.15** | Patient stratification, companion diagnostic |
| **E. Druggability** | **0.05** | Kinases highly tractable |
| **H. Competitive Novelty** | **0.05** | Uncrowded, differentiation path |

**Penalty Items**:
- Pan-essential gene (-0.25)
- Poor normal-tissue window (-0.20)
- Resistance bypass likely (-0.15)
- Crowded target with no differentiation (-0.10)

---

## 3. Modality Routing Tables

### 3.1 Sarcopenia Modality Routing

| Target Type | Preferred Modality | Rationale | Caution |
|-------------|------------------|-----------|---------|
| Extracellular ligand/receptor | **Biologic, Peptide** | High specificity | Chronic injection burden |
| Kinase/Enzyme | **Small molecule** | Oral possible, scalable | Off-target toxicity |
| Transcriptional regulator | **Oligo, Degrader, Indirect SM** | Direct ligandability low | Delivery challenge |
| Myostatin/Activin axis | **Antibody, Ligand trap** | Precedent exists | Systemic endocrine effects |

**Priority Order**: 1. Biologic/Peptide > 2. Small molecule > 3. RNA-based

---

### 3.2 Heart Failure Modality Routing

| Target Type | Preferred Modality | Rationale | Caution |
|-------------|------------------|-----------|---------|
| Extracellular fibrosis mediator | **Antibody/Biologic** | Selectivity good | Tissue penetration |
| Intracellular signaling enzyme | **Small molecule** | Oral, chronic use | Cardiac safety |
| Ion/calcium handling | **Tuned small molecule** | Direct functional effect | Arrhythmia risk |
| Liver/kidney crosstalk factor | **Biologic/Oligo** | Systemic axis modulation | Organ cross-talk complexity |

**Priority Order**: 1. Small molecule > 2. Biologic > 3. RNA therapeutics

---

### 3.3 MASLD Modality Routing

| Target Type | Preferred Modality | Rationale | Caution |
|-------------|------------------|-----------|---------|
| Hepatocyte metabolic enzyme | **Small molecule** | Liver exposure favorable | Metabolic toxicity |
| Hepatocyte-expressed gene | **GalNAc-siRNA/ASO** | Strong liver targeting | Chronic dosing |
| Secreted metabolic factor | **Peptide/Biologic** | Endocrine modulation | Systemic effects |
| Fibrosis axis target | **Small molecule/Biologic** | Stage-specific strategy | Anti-fibrotic vs repair tradeoff |

**Priority Order**: 1. Small molecule > 2. Liver-targeted siRNA/ASO > 3. Peptide analog > 4. Biologic

---

### 3.4 Lung Fibrosis Modality Routing

| Target Type | Preferred Modality | Rationale | Caution |
|-------------|------------------|-----------|---------|
| Fibroblast signaling enzyme | **Small molecule** | Oral or inhaled possible | Systemic toxicity |
| Extracellular profibrotic mediator | **Antibody/Biologic** | Target specificity | Lung penetration/cost |
| Epithelial repair target | **Small molecule/Inhaled biologic** | Local delivery feasible | Repair overshoot risk |
| Integrin/ECM interface | **Antibody/Small molecule** | Fibrosis pathway relevance | Wound healing liability |

**Priority Order**: 1. Small molecule > 2. Inhaled modality > 3. Biologic (extracellular)

---

### 3.5 Cancer Modality Routing

| Target Type | Preferred Modality | Rationale | Caution |
|-------------|------------------|-----------|---------|
| Kinase/Enzyme driver | **Small molecule** | Strong precedent | Resistance mutations |
| Transcription factor/Scaffold | **Degrader/Glue/Indirect SM** | Hard target response | Chemistry difficulty |
| Cell-surface antigen | **Antibody/ADC** | High specificity | Expression heterogeneity |
| Synthetic lethality target | **Small molecule/Degrader** | Subtype selectivity | Normal tissue window |
| Immune target | **Antibody/Biologic/Cell therapy** | IO relevance | Immune toxicity |

**Priority Order**: 1. Small molecule > 2. Degrader > 3. Antibody/ADC > 4. IO (separate track)

---

## 4. Target Score Output Schema

```yaml
{
  "target": "FOXO1",
  "disease": "sarcopenia",
  "scores": {
    "genetic_causality": 0.35,
    "disease_context": 0.82,
    "perturbation_rescue": 0.78,
    "tissue_specificity": 0.74,
    "druggability": 0.56,
    "safety": 0.68,
    "translation": 0.61,
    "competitive_novelty": 0.44
  },
  "penalties": {
    "systemic_liability": 0.22,
    "oncogenic_risk": 0.10
  },
  "priority_score": 0.69,
  "recommended_modalities": ["small_molecule", "oligo"],
  "confidence": 0.72,
  "evidence_sources": ["GWAS_Catalog", "CRISPR_screens", "snRNA_seq"],
  "biomarkers": ["MuRF1", "MAFbx", "muscle_mass_DXA"],
  "assay_recommendations": ["myotube_atrophy_rescue", "grip_strength"]
}
```

---

## 5. Decision Rules for Modality Routing

```python
def route_modality(target, disease_context):
    """Automatic modality decision logic"""
    
    if target.is_extracellular and target.tissue_accessible:
        return "biologic"  # Highest specificity
    
    elif target.is_enzyme and target.has_known_pocket:
        return "small_molecule"  # Tractable pocket
    
    elif target.is_intracellular and target.degradation_logic_exists:
        return "degrader"  # Hard target approach
    
    elif disease_context == "MASLD" and target.liver_specific:
        return "GalNAc-siRNA"  # Liver targeting advantage
    
    elif disease_context == "Lung_Fibrosis" and target.inhalation_feasible:
        return "inhaled_modality"  # Local delivery
    
    else:
        return "indirect_small_molecule"  # Fallback strategy
```

---

## 6. Assay Templates by Disease

### Sarcopenia Assays
- Myotube atrophy/rescue assay
- Myoblast differentiation
- Mitochondrial function ( Seahorse)
- Protein synthesis/degradation balance ([^3H]leucine incorporation)
- In vivo: grip strength, muscle mass (DXA), endurance

### Heart Failure Assays
- Cardiomyocyte hypertrophy/remodeling assay
- Contractility/calcium handling (iPSC-CMs)
- Fibroblast activation (α-SMA, collagen)
- Fibrosis markers (hydroxyproline)
- In vivo: echocardiography, hemodynamics

### MASLD Assays
- Hepatocyte lipid accumulation (Nile red, BODIPY)
- Stellate cell activation (α-SMA)
- Inflammatory cytokine panel
- Liver organoid/co-culture
- Histology-linked fibrosis endpoints (NAS score)

### Lung Fibrosis Assays
- Fibroblast activation (α-SMA, collagen contraction)
- Collagen deposition
- Epithelial injury-repair assay
- Precision-cut lung slice (PCLS)
- In vivo: lung compliance, hydroxyproline

### Cancer Assays
- Cell viability/dependency (CRISPR screens)
- Apoptosis/cell-cycle arrest
- Resistance rescue models
- Biomarker-stratified panels
- Xenograft/PDX/organoid

---

## 7. Implementation Priority (Tiering)

### Tier 1 (MVP)
| Priority | Disease | Rationale |
|-----------|---------|-----------|
| **1** | MASLD | Resmetirom approved, pathway clear, metabolic tissue |
| **2** | Sarcopenia | High unmet need, clear functional endpoints |
| **3** | Lung Fibrosis | IPF biology well-characterized |

### Tier 2 (Expansion)
| Priority | Disease | Rationale |
|-----------|---------|-----------|
| **4** | Heart Failure | Choose HFrEF or HFpEF first |
| **5** | Cancer | NSCLC EGFR-mutant as index indication |

---

## 8. Disease Pack Components

Each disease pack should contain:

```
disease_pack_{disease}/
├── ontology.py           # Disease definitions, subtypes, stages
├── targets.py           # Target priors with weights
├── tissue_weights.py     # Tissue/cell-specific scoring
├── biomarkers.py        # Clinical biomarker mappings
├── contraindications.py # Safety flags, penalty terms
├── assays.py           # Assay templates, readouts
├── data_sources.py     # Required datasets, priority tiers
└── modality_routes.py  # Disease-specific modality preferences
```

---

## 9. Next Steps

1. **Create target dossier template**
2. **Create candidate dossier template**
3. **Implement MASLD disease pack (Tier 1)**
4. **Implement Engine 1: Disease → Target scoring**
5. **Implement Engine 2: Target → Modality routing**

---

*Document Version: 2.0 (Complete)*
*Generated: 2026-04-15*
*Status**: Ready for Implementation*
