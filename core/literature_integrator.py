"""
ARP v22 - Literature Integration Module

Real-time data from:
- PubMed (literature)
- ClinicalTrials.gov (clinical trials)
- DrugBank (drug information)
- ChEMBL (bioactivity)
"""

import httpx
import json
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime
import asyncio


# ============================================================================
# API CLIENTS
# ============================================================================

@dataclass
class PubMedArticle:
    """PubMed article data"""
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    journal: str
    year: int
    mesh_terms: List[str]
    keywords: List[str]
    cited_by: int = 0


@dataclass
class ClinicalTrial:
    """Clinical trial data"""
    nct_id: str
    title: str
    phase: str
    status: str
    conditions: List[str]
    interventions: List[str]
    sponsors: List[str]
    start_date: str
    completion_date: Optional[str]
    enrollment: int
    locations: List[str]
    results_posted: bool = False
    url: str = ""


@dataclass
class DrugInfo:
    """Drug information from DrugBank"""
    drugbank_id: str
    name: str
    synonyms: List[str]
    drug_type: str
    indication: str
    mechanism: str
    target: str
    phase: str
    status: str
    smiles: Optional[str] = None
    weight: float = 0.0
    atc_codes: List[str] = field(default_factory=list)


# ============================================================================
# PUBMED CLIENT
# ============================================================================

class PubMedClient:
    """Client for PubMed API via NCBI E-utilities"""
    
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
    
    async def search(
        self,
        query: str,
        max_results: int = 20,
        date_filter: Optional[str] = None,
    ) -> List[str]:
        """
        Search PubMed and return PMIDs.
        
        Args:
            query: Search query
            max_results: Maximum number of results
            date_filter: Date filter (e.g., "5[dp]" for 5 years)
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Search for PMIDs
            params = {
                "db": "pubmed",
                "term": query,
                "retmax": str(max_results),
                "retmode": "json",
                "sort": "relevance",
            }
            if self.api_key:
                params["api_key"] = self.api_key
            if date_filter:
                params["datetype"] = "pdat"
                params["reldate"] = date_filter
            
            try:
                response = await client.get(
                    f"{self.BASE_URL}/esearch.fcgi",
                    params=params,
                )
                response.raise_for_status()
                
                # Handle JSON or text response
                content = response.text.strip()
                if not content:
                    return []
                
                data = json.loads(content)
                id_list = data.get("esearchresult", {}).get("idlist", [])
                return id_list
            except json.JSONDecodeError as e:
                print(f"PubMed JSON parse error: {e}")
                return []
            except Exception as e:
                print(f"PubMed search error: {e}")
                return []
    
    async def fetch_articles(
        self,
        pmids: List[str],
    ) -> List[PubMedArticle]:
        """Fetch article details for given PMIDs"""
        if not pmids:
            return []
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Use XML format for efetch (more reliable)
            params = {
                "db": "pubmed",
                "id": ",".join(pmids),
                "retmode": "xml",
            }
            if self.api_key:
                params["api_key"] = self.api_key
            
            try:
                response = await client.get(
                    f"{self.BASE_URL}/efetch.fcgi",
                    params=params,
                )
                response.raise_for_status()
                
                # Parse XML response
                import xml.etree.ElementTree as ET
                root = ET.fromstring(response.content)
                
                articles = []
                
                for article_elem in root.findall(".//PubmedArticle"):
                    try:
                        # PMID
                        pmid_elem = article_elem.find(".//PMID")
                        pmid = pmid_elem.text if pmid_elem is not None else ""
                        
                        # Title
                        title_elem = article_elem.find(".//ArticleTitle")
                        title = title_elem.text if title_elem is not None else ""
                        
                        # Abstract
                        abstract_parts = []
                        abstract_elem = article_elem.find(".//Abstract")
                        if abstract_elem is not None:
                            for abstract_text_elem in abstract_elem.findall(".//AbstractText"):
                                if abstract_text_elem.text:
                                    abstract_parts.append(abstract_text_elem.text)
                        abstract_text = " ".join(abstract_parts)
                        
                        # Authors
                        authors = []
                        for author_elem in article_elem.findall(".//Author"):
                            last_name = author_elem.find("LastName")
                            fore_name = author_elem.find("ForeName")
                            if last_name is not None:
                                name = last_name.text
                                if fore_name is not None and fore_name.text:
                                    name = f"{fore_name.text} {name}"
                                authors.append(name)
                        
                        # Journal
                        journal_elem = article_elem.find(".//Journal/Title")
                        journal = journal_elem.text if journal_elem is not None else ""
                        
                        # Year
                        pub_date_elem = article_elem.find(".//Journal/JournalIssue/PubDate")
                        year = 2020
                        if pub_date_elem is not None:
                            year_elem = pub_date_elem.find("Year")
                            if year_elem is not None and year_elem.text:
                                try:
                                    year = int(year_elem.text)
                                except:
                                    year = 2020
                        
                        # Mesh terms
                        mesh_terms = []
                        for mesh_elem in article_elem.findall(".//MeshHeading/DescriptorName"):
                            if mesh_elem.text:
                                mesh_terms.append(mesh_elem.text)
                        
                        articles.append(PubMedArticle(
                            pmid=pmid,
                            title=title,
                            abstract=abstract_text,
                            authors=authors,
                            journal=journal,
                            year=year,
                            mesh_terms=mesh_terms,
                            keywords=[],
                        ))
                    except Exception as e:
                        continue
                
                return articles
                
            except Exception as e:
                print(f"PubMed fetch error: {e}")
                return []
    
    async def search_and_fetch(
        self,
        query: str,
        max_results: int = 20,
    ) -> List[PubMedArticle]:
        """Search and fetch articles in one call"""
        try:
            pmids = await self.search(query, max_results)
            if not pmids:
                return []
            return await self.fetch_articles(pmids)
        except Exception as e:
            print(f"PubMed search_and_fetch error: {e}")
            return []


# ============================================================================
# CLINICAL TRIALS CLIENT
# ============================================================================

class ClinicalTrialsClient:
    """Client for ClinicalTrials.gov API v2"""
    
    BASE_URL = "https://clinicaltrials.gov/api/v2"
    
    def __init__(self):
        pass
    
    async def search_trials(
        self,
        condition: str,
        intervention: Optional[str] = None,
        phase: Optional[str] = None,
        status: str = "RECRUITING|ACTIVE_NOT_RECRUITING|COMPLETED",
        max_results: int = 20,
    ) -> List[ClinicalTrial]:
        """
        Search ClinicalTrials.gov for trials.
        
        Args:
            condition: Disease/condition
            intervention: Drug/intervention
            phase: Trial phase (EARLY_PHASE1, PHASE1, PHASE2, PHASE3, PHASE4)
            status: Recruitment status filter
            max_results: Maximum results
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            # Build query
            query_parts = [condition]
            if intervention:
                query_parts.append(intervention)
            query_str = " ".join(query_parts)
            
            params = {
                "query.term": query_str,
                "pageSize": str(max_results),
            }
            
            try:
                response = await client.get(
                    f"{self.BASE_URL}/studies",
                    params=params,
                )
                response.raise_for_status()
                data = response.json()
                
                studies = data.get("studies", [])
                
                trials = []
                for study in studies:
                    try:
                        protocol = study.get("protocolSection", {})
                        identification = protocol.get("identificationModule", {})
                        status_module = protocol.get("statusModule", {})
                        design_module = protocol.get("designModule", {})
                        contacts_module = protocol.get("contactsLocationsModule", {})
                        
                        nct_id = identification.get("nctId", "")
                        
                        # Phase
                        phases = design_module.get("phases", ["Unknown"])
                        if isinstance(phases, str):
                            phases = [phases]
                        phase_str = "/".join(str(p) for p in phases) if phases else "Unknown"
                        
                        # Status
                        status_str = status_module.get("overallStatus", "Unknown")
                        
                        # Conditions
                        conditions = identification.get("conditions", [])
                        if not isinstance(conditions, list):
                            conditions = [conditions] if conditions else []
                        
                        # Interventions
                        arms_interventions = design_module.get("armsInterventions", [])
                        if not isinstance(arms_interventions, list):
                            arms_interventions = [arms_interventions] if arms_interventions else []
                        interventions = [a.get("interventionName", "") for a in arms_interventions if isinstance(a, dict)]
                        
                        # Sponsors
                        org = identification.get("organization", {})
                        full_name = org.get("fullName", "") if isinstance(org, dict) else ""
                        sponsors = [full_name] if full_name else []
                        
                        # Dates
                        start_date = status_module.get("startDateStruct", {})
                        start_date_str = ""
                        if isinstance(start_date, dict):
                            start_date_str = start_date.get("date", "")
                        
                        completion = status_module.get("primaryCompletionDateStruct", {})
                        completion_date = None
                        if isinstance(completion, dict):
                            completion_date = completion.get("date", None)
                        
                        # Enrollment
                        enrollment = design_module.get("enrollmentInfo", {})
                        enrollment_count = 0
                        if isinstance(enrollment, dict):
                            enrollment_count = enrollment.get("count", 0) or 0
                        
                        # Locations
                        locations = contacts_module.get("locations", [])
                        if not isinstance(locations, list):
                            locations = [locations] if locations else []
                        location_names = []
                        for loc in locations[:5]:
                            if isinstance(loc, dict):
                                facility = loc.get("facility", "")
                                if facility:
                                    location_names.append(facility)
                        
                        trials.append(ClinicalTrial(
                            nct_id=nct_id,
                            title=identification.get("briefTitle", ""),
                            phase=phase_str,
                            status=status_str,
                            conditions=conditions,
                            interventions=interventions,
                            sponsors=sponsors,
                            start_date=start_date_str,
                            completion_date=completion_date,
                            enrollment=enrollment_count,
                            locations=location_names,
                        ))
                    except Exception as e:
                        continue
                
                return trials
                
            except Exception as e:
                print(f"ClinicalTrials API error: {e}")
                return []


# ============================================================================
# LITERATURE INTEGRATOR
# ============================================================================

class LiteratureIntegrator:
    """
    Unified literature integration for ARP v22.
    Combines PubMed, ClinicalTrials.gov for comprehensive research.
    """
    
    def __init__(self, pubmed_api_key: Optional[str] = None):
        # Use provided key or check environment
        import os
        api_key = pubmed_api_key or os.environ.get('NCBI_API_KEY')
        self.pubmed = PubMedClient(api_key)
        self.clinical_trials = ClinicalTrialsClient()
    
    async def get_target_literature(
        self,
        gene_name: str,
        disease: str,
        max_articles: int = 10,
    ) -> Dict[str, Any]:
        """
        Get literature for a target in a disease context.
        
        Returns:
            Dict with articles, trials, and drug info
        """
        # Build search queries
        target_disease_query = f"{gene_name}[Title/Abstract] AND {disease}[Title/Abstract]"
        
        # Fetch in parallel
        try:
            articles, trials = await asyncio.gather(
                self.pubmed.search_and_fetch(target_disease_query, max_articles),
                self.clinical_trials.search_trials(
                    condition=disease,
                    intervention=gene_name,
                    max_results=max_articles // 2,
                ),
            )
        except Exception as e:
            print(f"Literature fetch error: {e}")
            articles = []
            trials = []
        
        # Ensure articles is a list
        if not isinstance(articles, list):
            articles = [articles] if articles else []
        
        # Ensure trials is a list
        if not isinstance(trials, list):
            trials = [trials] if trials else []
        
        return {
            "gene": gene_name,
            "disease": disease,
            "articles": [
                {
                    "pmid": getattr(a, 'pmid', str(a)) if not isinstance(a, dict) else a.get('pmid', ''),
                    "title": getattr(a, 'title', '') if not isinstance(a, dict) else a.get('title', ''),
                    "abstract": (getattr(a, 'abstract', '')[:500] + "..." if len(getattr(a, 'abstract', '')) > 500 else getattr(a, 'abstract', '')) if not isinstance(a, dict) else (a.get('abstract', '')[:500] + "..." if len(a.get('abstract', '')) > 500 else a.get('abstract', '')),
                    "authors": getattr(a, 'authors', [])[:5] if not isinstance(a, dict) else a.get('authors', [])[:5],
                    "journal": getattr(a, 'journal', '') if not isinstance(a, dict) else a.get('journal', ''),
                    "year": getattr(a, 'year', 2020) if not isinstance(a, dict) else a.get('year', 2020),
                    "mesh_terms": getattr(a, 'mesh_terms', [])[:10] if not isinstance(a, dict) else a.get('mesh_terms', [])[:10],
                }
                for a in articles[:max_articles]
            ],
            "clinical_trials": [
                {
                    "nct_id": getattr(t, 'nct_id', '') if not isinstance(t, dict) else t.get('nct_id', ''),
                    "title": getattr(t, 'title', '') if not isinstance(t, dict) else t.get('title', ''),
                    "phase": getattr(t, 'phase', '') if not isinstance(t, dict) else t.get('phase', ''),
                    "status": getattr(t, 'status', '') if not isinstance(t, dict) else t.get('status', ''),
                    "enrollment": getattr(t, 'enrollment', 0) if not isinstance(t, dict) else t.get('enrollment', 0),
                    "interventions": getattr(t, 'interventions', []) if not isinstance(t, dict) else t.get('interventions', []),
                }
                for t in trials
            ],
            "summary": {
                "total_articles": len(articles),
                "total_trials": len(trials),
                "recruiting_trials": sum(1 for t in trials if (getattr(t, 'status', '') if not isinstance(t, dict) else t.get('status', '')).startswith('RECRUITING')),
            }
        }
    
    def get_evidence_summary(
        self,
        literature_data: Dict[str, Any],
    ) -> str:
        """Generate a text summary of the literature evidence"""
        summary_parts = []
        
        # Articles summary
        articles = literature_data.get("articles", [])
        if articles:
            summary_parts.append(f"Found {len(articles)} relevant articles:")
            for art in articles[:3]:
                summary_parts.append(f"  - {art['title'][:80]}... ({art['year']})")
        
        # Trials summary
        trials = literature_data.get("clinical_trials", [])
        if trials:
            summary_parts.append(f"\nFound {len(trials)} clinical trials:")
            for trial in trials[:3]:
                summary_parts.append(
                    f"  - {trial['nct_id']}: {trial['phase']} - {trial['status']}"
                )
        
        return "\n".join(summary_parts) if summary_parts else "No literature found"


# ============================================================================
# SYNC CONVENIENCE FUNCTIONS
# ============================================================================

def get_target_literature_sync(
    gene_name: str,
    disease: str,
    max_articles: int = 10,
) -> Dict[str, Any]:
    """Synchronous wrapper for get_target_literature"""
    integrator = LiteratureIntegrator()
    return asyncio.run(integrator.get_target_literature(gene_name, disease, max_articles))
