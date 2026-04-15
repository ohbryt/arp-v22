# Target Dossier Template

## Purpose
Standardized format for documenting target prioritization decisions in ARP v22 drug discovery pipeline.

---

## Template Structure

```yaml
target_dossier:
  metadata:
    target_id: string          # e.g., "THRB_001"
    gene_name: string           # e.g., "THRB"
    protein_name: string         # e.g., "Thyroid hormone receptor beta"
    disease: string            # e.g., "MASLD"
    subtype: string             # e.g., "MASH with fibrosis"
    dossier_version: string     # e.g., "1.0"
    created_date: date
    last_updated: date
    confidence_level: float     # 0-1
    status: enum               # "prioritized", "rejected", "deprioritized"
  
  genetic_causality:
    score: float               # 0-1
    evidence:
      - gwas_associations: list
        - trait: string
        - variant: string
        - p_value: float
        - beta: float
      - rare_variants: list
        - mutation: string
        - inheritance: string
        - disease_relationship: string
      - eqtl_colocalization: list
        - tissue: string
        - gene: string
        - posterior_prob: float
      - mendelian_evidence: string
    citations:
      - pubmed_id: string
      - relevance: string
    confidence_notes: string
  
  disease_context:
    score: float               # 0-1
    relevance_axis: 
      primary: string          # e.g., "lipid_metabolism"
      secondary: list           # e.g., ["fibrosis", "inflammation"]
    pathway_membership:
      - kegg_pathway: string
      - reactome_pathway: string
    tissue_expression:
      - tissue: string
        normal_expression: float
        disease_expression: float
        differential: float
    cell_type_specificity:
      - cell_type: string
        expression: float
        specificity_score: float
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  perturbation_rescue:
    score: float               # 0-1
    evidence:
      crSpr_screen:
        - cell_line: string
        - effect_size: float
        - direction: enum       # "loss" or "gain"
        - context: string
      animal_models:
        - model: string
        - phenotype: string
        - rescue_observed: boolean
        - study_id: string
      small_molecule:
        - compound: string
        - effect: string
        - ic50: float
        - study_id: string
      clinical_trials:
        - nct_id: string
        - phase: string
        - outcome: string
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  tissue_specificity:
    score: float               # 0-1
    expression_data:
      hpa_normal_tissue:
        - tissue: string
          expression_level: enum  # "Not detected", "Low", "Medium", "High"
          specificity: float
      single_cell:
        - dataset: string
        - cell_type: string
          mean_expression: float
          pct_cells: float
    off_target_tissues:
      - tissue: string
        expression_concern: string
        liability_level: enum    # "low", "moderate", "high"
    delivery_feasibility:
      - route: string           # e.g., "oral", "inhaled"
        predicted_exposure: float
        tissue_penetration: float
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  druggability:
    score: float               # 0-1
    target_class: enum         # "kinase", "gpcR", "nuclear_receptor", etc.
    structural_data:
      - pdb_id: string
        resolution: float
        binding_site_defined: boolean
      - alphafold_confidence: float
    ligand_precedent:
      - compound: string
        affinity: float
        target: string
        clinical_use: string
    tractability_assessment:
      - assessment_level: enum  # " validated", "probable", "speculative"
        rationale: string
    development_challenges:
      - challenge: string
        mitigation: string
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  safety:
    score: float               # 0-1
    therapeutic_window:
      estimated_window: string
      based_on: string
    essential_gene_status:
      - tissue: string
        essential: boolean
        conditional_essential: boolean
        rationale: string
    known_adverse_effects:
      - effect: string
        severity: enum          # "mild", "moderate", "severe"
        frequency: string
        mechanism: string
    class_toxicity:
      - tox_class: string
        liability: string
        mitigation: string
    on_target_liability:
      - tissue: string
        liability: string
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  translation:
    score: float               # 0-1
    biomarker_status:
      - biomarker: string
        type: enum              # "diagnostic", "prognostic", "predictive"
        specimen: string
        status: string
      predictive_biomarker:
        - biomarker: string
          cutoff: float
          assay: string
    clinical_assays:
      - assay: string
        specimen: string
        standardizability: enum  # "established", "feasible", "developing"
    pk_pd_considerations:
      - species: string
        prediction_reliability: float
        human_relevance: string
    patient_stratification:
      - subgroup: string
        prevalence: float
        rationale: string
    clinical_development:
      - current_phase: string
        development_questions: list
    citations:
      - pubmed_id: string
    confidence_notes: string
  
  competitive_novelty:
    score: float               # 0-1
    patent_landscape:
      - patent_family: string
        status: string
        expiration: date
      freedom_to_operate:
        assessment: string
    competitive_pipeline:
      - company: string
        compound: string
        mechanism: string
        stage: string
    differentiation_opportunity:
      - opportunity: string
        feasibility: float
    fast_follower_space:
      - space_type: enum         # "crowded", "moderate", "open"
        strategy: string
    citations:
      - source: string
    confidence_notes: string
  
  penalties:
    - penalty_name: string
      severity: float           # 0-1 (higher = more severe)
      rationale: string
      evidence: string
  
  priority_calculation:
    weighted_score: float
    calculation_breakdown:
      dimension: string
        weight: float
        score: float
        contribution: float
    final_priority_score: float
    rank: integer
    confidence: float
  
  recommended_modalities:
    - modality: string
      rationale: string
      fit_score: float          # 0-1
      development_timeline: string
      estimated_cost: string
      key_challenges: list
      key_opportunities: list
      references: list
  
  assay_strategy:
    primary_assays:
      - assay_name: string
        assay_type: string
        readout: string
        gold_standard: boolean
        development_status: string
    secondary_assays:
      - assay_name: string
        purpose: string
    clinical_biomarkers:
      - biomarker: string
        sample_type: string
        measurement_method: string
    go/no_go_criteria:
      - criterion: string
        threshold: float
        rationale: string
  
  development_roadmap:
    preclinical:
      - milestone: string
        timeline: string
        key_dependencies: list
    clinical:
      - phase: string
        primary_endpoint: string
        secondary_endpoints: list
        estimated_enrollment: integer
        timeline: string
    biomarker_strategy:
      - biomarker: string
        clinical_context: string
        assay_development: string
  
  risk_assessment:
    technical_risks:
      - risk: string
        likelihood: enum          # "low", "medium", "high"
        impact: enum
        mitigation: string
    regulatory_risks:
      - risk: string
        likelihood: enum
        impact: enum
        mitigation: string
    commercial_risks:
      - risk: string
        likelihood: enum
        impact: enum
        mitigation: string
  
  key_references:
    - pubmed_id: string
      title: string
      relevance: string
    clinical_trial:
      - nct_id: string
        phase: string
        status: string
    patent:
      - patent_number: string
      status: string
  
  dossier_author:
    name: string
    organization: string
    date: date
    review_status: enum        # "draft", "reviewed", "approved"
    review_notes: string
```

---

## Example: Target Dossier for THRβ in MASLD

```yaml
target_dossier:
  metadata:
    target_id: "THRB_001"
    gene_name: "THRB"
    protein_name: "Thyroid hormone receptor beta"
    disease: "MASLD"
    subtype: "MASH with fibrosis F2-F3"
    dossier_version: "1.0"
    created_date: "2026-04-15"
    last_updated: "2026-04-15"
    confidence_level: 0.92
    status: "prioritized"
  
  genetic_causality:
    score: 0.90
    evidence:
      gwas_associations:
        - trait: "HDL cholesterol"
          variant: "rs3935579"
          p_value: 1.2e-15
          beta: 0.08
        - trait: "LDL cholesterol"
          variant: "rs9399133"
          p_value: 3.4e-22
          beta: 0.12
      eqtl_colocalization:
        - tissue: "liver"
          gene: "THRB"
          posterior_prob: 0.89
    citations:
      - pubmed_id: "32541065"
      - pubmed_id: "30239722"
  
  disease_context:
    score: 0.85
    relevance_axis:
      primary: "lipid_metabolism"
      secondary: ["bile_acid", "glucose"]
    tissue_expression:
      - tissue: "liver"
        normal_expression: 4.2
        disease_expression: 3.8
        differential: -0.4
  
  perturbation_rescue:
    score: 0.95
    evidence:
      small_molecule:
        - compound: "Resmetirom"
          effect: "65% liver fat reduction"
          ic50: 0.21
          study_id: "MAESTRO-NASH"
      animal_models:
        - model: "MASH diet mice"
          phenotype: "NASH resolution"
          rescue_observed: true
  
  tissue_specificity:
    score: 0.85
    off_target_tissues:
      - tissue: "heart"
        expression_concern: "T3 cardiac effects"
        liability_level: "moderate"
  
  druggability:
    score: 0.90
    target_class: "nuclear_receptor"
    ligand_precedent:
      - compound: "Triac"
        affinity: "nanomolar"
        clinical_use: "approved for thyroid"
  
  safety:
    score: 0.80
    known_adverse_effects:
      - effect: "Thyroid axis suppression"
        severity: "moderate"
        frequency: "common"
        mechanism: "On-target TH activity"
  
  translation:
    score: 0.90
    biomarker_status:
      - biomarker: "LDL-C"
        type: "efficacy"
  
  priority_calculation:
    final_priority_score: 0.871
    rank: 1
  
  recommended_modalities:
    - modality: "small_molecule"
      rationale: "Nuclear receptor, oral bioavailability achieved"
      fit_score: 0.92
  
  key_references:
    - pubmed_id: "33106447"  # Resmetirom Phase III
```

---

## Usage Notes

1. **Minimum Required Fields**: Target ID, Gene Name, Disease, all 8 dimension scores, final priority score, recommended modalities

2. **Confidence Scoring**: Higher confidence (>0.8) requires strong evidence in at least 3 dimensions

3. **Modality Fit**: Multiple modalities can be recommended with fit scores

4. **Dossier Review**: All dossiers should be reviewed by domain expert before Engine 2 routing

5. **Version Control**: Update `last_updated` and `dossier_version` with each revision

---

*Template Version: 1.0*
*Created: 2026-04-15*
*Status: Ready for Implementation*
