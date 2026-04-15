# Candidate Dossier Template

## Purpose
Standardized format for documenting candidate prioritization decisions in ARP v22 drug discovery pipeline.

---

## Template Structure

```yaml
candidate_dossier:
  metadata:
    candidate_id: string          # e.g., "RESV_001"
    name: string                 # e.g., "Resmetirom"
    smiles: string               # e.g., "CC(=O)Nc1ccc(C2=C(C3CCC3)C(=O)C2=C(C)C(=O)C=C1)cc1"
    candidate_type: enum          # "small_molecule", "peptide", "biologic", "oligo", "adc"
    target: string               # e.g., "THRB"
    disease: string             # e.g., "MASLD"
    indication: string          # e.g., "MASH with fibrosis F2-F3"
    development_stage: enum      # "discovery", "lead_opt", "preclinical", "phase1", "phase2", "phase3", "approved"
    dossier_version: string
    created_date: date
    last_updated: date
    confidence_level: float     # 0-1
    status: enum               # "active", "terminated", "on_hold", "approved"
  
  chemical_properties:
    molecular_weight: float     # Da
    logp: float
    topological_polar_surface_area: float  # TPSA
    hydrogen_bond_donors: integer
    hydrogen_bond_acceptors: integer
    rotatable_bonds: integer
    rings: integer
    aromatic_rings: integer
    chiral_centers: integer
    fsp3: float               # Fraction sp3
    molecular_formula: string
    canonical_smiles: string
    inchi_key: string
  
  admet_properties:
    absorption:
      solubility:
        value: string
        prediction_confidence: float
        experimental_data: string
      permeability:
        caco2_papp: float
        prediction_confidence: float
      bioavailability:
        predicted_f: float       # Oral bioavailability %
        prediction_confidence: float
    distribution:
      plasma_protein_binding:
        human_ppbr: float        # %
        prediction_confidence: float
      volume_of_distribution:
        vd_ss_predicted: float  # L/kg
      brain_penetration:
        bbb_score: float        # 0-1
        prediction_confidence: float
    metabolism:
      cytochrome_p450:
        cyp1a2_inhibition: float  # IC50 uM
        cyp2c9_inhibition: float
        cyp2c19_inhibition: float
        cyp2d6_inhibition: float
        cyp3a4_inhibition: float
        cyp3a4_induction: float   # fold
      half_life:
        human_hl_predicted: float  # hours
        prediction_confidence: float
      metabolic_stability:
        intrinsic_clearance: float  # uL/min/mg
    excretion:
      renal_excretion: float    # % of dose
      hepatic_excretion: float
      total_clearance: float
    safety_pharmacology:
      herg_blockade:
        ic50: float            # uM
        liability: enum        # "low", "moderate", "high"
      ames_test: string        # "negative", "positive", "predicted_negative"
      micronucleus: string
      cytotoxicity:
        cell_line: string
        ic50: float            # uM
      off_target_toxicity:
        - target: string
          ic50: float
          liability: string
    drug_interactions:
      cyp_inhibition_treatment_risk: enum  # "low", "moderate", "high"
  
  target_engagement:
    primary_target:
      target_name: string
      gene_name: string
      binding_mode: enum        # "agonist", "antagonist", "inverse_agonist", "inhibitor", etc.
      affinity:
        kd: float             # nM
        ki: float             # nM
        ic50: float           # nM
        ec50: float           # nM (for agonists)
      assay_type: string
      species_relevance: string
    secondary_targets:
      - target_name: string
        gene_name: string
        activity: string
        affinity: float
        selectivity_over_primary: float
    pathway_activity:
      - pathway: string
        activity: string
        measurement: string
        result: string
  
  efficacy_data:
    in_vitro:
      - assay: string
        model_system: string
        endpoint: string
        result: string
        ic50_ec50: float
        hill_slope: float
        efficacy_max: float
        references: list
    in_vivo:
      preclinical_efficacy:
        - model: string
          species: string
          dosing: string
          duration: string
          endpoint: string
          result: string
          statistical_analysis: string
          references: list
      animal_pharmacokinetics:
        - species: string
          route: string
          dose: string
          auc: float
          cmax: float
          half_life: float
          bioavailability: float
    clinical_efficacy:
      - trial_id: string       # NCT number
        phase: string
        population: string
        sample_size: integer
        primary_endpoint: string
        result: string
        statistical_analysis: string
        references: list
  
  development_status:
    current_phase: string
    development_history:
      - date: date
        event: string
        details: string
    competitive_position:
      - competitor: string
        compound: string
        mechanism: string
        status: string
        market_share: string
    regulatory_status:
      breakthrough_therapy: boolean
      orphan_drug: boolean
      fast_track: boolean
      priority_review: boolean
      approval_date: date
      approved_indications: list
  
  safety_assessment:
    clinical_safety:
      - trial_id: string
        population: string
        sample_size: integer
        treatment_emergent_ae:
          - event: string
            frequency: float        # %
            severity: enum          # "mild", "moderate", "severe"
            relatedness: enum       # "unrelated", "possibly_related", "probably_related"
        serious_ae: list
        ae_discontinuation_rate: float
    observed_adverse_events:
      - event: string
        incidence: float           # %
        grade: integer            # CTCAE grade
        management: string
        outcome: string
    risk_mitigation:
      - risk: string
        probability: float
        impact: string
        mitigation_strategy: string
        monitoring_plan: string
  
  biomarker_strategy:
    predictive_biomarkers:
      - biomarker: string
        sample_type: string
        cutoff_value: string
        assay_method: string
        status: string          # "validated", "exploratory"
        clinical_utility: string
    pharmacodynamic_biomarkers:
      - biomarker: string
        sample_type: string
        expected_direction: string
        measurement_timepoint: string
    prognostic_biomarkers:
      - biomarker: string
        status: string
  
  combination_potential:
    rationale: string
    combinations_considered:
      - partner: string
        mechanism: string
        preclinical_data: string
        clinical_data: string
        potential_synergy: string
        risk_concerns: string
    ongoing_combo_trials:
      - trial_id: string
        combination: string
        status: string
  
  manufacturingCMC:
    synthesis:
      synthetic_route: string
      key_intermediates: list
      critical_quality_attributes: list
    formulation:
      dosage_form: string
      formulation_approach: string
      excipients: list
      stability_data: string
    scalability:
      current_batch_size: float
      projected_batch_size: float
      cost_of_goods: string
  
  intellectual_property:
    patent_family:
      - patent_number: string
        filing_date: date
        status: string
        expiration_date: date
        claims_scope: string
    freedom_to_operate:
      analysis_date: date
      fto_risks: list
      mitigation_strategies: list
    exclusivity_estimation:
      base_exclusivity: float      # years
      patent_extensions: float
      regulatory_exclusivity: float
      total_estimation: float
  
  development_roadmap:
    preclinical:
      - milestone: string
        target_date: date
        status: string
        dependencies: list
    clinical:
      - phase: string
        target_start: date
        target_completion: date
        enrollment: integer
        primary_endpoint: string
        estimated_cost: string
        go_no_go_criteria: list
    regulatory:
      - milestone: string
        target_date: date
        requirements: list
    commercial:
      - milestone: string
        target_date: date
  
  overall_assessment:
    strengths:
      - strength: string
        evidence: string
    weaknesses:
      - weakness: string
        mitigation: string
    opportunities:
      - opportunity: string
        feasibility: string
    threats:
      - threat: string
        contingency: string
    competitive_advantages:
      - advantage: string
        differentiation: string
    development_risks:
      - risk: string
        likelihood: enum
        impact: enum
    go_decision:
      recommendation: enum        # "proceed", "conditional_proceed", "reconsider", "terminate"
      rationale: string
      key_conditions: list
  
  key_references:
    - pubmed_id: string
      title: string
      relevance: string
    - trial_id: string
      phase: string
      status: string
  
  dossier_author:
    name: string
    organization: string
    date: date
    review_status: enum
    review_notes: string
```

---

## Example: Candidate Dossier for Resmetirom (MASLD)

```yaml
candidate_dossier:
  metadata:
    candidate_id: "MGL3196_001"
    name: "Resmetirom"
    smiles: "CC(=O)Nc1ccc(C2=C(C3CCC3)C(=O)C2=C(C)C(=O)C=C1)cc1"
    candidate_type: "small_molecule"
    target: "THRB"
    disease: "MASLD"
    indication: "MASH with fibrosis F2-F3"
    development_stage: "approved"
    dossier_version: "1.0"
    created_date: "2026-04-15"
    confidence_level: 0.95
    status: "approved"
  
  chemical_properties:
    molecular_weight: 585.7
    logp: 5.2
    topological_polar_surface_area: 89.3
    hydrogen_bond_donors: 1
    hydrogen_bond_acceptors: 4
  
  admet_properties:
    absorption:
      bioavailability:
        predicted_f: 45
    metabolism:
      cyp3a4_inhibition: 0.3  # uM - low inhibition
    safety_pharmacology:
      herg_blockade:
        ic50: 8.2
        liability: "moderate"
  
  target_engagement:
    primary_target:
      target_name: "Thyroid hormone receptor beta"
      gene_name: "THRB"
      binding_mode: "agonist"
      affinity:
        kd: 0.21
  
  efficacy_data:
    clinical_efficacy:
      - trial_id: "MAESTRO-NASH"
        phase: "Phase 3"
        result: "NASH resolution 26% vs 10% placebo"
  
  overall_assessment:
    go_decision:
      recommendation: "proceed"
      rationale: "FDA approved 2024, clear efficacy"
```

---

## Candidate Ranking Schema

```yaml
candidate_ranking:
  composite_score:
    target_engagement: 0.30    # 30%
    admet_developability: 0.20  # 20%
    efficacy_potency: 0.25       # 25%
    safety_tolerability: 0.25     # 25%
  
  sub_scores:
    admet_developability:
      - metric: "solubility"
        weight: 0.15
      - metric: "permeability"
        weight: 0.15
      - metric: "metabolic_stability"
        weight: 0.25
      - metric: "hERGliability"
        weight: 0.25
      - metric: "CYP_interactions"
        weight: 0.20
  
  final_ranking:
    - candidate_id: string
      composite_score: float
      rank: integer
      decision: enum            # "advance", "hold", "deprioritize"
      rationale: string
```

---

## Usage Notes

1. **Minimum Required Fields**: Candidate ID, Name, Type, Target, all 4 composite score dimensions, final ranking

2. **Confidence Scoring**: Higher confidence (>0.8) requires clinical data

3. **Decision Framework**: Composite score weighted by disease-specific priorities

4. **Dossier Review**: All dossiers should be reviewed before candidate selection

5. **Version Control**: Update `last_updated` and `dossier_version` with each revision

---

*Template Version: 1.0*
*Created: 2026-04-15*
*Status: Ready for Implementation*
