"""
Cardiac Fibrosis Disease Ontology

Disease definition and pathophysiology for cardiac fibrosis.
Based on 2025-2026 multi-omics research.
"""

CARDIAC_FIBROSIS_ONTOLOGY = {
    'disease_id': 'DOID:0060452',
    'disease_name': 'Cardiac Fibrosis',
    'alternative_names': [
        'Myocardial Fibrosis',
        'Fibrotic Heart Disease',
        'Post-MI Fibrosis',
        'Reactive Fibrosis'
    ],
    'definition': (
        'Cardiac fibrosis is characterized by excessive accumulation of extracellular matrix (ECM) '
        'proteins in the heart, leading to increased myocardial stiffness, impaired cardiac function, '
        'and ultimately heart failure. It results from activated cardiac fibroblasts differentiating '
        'into myofibroblasts and depositing collagen and other ECM components.'
    ),
    'pathophysiology': {
        'primary_cell_type': 'Cardiac Fibroblasts',
        'activated_state': 'Myofibroblasts',
        'key_markers': [
            'ACTA2 (α-SMA)',
            'POSTN (Periostin)',
            'COL1A1 (Collagen I)',
            'COL3A1 (Collagen III)',
            'FAP (Fibroblast Activation Protein)',
            'THBS4 (Thrombospondin-4)',
            'NOX4 (NADPH Oxidase 4)'
        ],
        'trigger_events': [
            'Myocardial infarction (MI)',
            'Hypertension',
            'Diabetic cardiomyopathy',
            'Aging',
            'Chemotherapy-induced cardiotoxicity'
        ]
    },
    'signaling_pathways': {
        'canonical_fibrosis': {
            'pathway': 'TGF-β/SMAD',
            'description': 'Central mediator of fibroblast activation and ECM production',
            'key_components': ['TGFB1', 'SMAD2', 'SMAD3', 'SMAD4', 'TGFβR1', 'TGFβR2'],
            'transcriptional_targets': ['ACTA2', 'COL1A1', 'COL3A1', 'POSTN', 'FN1']
        },
        'mechanotransduction': {
            'pathway': 'YAP/TAZ-TEAD',
            'description': 'Mediates mechanically induced ECM remodeling based on tissue stiffness',
            'key_components': ['YAP1', 'TAZ (WWTR1)', 'TEAD1', 'TEAD4', 'AMOT'],
            'canonical_targets': ['CCN1', 'ACTA2', 'RSPO3', 'CYR61'],
            'drug_target': True,
            'inhibitors': ['Verteporfin']
        },
        'cytoskeletal_transcription': {
            'pathway': 'MRTF-A/SRF',
            'description': 'Links cytoskeletal dynamics to profibrotic gene expression',
            'key_components': ['MKL1 (MRTF-A)', 'SRF', 'MYOCD'],
            'upstream_regulators': ['RHOA', 'ARHGEF12', 'ROCK1'],
            'target_genes': ['ACTA2', 'CTGF', 'TGFBI']
        },
        'inflammation_fibrosis': {
            'pathway': 'IL-11/IL11RA',
            'description': 'IL-11 is a crucial determinant of cardiovascular fibrosis, downstream of TGF-β',
            'key_components': ['IL11', 'IL11RA1', 'STAT3', 'ERK1/2'],
            'evidence': 'IL-11 inhibition attenuates fibrosis; anti-IL-6 has no effect',
            'novel_target': True,
            'priority': 'HIGH'
        },
        'collagen_crosslinking': {
            'pathway': 'LOX/LOXL',
            'description': 'Lysyl oxidase family for ECM collagen and elastin crosslinking',
            'key_components': ['LOX', 'LOXL1', 'LOXL2', 'LOXL3', 'LOXL4'],
            'drug_target': True,
            'inhibitors': ['SNT-5382']
        },
        'natriuretic_peptide': {
            'pathway': 'NPRC/GCY',
            'description': 'Natriuretic peptide clearance receptor impacts cardiac remodeling',
            'key_components': ['NPRC (NPR3)', 'NPRA (NPR1)', 'NPRB (NPR2)', 'GCY (GUCY1A2)'],
            'ligands': ['ANP', 'BNP', 'CNP'],
            'mechanism': 'NPRC deletion → PKA/PKG activation → TGF-β1/Smad inhibition'
        },
        'epigenetic_regulation': {
            'pathway': 'miRNA/TGF-β',
            'description': 'Non-coding RNAs as effectors of TGF-β signaling',
            'key_mirnas': ['miR-29b', 'miR-26a', 'miR-21', 'miR-200c'],
            'targets': {
                'miR-29b': 'Elastic, collagen (Eln, Fbn1, Col1, Col3)',
                'miR-26a': 'Col11, CTGF',
                'miR-21': 'SMAD7, DUSP8'
            }
        }
    },
    'disease_stages': {
        'early': {
            'description': 'Quiescent fibroblasts respond to injury signals',
            'markers': ['PDGFRα', 'TCF21', 'COL1A1 (low)'],
            'reversibility': True
        },
        'intermediate': {
            'description': 'Fibroblast activation and differentiation into myofibroblasts',
            'markers': ['ACTA2', 'POSTN', 'FAP', 'NOX4'],
            'reversibility': Possibly
        },
        'late': {
            'description': 'Established fibrosis with crosslinked collagen',
            'markers': ['LOXL2', 'THBS4', 'COL1A1 (high)', 'FN1'],
            'reversibility': False
        }
    },
    'related_diseases': [
        'Heart Failure (HFrEF)',
        'Diabetic Cardiomyopathy',
        'Hypertensive Heart Disease',
        'Fibrodysplasia Ossificans Progressiva (FOP)',
        'Idiopathic Pulmonary Fibrosis (IPF)'
    ],
    'clinical_outcomes': [
        'Reduced ejection fraction',
        'Increased myocardial stiffness',
        'Diastolic dysfunction',
        'Arrhythmias',
        'Heart failure progression'
    ],
    'animal_models': [
        'TAC (Transverse Aortic Constriction) - pressure overload',
        'MI/IRI (Myocardial Infarction/Ischemia-Reperfusion)',
        'Angiotensin II infusion',
        'Spontaneously Hypertensive Rats (SHR)',
        'db/db mice (diabetic cardiomyopathy)'
    ],
    'multiomics_markers': {
        'scRNAseq': {
            'fibroblast_clusters': ['Col14a1+', 'Pi16+', 'Thbs4+', 'Fap+', 'Acta2+ myofibroblasts'],
            'myofibroblast_signature': ['Acta2', 'Tagln', 'Postn', 'Col1a1', 'Col3a1']
        },
        'bulk_RNAseq': {
            'upregulated': ['COL1A1', 'COL3A1', 'ACTA2', 'POSTN', 'FN1', 'CTGF', 'NOX4'],
            'downregulated': ['TCF21', 'PDGFRα']
        },
        'proteomics': {
            'ECM_components': ['Collagen I', 'Collagen III', 'Fibronectin', 'Periostin'],
            'crosslinking_enzymes': ['LOXL2', 'LOX']
        }
    },
    'treatment_approaches': {
        'prevention': 'Block fibroblast activation',
        'reversal': 'Promote myofibroblast apoptosis or regression',
        'regression': 'Enhance ECM degradation'
    }
}