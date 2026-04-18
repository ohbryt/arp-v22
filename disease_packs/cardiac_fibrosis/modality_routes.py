"""
Cardiac Fibrosis Modality Routes

Recommended treatment modalities for cardiac fibrosis based on target and disease characteristics.
"""

CARDIAC_FIBROSIS_MODALITY_ROUTES = {
    'small_molecule': {
        'description': 'Small molecule inhibitors for intracellular targets and enzymes',
        'recommended_targets': [
            'LOXL2',  # Best druggable enzyme
            'YAP1',   # Verteporfin repositioning
            'NPR3',   # Clearance receptor antagonism
            'PIN1',   # Isomerase inhibition
            'MKL1'    # Via RhoA pathway
        ],
        'development_approach': [
            'Drug repositioning (Verteporfin for AMD → cardiac fibrosis)',
            'Structure-based design for LOXL2',
            'High-throughput screening for novel scaffolds'
        ],
        'admet_considerations': [
            'Cardiac tissue penetration required',
            'Long-term safety monitoring',
            'Avoid off-target effects on normal ECM'
        ]
    },
    
    'biologic': {
        'description': 'Biologics for extracellular targets and cytokines',
        'recommended_targets': [
            'IL11',   # mAb or siRNA
            'FAP',    # Vaccine or mAb
            'LOXL2',  # mAb (alternative to small molecule)
            'CXCL12'  # Antibody or peptide antagonist
        ],
        'development_approach': [
            'Anti-IL-11 monoclonal antibodies (like anti-TGFβ approaches)',
            'FAP-targeting vaccine (innovative)',
            'IL11RA-targeted siRNA delivery to heart'
        ],
        'admet_considerations': [
            'Protein degradation issues',
            'Immunogenicity risk',
            'Delivery to cardiac tissue challenging',
            'May require tissue-specific delivery'
        ]
    },
    
    'natural_compound': {
        'description': 'Natural products with anti-fibrotic activity',
        'recommended_targets': [
            'TGF-β pathway (quercetin, curcumin)',
            'NOX4 (epicatechin)',
            'NF-κB pathway (curcumin, resveratrol)',
            'SIRT1 activation (resveratrol)',
            'AMPK activation (berberine)'
        ],
        'development_approach': [
            'Bioavailability enhancement (cocrystal formation)',
            'Synergistic combinations',
            'Multi-target approach for complex fibrosis'
        ],
        'specific_compounds': {
            'quercetin': {
                'mechanism': ['TGF-β/Smad3 inhibition', 'Antioxidant', 'NOX4 reduction'],
                'evidence': 'Established preclinical',
                'dose_equivalent': '500-1000mg/day',
                'bioavailability_issue': True,
                'enhancement': 'Cocrystal with ascorbic acid or citric acid'
            },
            'curcumin': {
                'mechanism': ['NF-κB inhibition', 'TGF-β modulation', 'Anti-inflammatory'],
                'evidence': 'Established preclinical',
                'dose_equivalent': '500-1000mg/day',
                'bioavailability_issue': True,
                'enhancement': 'Piperine cocrystal or liposomal'
            },
            'resveratrol': {
                'mechanism': ['SIRT1 activation', 'AMPK activation', 'Anti-fibrotic'],
                'evidence': 'Moderate preclinical',
                'dose_equivalent': '150-500mg/day',
                'bioavailability_issue': True,
                'enhancement': 'Nicotinamide cocrystal'
            },
            'epicatechin': {
                'mechanism': ['NOX4 inhibition', 'Antioxidant', 'Mitochondrial protection'],
                'evidence': 'Moderate preclinical',
                'dose_equivalent': '1mg/kg/day',
                'bioavailability': '65% (moderate)'
            },
            'berberine': {
                'mechanism': ['AMPK activation', 'Anti-inflammatory', 'Anti-diabetic'],
                'evidence': 'Strong metabolic effects',
                'dose_equivalent': '500-1500mg/day',
                'bioavailability_issue': True,
                'enhancement': 'Liposomal or piperine'
            }
        }
    },
    
    'repurposing': {
        'description': 'Repositioning of approved drugs for cardiac fibrosis',
        'recommended_drugs': [
            {
                'drug': 'Pirfenidone',
                'original_indication': 'Idiopathic Pulmonary Fibrosis (IPF)',
                'mechanism': ['Multi-cytokine inhibition', 'TGF-β modulation', 'NF-κB inhibition'],
                'evidence': 'Preclinical cardiac fibrosis',
                'status': 'Approved for IPF',
                'cardiac_trial_status': 'Needed'
            },
            {
                'drug': 'Nintedanib',
                'original_indication': 'Idiopathic Pulmonary Fibrosis (IPF)',
                'mechanism': ['PDGFR inhibition', 'FGFR inhibition', 'VEGFR inhibition'],
                'evidence': 'Preclinical cardiac fibrosis',
                'status': 'Approved for IPF',
                'cardiac_trial_status': 'Needed'
            },
            {
                'drug': 'Verteporfin',
                'original_indication': 'Age-related Macular Degeneration (AMD)',
                'mechanism': ['YAP-TEAD inhibition', 'Anti-angiogenic'],
                'evidence': 'Strong preclinical cardiac fibrosis',
                'status': 'FDA-approved for AMD',
                'cardiac_trial_status': 'Preclinical'
            },
            {
                'drug': 'Losartan',
                'original_indication': 'Hypertension',
                'mechanism': ['AT1R blockade', 'TGF-β reduction'],
                'evidence': 'Clinical (some cardiac effects)',
                'status': 'Approved for hypertension',
                'cardiac_trial_status': 'Mixed results'
            },
            {
                'drug': 'Sacubitril/valsartan',
                'original_indication': 'Heart Failure',
                'mechanism': ['Neprilysin + AT1R inhibition', '↑ Natriuretic peptides'],
                'evidence': 'Approved for HF, anti-fibrotic',
                'status': 'FDA-approved for HF',
                'cardiac_trial_status': 'Approved'
            }
        ]
    },
    
    'combination_therapy': {
        'description': 'Multi-target combinations for synergistic effects',
        'recommended_combinations': [
            {
                'name': 'Triple Natural Combination',
                'components': ['Quercetin', 'Curcumin', 'Resveratrol'],
                'targets': ['TGF-β/Smad3', 'NF-κB', 'SIRT1/AMPK'],
                'rationale': 'Address multiple fibrosis pathways synergistically',
                'bioavailability_enhancement': 'Required for quercetin + curcumin'
            },
            {
                'name': 'Targeted + Natural',
                'components': ['Verteporfin (YAP/TAZ)', 'Quercetin'],
                'targets': ['YAP/TAZ-TEAD', 'TGF-β'],
                'rationale': 'Combine targeted therapy with broad anti-fibrotic'
            },
            {
                'name': 'Biologic + Small Molecule',
                'components': ['Anti-IL-11 mAb', 'LOXL2 inhibitor'],
                'targets': ['IL-11/STAT3', 'Collagen crosslinking'],
                'rationale': 'Block multiple fibrosis mechanisms'
            }
        ]
    }
}