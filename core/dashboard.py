"""
ARP v22 - Dashboard / Report Generator

Generates HTML reports for the drug discovery pipeline results.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime
import json


@dataclass
class DashboardConfig:
    """Configuration for dashboard generation"""
    title: str = "ARP v22 Drug Discovery Dashboard"
    include_charts: bool = True
    theme: str = "light"  # "light" or "dark"
    logo_url: Optional[str] = None
    output_format: str = "html"  # "html" or "json"


class DashboardGenerator:
    """
    Generates interactive HTML dashboard for ARP v22 results.
    """
    
    def __init__(self, config: Optional[DashboardConfig] = None):
        self.config = config or DashboardConfig()
    
    def generate_pipeline_report(
        self,
        disease: str,
        engine1_result: Dict,
        engine2_results: Dict[str, Any],
        engine3_results: Dict[str, Any],
    ) -> str:
        """Generate a complete pipeline report HTML"""
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.config.title} - {disease.upper()}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{ font-size: 2rem; margin-bottom: 0.5rem; }}
        .header .subtitle {{ opacity: 0.9; }}
        .container {{ max-width: 1400px; margin: 2rem auto; padding: 0 1rem; }}
        .card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }}
        .card h2 {{
            color: #667eea;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #f0f0f0;
        }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }}
        .stat-box {{
            background: #f8f9fa;
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }}
        .stat-value {{ font-size: 2.5rem; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #666; font-size: 0.9rem; }}
        .target-list {{ list-style: none; }}
        .target-item {{
            padding: 1rem;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .target-item:last-child {{ border-bottom: none; }}
        .target-rank {{
            background: #667eea;
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.85rem;
        }}
        .target-name {{ font-weight: 600; }}
        .target-score {{ 
            background: #e8f5e9;
            color: #2e7d32;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-weight: 600;
        }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 500;
        }}
        .badge-approved {{ background: #c8e6c9; color: #2e7d32; }}
        .badge-phase3 {{ background: #bbdefb; color: #1565c0; }}
        .badge-phase2 {{ background: #fff9c4; color: #f57f17; }}
        .badge-phase1 {{ background: #ffe0b2; color: #e65100; }}
        .badge-preclinical {{ background: #f5f5f5; color: #616161; }}
        .table {{ width: 100%; border-collapse: collapse; }}
        .table th, .table td {{ padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }}
        .table th {{ background: #f8f9fa; font-weight: 600; color: #666; }}
        .score-bar {{
            height: 8px;
            background: #e0e0e0;
            border-radius: 4px;
            overflow: hidden;
        }}
        .score-bar-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }}
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #999;
            font-size: 0.85rem;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🧬 ARP v22 Drug Discovery Report</h1>
        <div class="subtitle">{disease.upper()} | Generated {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
    </div>
    
    <div class="container">
        <!-- Summary Stats -->
        <div class="card">
            <h2>📊 Pipeline Summary</h2>
            <div class="grid">
                <div class="stat-box">
                    <div class="stat-value">{len(engine1_result.get('targets', []))}</div>
                    <div class="stat-label">Targets Evaluated</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{len(engine2_results)}</div>
                    <div class="stat-label">Modality Routes</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{sum(len(r.get('candidates', [])) for r in engine3_results.values())}</div>
                    <div class="stat-label">Candidates Generated</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value">{sum(1 for r in engine3_results.values() for c in r.get('candidates', []) if c.get('development_stage') == 'approved')}</div>
                    <div class="stat-label">Approved Drugs</div>
                </div>
            </div>
        </div>
        
        <!-- Top Targets -->
        <div class="card">
            <h2>🎯 Prioritized Targets (Engine 1)</h2>
            <ul class="target-list">
"""
        
        # Add targets
        targets = engine1_result.get('targets', [])[:10]
        for i, target in enumerate(targets, 1):
            score = target.get('priority_score', 0)
            gene = target.get('gene_name', target.get('gene', 'Unknown'))
            modalities = target.get('recommended_modalities', [])[:2]
            modalities_str = ', '.join(modalities) if modalities else 'N/A'
            
            html += f"""
                <li class="target-item">
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <span class="target-rank">{i}</span>
                        <div>
                            <div class="target-name">{gene}</div>
                            <div style="font-size: 0.85rem; color: #666;">Modalities: {modalities_str}</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="target-score">{score:.3f}</span>
                    </div>
                </li>
"""
        
        html += """
            </ul>
        </div>
        
        <!-- Modality Routing -->
        <div class="card">
            <h2>🔄 Modality Routing (Engine 2)</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Target</th>
                        <th>Recommended Modality</th>
                        <th>Score</th>
                        <th>Timeline</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for gene, routing in list(engine2_results.items())[:10]:
            modalities = routing.get('all_modalities', [])
            if modalities:
                top_mod = modalities[0]
                html += f"""
                    <tr>
                        <td><strong>{gene}</strong></td>
                        <td>{top_mod.get('modality', 'N/A').replace('_', ' ').title()}</td>
                        <td>
                            <div class="score-bar" style="width: 100px;">
                                <div class="score-bar-fill" style="width: {top_mod.get('score', 0) * 100}%;"></div>
                            </div>
                            {top_mod.get('score', 0):.2f}
                        </td>
                        <td>{top_mod.get('timeline', 'N/A')} years</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <!-- Candidates -->
        <div class="card">
            <h2>💊 Candidate Compounds (Engine 3)</h2>
            <table class="table">
                <thead>
                    <tr>
                        <th>Target</th>
                        <th>Compound</th>
                        <th>Stage</th>
                        <th>ADMET Score</th>
                        <th>Composite</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        for gene, data in engine3_results.items():
            candidates = data.get('top_10', data.get('candidates', []))[:3]
            for c in candidates:
                stage = c.get('stage', 'unknown')
                badge_class = f"badge-{stage.lower().replace(' ', '-').replace('.', '')}"
                
                html += f"""
                    <tr>
                        <td><strong>{gene}</strong></td>
                        <td>{c.get('name', 'Unknown')}</td>
                        <td><span class="badge {badge_class}">{stage.upper()}</span></td>
                        <td>{c.get('admet_score', 0):.2f}</td>
                        <td><strong>{c.get('composite_score', c.get('score', 0)):.3f}</strong></td>
                    </tr>
"""
        
        html += f"""
                </tbody>
            </table>
        </div>
        
        <!-- Footer -->
        <div class="footer">
            Generated by ARP v22 Drug Discovery Pipeline | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_target_report(
        self,
        target_data: Dict[str, Any],
    ) -> str:
        """Generate a detailed report for a single target"""
        
        gene = target_data.get('gene', 'Unknown')
        disease = target_data.get('disease', 'Unknown')
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Target Report: {gene}</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; }}
        .section {{ background: white; border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
        h2 {{ color: #667eea; margin-bottom: 1rem; }}
        .score-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; }}
        .score-item {{ background: #f8f9fa; padding: 1rem; border-radius: 8px; text-align: center; }}
        .score-value {{ font-size: 1.5rem; font-weight: bold; color: #667eea; }}
        .score-label {{ font-size: 0.85rem; color: #666; }}
        .compound-list {{ list-style: none; }}
        .compound-item {{ padding: 1rem; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 {gene}</h1>
        <p>Disease: {disease.replace('_', ' ').title()}</p>
    </div>
    
    <div class="section">
        <h2>📊 Target Scores</h2>
        <div class="score-grid">
"""
        
        scores = target_data.get('scores', {})
        for dim, score in scores.items():
            if isinstance(score, (int, float)):
                html += f"""
            <div class="score-item">
                <div class="score-value">{score:.2f}</div>
                <div class="score-label">{dim.replace('_', ' ').title()}</div>
            </div>
"""
        
        html += """
        </div>
    </div>
    
    <div class="section">
        <h2>💊 Top Compounds</h2>
        <ul class="compound-list">
"""
        
        candidates = target_data.get('candidates', {}).get('top_10', [])
        for c in candidates[:5]:
            html += f"""
            <li class="compound-item">
                <span><strong>{c.get('name', 'Unknown')}</strong></span>
                <span>{c.get('stage', 'unknown').upper()} | Score: {c.get('composite_score', 0):.3f}</span>
            </li>
"""
        
        html += """
        </ul>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_report(self, html: str, filepath: str):
        """Save HTML report to file"""
        with open(filepath, 'w') as f:
            f.write(html)
        return filepath


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def generate_pipeline_html_report(
    disease: str,
    engine1_result: Dict,
    engine2_results: Dict[str, Any],
    engine3_results: Dict[str, Any],
    output_path: str = "arp22_report.html",
) -> str:
    """Generate and save a pipeline report"""
    generator = DashboardGenerator()
    html = generator.generate_pipeline_report(
        disease, engine1_result, engine2_results, engine3_results
    )
    generator.save_report(html, output_path)
    return output_path


def generate_target_html_report(
    target_data: Dict[str, Any],
    output_path: str = "target_report.html",
) -> str:
    """Generate and save a target-specific report"""
    generator = DashboardGenerator()
    html = generator.generate_target_report(target_data)
    generator.save_report(html, output_path)
    return output_path
