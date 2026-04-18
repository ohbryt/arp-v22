"""
Cardiac Fibrosis Target List

Novel and established therapeutic targets for cardiac fibrosis drug discovery.
Prioritized based on novelty, druggability, and clinical potential.
"""

CARDIAC_FIBROSIS_TARGETS = {
    'IL11': {
        'gene_name': 'Interleukin 11',
        'uniprot_id': 'P20809',
        'priority': 1,
        'target_class': 'Cytokine',
        'pathway': 'IL-11/IL11RA',
        'description': 'IL-11 is a crucial determinant of cardiovascular fibrosis, acting downstream of TGF-β1 in cardiac fibroblast activation. Unlike pan-TGF-β inhibition, IL-11 targeting offers specificity and avoids systemic toxicity.',
        'rationale': (
            'TGF-β inhibition has failed in clinical trials due to dose-limiting toxicities. '
            'IL-11 is specifically required for TGF-β1-induced cardiac fibroblast activation: '
            'anti-IL-6 antibodies have NO effect, while anti-IL-11 antibodies and IL11RA siRNA '
            'BLOCK fibrosis. This makes IL-11 a specific, safer target.'
        ),
        'genetic_evidence': 'IL11RA knockdown blocks TGF-β1 effects',
        'drug_modality': ['Monoclonal antibody', 'siRNA', 'Small molecule'],
        'development_stage': 'Preclinical',
        'novelty_score': 9.0,
        'druggability_score': 8.5,
        'safety_score': 8.0,
        'priority_score': 8.5,
        'known_inhibitors': [
            {'name': 'Anti-IL-11 antibodies', 'type': 'mAb', 'company': 'Various', 'status': 'Research'},
            {'name': 'IL11RA siRNA', 'type': 'siRNA', 'status': 'Research'}
        ],
        'screening_assay': 'IL-11/TGF-β1 induced fibroblast activation (α-SMA, COL1A1)',
        'validation_model': 'Mouse TAC model, human cardiac fibroblast cultures'
    },
    
    'LOXL2': {
        'gene_name': 'Lysyl Oxidase Like 2',
        'uniprot_id': 'Q9Y4K0',
        'priority': 2,
        'target_class': 'Enzyme',
        'pathway': 'LOX/LOXL',
        'description': 'LOXL2 is crucial for collagen and elastin fiber crosslinking, leading to ECM stiffening and cardiac dysfunction. SNT-5382 is a selective LOXL2 inhibitor showing strong anti-fibrotic effects.',
        'rationale': (
            'Collagen crosslinking by LOXL2 makes fibrosis irreversible and stiff. '
            'SNT-5382 (2025) reduces cardiac fibrosis with strong target engagement. '
            'LOXL2 inhibition prevents ECM stiffening and may allow reversal.'
        ),
        'genetic_evidence': 'LOXL2 knockdown reduces fibrosis in mouse models',
        'drug_modality': ['Small molecule inhibitor'],
        'development_stage': 'Preclinical (SNT-5382)',
        'novelty_score': 8.0,
        'druggability_score': 9.5,
        'safety_score': 8.5,
        'priority_score': 8.7,
        'known_inhibitors': [
            {'name': 'SNT-5382', 'type': 'Small molecule', 'evidence': 'Scientific Reports 2025', 'results': 'Reduces cardiac fibrosis, strong target engagement'}
        ],
        'screening_assay': 'LOXL2 enzymatic activity (amiloride-resistant substrate)',
        'validation_model': 'Mouse TAC model'
    },
    
    'YAP1': {
        'gene_name': 'Yes-Associated Protein 1',
        'uniprot_id': 'P46937',
        'priority': 3,
        'target_class': 'Transcription Co-activator',
        'pathway': 'Hippo/YAP/TAZ',
        'description': 'YAP/TAZ are mechanosensors that regulate fibroblast activation in response to ECM stiffness. Verteporfin (FDA-approved) inhibits YAP-TEAD interaction and reduces myocardial fibrosis.',
        'rationale': (
            'YAP/TAZ mediate mechanically-induced ECM remodeling. '
            'Genetic YAP ablation in fibroblasts attenuates cardiac fibrosis and improves function. '
            'Verteporfin (FDA-approved for AMD) reduces myocardial fibrosis - drug repositioning opportunity.'
        ),
        'genetic_evidence': 'Fibroblast-specific YAP deletion improves cardiac function',
        'drug_modality': ['Small molecule inhibitor', 'siRNA'],
        'development_stage': 'Research (Verteporfin repositioning)',
        'novelty_score': 7.5,
        'druggability_score': 8.0,
        'safety_score': 7.5,
        'priority_score': 7.7,
        'known_inhibitors': [
            {'name': 'Verteporfin', 'type': 'FDA-approved', 'indication': 'AMD', 'mechanism': 'YAP-TEAD inhibitor', 'repositioning_potential': True}
        ],
        'screening_assay': 'TEAD luciferase reporter, α-SMA expression',
        'validation_model': 'Mouse TAC, AngII infusion'
    },
    
    'WWTR1': {
        'gene_name': 'WW Domain Containing Transcription Regulator 1 (TAZ)',
        'uniprot_id': 'Q9GZV5',
        'priority': 4,
        'target_class': 'Transcription Co-activator',
        'pathway': 'Hippo/YAP/TAZ',
        'description': 'TAZ is the paralog of YAP, working with YAP to activate TEAD-dependent transcription of profibrotic genes. TAZ interacts with MRTF-A and Smad3.',
        'rationale': 'YAP and TAZ have overlapping and distinct functions. Combined inhibition may be more effective.',
        'genetic_evidence': 'TAZ knockdown reduces fibrosis',
        'drug_modality': ['Small molecule inhibitor', 'siRNA'],
        'development_stage': 'Research',
        'novelty_score': 7.5,
        'druggability_score': 8.0,
        'safety_score': 7.5,
        'priority_score': 7.7,
        'known_inhibitors': [
            {'name': 'Verteporfin', 'type': 'YAP/TAZ-TEAD', 'status': 'Research'}
        ],
        'screening_assay': 'TEAD luciferase reporter, collagen gel contraction'
    },
    
    'FAP': {
        'gene_name': 'Fibroblast Activation Protein Alpha',
        'uniprot_id': 'Q12884',
        'priority': 5,
        'target_class': 'Serine Protease',
        'pathway': 'Fibroblast Activation',
        'description': 'FAP is a marker of activated myofibroblasts and is a promising target for fibrosis vaccine therapy. FAP vaccine reduces myofibroblast accumulation in post-MI hearts.',
        'rationale': (
            'FAP is specifically expressed on activated fibroblasts but not quiescent cells. '
            'Vaccination against FAP (2024) reduces fibrosis and improves cardiac function. '
            'This represents an innovative immunotherapy approach.'
        ),
        'genetic_evidence': 'FAP+ fibroblast depletion reduces fibrosis',
        'drug_modality': ['Vaccine', 'Small molecule inhibitor', 'Antibody'],
        'development_stage': 'Preclinical (Vaccine)',
        'novelty_score': 8.5,
        'druggability_score': 7.5,
        'safety_score': 8.0,
        'priority_score': 8.0,
        'known_inhibitors': [
            {'name': 'Anti-FAP vaccine', 'type': 'Vaccine', 'evidence': 'Circulation Research 2024', 'results': 'Reduces myofibroblast accumulation post-MI'}
        ],
        'screening_assay': 'FAP enzymatic activity, fibroblast activation markers',
        'validation_model': 'Mouse MI model'
    },
    
    'NPR3': {
        'gene_name': 'Natriuretic Peptide Receptor 3 (NPRC)',
        'uniprot_id': 'P17342',
        'priority': 6,
        'target_class': 'Receptor',
        'pathway': 'Natriuretic Peptide',
        'description': 'NPRC (clearance receptor) deletion is cardioprotective and anti-fibrotic via PKA/PKG activation and TGF-β1/Smad inhibition. Existing drugs sacubitril/valsartan affect this pathway.',
        'rationale': (
            'NPRC deletion activates PKA/PKG → inhibits TGF-β1/Smad pathway. '
            'Sacubitril/valsartan (approved for HF) inhibits neprilysin, increasing natriuretic peptides. '
            'NPRC antagonism is a novel but validated approach.'
        ),
        'genetic_evidence': 'NPRC knockout is cardioprotective in diabetic mice',
        'drug_modality': ['Small molecule antagonist'],
        'development_stage': 'Research',
        'novelty_score': 7.0,
        'druggability_score': 9.0,
        'safety_score': 8.5,
        'priority_score': 8.2,
        'known_inhibitors': [
            {'name': 'NPRC antagonists', 'type': 'Research compounds', 'status': 'Research'},
            {'name': 'Sacubitril/valsartan', 'type': 'Approved', 'mechanism': 'Neprilysin + AT1R', 'indication': 'Heart failure'}
        ],
        'screening_assay': 'cGMP accumulation, fibroblast activation',
        'validation_model': 'Mouse diabetic cardiomyopathy'
    },
    
    'MKL1': {
        'gene_name': 'MKL1 (MRTF-A)',
        'uniprot_id': 'Q969V6',
        'priority': 7,
        'target_class': 'Transcription Factor',
        'pathway': 'MRTF-A/SRF',
        'description': 'MRTF-A links cytoskeletal dynamics to profibrotic gene expression. RhoA-mediated nuclear translocation activates SRF-dependent transcription of α-SMA and CTGF.',
        'rationale': (
            'MRTF-A/SRF regulates α-SMA and CTGF expression. '
            'MRTF-A interacts with YAP/TAZ and Smad3 at multiple levels. '
            'Targeting upstream RhoA may reduce MRTF-A activity.'
        ),
        'genetic_evidence': 'MRTF-A knockdown reduces fibrosis',
        'drug_modality': ['Small molecule (RhoA inhibitors)', 'siRNA'],
        'development_stage': 'Research',
        'novelty_score': 6.5,
        'druggability_score': 7.0,
        'safety_score': 7.5,
        'priority_score': 7.0,
        'known_inhibitors': [
            {'name': 'RhoA inhibitors', 'type': 'Research', 'status': 'Research'}
        ],
        'screening_assay': 'SRF luciferase reporter, α-SMA expression',
        'validation_model': 'Mouse TAC, AngII infusion'
    },
    
    'PIN1': {
        'gene_name': 'Peptidyl-Prolyl Isomerase NIMA-Interacting 1',
        'uniprot_id': 'Q13526',
        'priority': 8,
        'target_class': 'Isomerase',
        'pathway': 'Prolyl Isomerization',
        'description': 'PIN1 facilitates isoproterenol-induced cardiac fibrosis by promoting oxidative stress and activating MEK1/2-ERK1/2 pathway.',
        'rationale': 'PIN1 is activated by isoproterenol and promotes fibrosis via ERK pathway.',
        'genetic_evidence': 'PIN1 knockdown reduces fibrosis',
        'drug_modality': ['Small molecule inhibitor'],
        'development_stage': 'Research',
        'novelty_score': 7.0,
        'druggability_score': 7.5,
        'safety_score': 7.0,
        'priority_score': 7.2,
        'known_inhibitors': [
            {'name': 'PIN1 inhibitors', 'type': 'Research', 'status': 'Research'}
        ],
        'screening_assay': 'PIN1 enzymatic activity (prolyl isomerization)',
        'validation_model': 'Rat isoproterenol model'
    },
    
    'CXCL12': {
        'gene_name': 'C-X-C Motif Chemokine Ligand 12',
        'uniprot_id': 'P48061',
        'priority': 9,
        'target_class': 'Chemokine',
        'pathway': 'CXCR4/7 Axis',
        'description': 'CXCL12 in smooth muscle regulates coronary arteries. CXCR7 deficiency leads to cardiac hypertrophy and fibrosis.',
        'rationale': 'CXCL12/CXCR4/7 axis is important for cardiac homeostasis and repair.',
        'genetic_evidence': 'CXCR7 knockout causes cardiac fibrosis',
        'drug_modality': ['Small molecule antagonist', 'Antibody'],
        'development_stage': 'Research',
        'novelty_score': 6.5,
        'druggability_score': 8.0,
        'safety_score': 7.5,
        'priority_score': 7.3,
        'known_inhibitors': [
            {'name': 'CXCR4/7 antagonists', 'type': 'Research', 'status': 'Development'}
        ],
        'screening_assay': 'CXCL12 binding, fibroblast migration'
    },
    
    'TGFB1': {
        'gene_name': 'Transforming Growth Factor Beta 1',
        'uniprot_id': 'P01137',
        'priority': 10,
        'target_class': 'Cytokine',
        'pathway': 'TGF-β/SMAD',
        'description': 'Canonical fibrosis pathway. TGF-β1 is the master regulator of fibroblast activation. However, systemic inhibition has failed due to toxicity.',
        'rationale': (
            'TGF-β1 is the central mediator but clinical trials failed due to on-target toxicity. '
            'More specific targeting (IL-11, SMAD3) may be safer.'
        ),
        'genetic_evidence': 'Extensive validation but clinical toxicity',
        'drug_modality': ['Neutralizing antibodies', 'Small molecule (TGFβR1 inhibitors)'],
        'development_stage': 'Failed clinical trials',
        'novelty_score': 3.0,
        'druggability_score': 9.0,
        'safety_score': 3.0,
        'priority_score': 5.0,
        'note': 'Priority reduced due to clinical toxicity. Consider downstream targets (IL-11, SMAD3).'
    }
}

def get_top_targets(n=5):
    """Get top N prioritized targets"""
    sorted_targets = sorted(CARDIAC_FIBROSIS_TARGETS.items(), key=lambda x: x[1]['priority_score'], reverse=True)
    return sorted_targets[:n]

def get_targets_by_pathway(pathway):
    """Get targets by pathway"""
    return {k: v for k, v in CARDIAC_FIBROSIS_TARGETS.items() if v['pathway'] == pathway}

def get_targets_by_class(target_class):
    """Get targets by class"""
    return {k: v for k, v in CARDIAC_FIBROSIS_TARGETS.items() if v['target_class'] == target_class}