"""
AI SEO Audit Agent - 3-Agent Pipeline
Built with Gemini API, Jina AI Reader, and SerpAPI

This script implements a sequential 3-agent system that:
1. Page Auditor Agent - Scrapes and analyzes webpage structure
2. SERP Analyst Agent - Analyzes Google search results for keywords
3. Optimization Advisor Agent - Generates comprehensive SEO report

Author: Built for non-technical users
License: MIT
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Configuration for API keys and settings"""
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

    # Jina AI Reader API (no key needed - completely free!)
    JINA_READER_URL = "https://r.jina.ai/"

    # Gemini Model
    GEMINI_MODEL = "gemini-2.5-flash"  # Using newest Gemini 2.5 model

    # Output settings
    REPORTS_DIR = "reports"


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_api_keys():
    """Validate that all required API keys are present"""
    missing_keys = []

    if not Config.GEMINI_API_KEY:
        missing_keys.append("GEMINI_API_KEY")
    if not Config.SERPAPI_KEY:
        missing_keys.append("SERPAPI_KEY")

    if missing_keys:
        print("\n❌ ERROR: Missing API keys!")
        print("Missing keys:", ", ".join(missing_keys))
        print("\nPlease create a .env file with:")
        print("GEMINI_API_KEY=your_gemini_key_here")
        print("SERPAPI_KEY=your_serpapi_key_here")
        print("\nGet free keys from:")
        print("- Gemini: https://aistudio.google.com/apikey")
        print("- SerpAPI: https://serpapi.com (free tier)")
        return False

    return True


def clean_url(url: str) -> str:
    """Ensure URL has proper protocol"""
    if not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url


def save_report(content: str, url: str):
    """Save SEO report to file"""
    # Create safe filename from URL
    filename = url.replace('https://', '').replace('http://', '').replace('/', '_')
    filename = f"seo_report_{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = os.path.join(Config.REPORTS_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath


# ============================================================================
# AGENT 1: PAGE AUDITOR
# ============================================================================

class PageAuditorAgent:
    """
    Agent 1: Scrapes webpage using Jina AI Reader and analyzes page structure.

    Uses Jina AI Reader API (free, no auth required) to convert any webpage
    to clean markdown, then uses Gemini to analyze SEO elements.
    """

    def __init__(self, gemini_model):
        self.model = gemini_model
        print("✅ Page Auditor Agent initialized")

    def scrape_page(self, url: str) -> Optional[str]:
        """
        Scrape webpage content using Jina AI Reader API
        Returns clean markdown content suitable for LLM processing
        """
        print(f"\n📄 Scraping page: {url}")

        try:
            # Jina AI Reader API - just prefix URL with r.jina.ai/
            jina_url = Config.JINA_READER_URL + url

            response = requests.get(jina_url, timeout=30)
            response.raise_for_status()

            content = response.text
            print(f"✅ Successfully scraped {len(content)} characters")
            return content

        except requests.exceptions.RequestException as e:
            print(f"❌ Error scraping page: {e}")
            return None

    def analyze_page(self, url: str, content: str) -> Optional[Dict]:
        """
        Analyze page content using Gemini to extract SEO insights
        """
        print("\n🔍 Analyzing page structure and SEO elements...")

        prompt = f"""You are an expert SEO auditor analyzing a webpage.

URL: {url}

PAGE CONTENT (in markdown format):
{content[:15000]}

Analyze this webpage and provide a comprehensive SEO audit in JSON format with these exact fields:

{{
  "title_tag": "The page title (or 'Not found' if missing)",
  "meta_description": "The meta description (or 'Not found' if missing)",
  "primary_heading": "The main H1 heading",
  "secondary_headings": ["H2 heading 1", "H2 heading 2", "..."],
  "word_count": estimated_word_count,
  "content_summary": "Brief 2-3 sentence summary of page content and topic",
  "technical_findings": [
    "Finding 1: e.g., Missing meta description",
    "Finding 2: e.g., Title tag too short (under 30 chars)",
    "Finding 3: e.g., Multiple H1 tags found",
    "..."
  ],
  "content_opportunities": [
    "Opportunity 1: e.g., Add more internal links",
    "Opportunity 2: e.g., Expand thin content sections",
    "..."
  ],
  "primary_keyword": "The main keyword/topic this page targets",
  "secondary_keywords": ["keyword1", "keyword2", "keyword3"],
  "search_intent": "informational/transactional/navigational/commercial"
}}

Be specific and actionable in your findings. Return ONLY valid JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]

            audit_results = json.loads(result_text)
            print("✅ Page audit complete")
            return audit_results

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            print("Raw response:", response.text[:500])
            return None
        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return None

    def run(self, url: str) -> Optional[Dict]:
        """Main execution method for Page Auditor Agent"""
        print("\n" + "="*70)
        print("🤖 AGENT 1: PAGE AUDITOR")
        print("="*70)

        # Step 1: Scrape the page
        content = self.scrape_page(url)
        if not content:
            return None

        # Step 2: Analyze with Gemini
        audit_results = self.analyze_page(url, content)
        if not audit_results:
            return None

        print("\n📊 Key Findings:")
        print(f"  - Primary Keyword: {audit_results.get('primary_keyword', 'N/A')}")
        print(f"  - Word Count: {audit_results.get('word_count', 'N/A')}")
        print(f"  - Technical Issues: {len(audit_results.get('technical_findings', []))}")

        return audit_results


# ============================================================================
# AGENT 2: SERP ANALYST
# ============================================================================

class SerpAnalystAgent:
    """
    Agent 2: Analyzes Google search results for target keywords.

    Uses SerpAPI to fetch live Google search results, then uses Gemini
    to analyze competitor pages and identify patterns.
    """

    def __init__(self, gemini_model):
        self.model = gemini_model
        print("✅ SERP Analyst Agent initialized")

    def fetch_serp_results(self, keyword: str) -> Optional[List[Dict]]:
        """
        Fetch Google search results using SerpAPI
        """
        print(f"\n🔎 Searching Google for: '{keyword}'")

        try:
            params = {
                "q": keyword,
                "api_key": Config.SERPAPI_KEY,
                "num": 10,  # Top 10 results
                "engine": "google"
            }

            response = requests.get("https://serpapi.com/search", params=params, timeout=30)
            response.raise_for_status()

            data = response.json()
            organic_results = data.get("organic_results", [])

            print(f"✅ Found {len(organic_results)} organic results")
            return organic_results

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching SERP results: {e}")
            return None

    def analyze_serp(self, keyword: str, serp_results: List[Dict]) -> Optional[Dict]:
        """
        Analyze SERP results using Gemini to identify patterns and opportunities
        """
        print("\n🔍 Analyzing SERP patterns and competitor strategies...")

        # Format SERP results for Gemini
        serp_summary = []
        for i, result in enumerate(serp_results[:10], 1):
            serp_summary.append({
                "rank": i,
                "title": result.get("title", ""),
                "url": result.get("link", ""),
                "snippet": result.get("snippet", "")
            })

        prompt = f"""You are an expert SERP analyst reviewing Google search results.

KEYWORD: "{keyword}"

TOP 10 GOOGLE RESULTS:
{json.dumps(serp_summary, indent=2)}

Analyze these search results and provide insights in JSON format:

{{
  "serp_overview": {{
    "dominant_content_types": ["blog posts", "product pages", "videos", "etc"],
    "average_title_length": estimated_average,
    "common_title_patterns": ["Pattern 1", "Pattern 2", "..."]
  }},
  "competitor_patterns": {{
    "common_themes": ["Theme 1", "Theme 2", "..."],
    "content_angles": ["Angle 1", "Angle 2", "..."],
    "key_features": ["Feature 1", "Feature 2", "..."]
  }},
  "opportunities": [
    "Opportunity 1: e.g., No results directly address X",
    "Opportunity 2: e.g., Could create more comprehensive guide",
    "..."
  ],
  "content_gaps": [
    "Gap 1: Missing information about...",
    "Gap 2: No in-depth coverage of...",
    "..."
  ],
  "recommended_approach": "2-3 sentences on how to differentiate and rank for this keyword"
}}

Return ONLY valid JSON, no other text."""

        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()

            # Remove markdown code blocks if present
            if result_text.startswith('```'):
                result_text = result_text.split('```')[1]
                if result_text.startswith('json'):
                    result_text = result_text[4:]

            serp_analysis = json.loads(result_text)
            print("✅ SERP analysis complete")
            return serp_analysis

        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON response: {e}")
            return None
        except Exception as e:
            print(f"❌ Error during SERP analysis: {e}")
            return None

    def run(self, page_audit: Dict) -> Optional[Dict]:
        """Main execution method for SERP Analyst Agent"""
        print("\n" + "="*70)
        print("🤖 AGENT 2: SERP ANALYST")
        print("="*70)

        # Get primary keyword from page audit
        primary_keyword = page_audit.get("primary_keyword", "")
        if not primary_keyword:
            print("❌ No primary keyword found in page audit")
            return None

        # Step 1: Fetch SERP results
        serp_results = self.fetch_serp_results(primary_keyword)
        if not serp_results:
            return None

        # Step 2: Analyze with Gemini
        serp_analysis = self.analyze_serp(primary_keyword, serp_results)
        if not serp_analysis:
            return None

        # Add SERP results to analysis
        serp_analysis["keyword"] = primary_keyword
        serp_analysis["top_results"] = serp_results[:10]

        print("\n📊 Key Findings:")
        print(f"  - Content Types: {', '.join(serp_analysis.get('serp_overview', {}).get('dominant_content_types', []))}")
        print(f"  - Opportunities Found: {len(serp_analysis.get('opportunities', []))}")

        return serp_analysis


# ============================================================================
# AGENT 3: OPTIMIZATION ADVISOR
# ============================================================================

class OptimizationAdvisorAgent:
    """
    Agent 3: Combines page audit and SERP analysis to generate
    a comprehensive SEO optimization report with prioritized recommendations.
    """

    def __init__(self, gemini_model):
        self.model = gemini_model
        print("✅ Optimization Advisor Agent initialized")

    def generate_report(self, url: str, page_audit: Dict, serp_analysis: Dict) -> Optional[str]:
        """
        Generate comprehensive SEO report using Gemini
        """
        print("\n📝 Generating comprehensive SEO optimization report...")

        prompt = f"""You are a senior SEO strategist creating a professional audit report.

URL ANALYZED: {url}

PAGE AUDIT RESULTS:
{json.dumps(page_audit, indent=2)}

SERP ANALYSIS RESULTS:
{json.dumps(serp_analysis, indent=2)}

Create a comprehensive, professional SEO Audit Report in Markdown format with the following structure:

# SEO Audit Report

**Website:** {url}
**Date:** {datetime.now().strftime('%B %d, %Y')}
**Primary Keyword:** {page_audit.get('primary_keyword', 'N/A')}

---

## Executive Summary

[2-3 paragraph overview of overall SEO health, main opportunities, and expected impact]

---

## 1. Technical & On-Page Analysis

### Current Status
- **Title Tag:** [Analysis with character count]
- **Meta Description:** [Analysis with character count]
- **Primary Heading (H1):** [Analysis]
- **Content Length:** [Word count and assessment]
- **Search Intent Match:** [How well content matches intent]

### Technical Findings
[List all technical issues found with severity indicators]

### Content Opportunities
[List content improvement opportunities]

---

## 2. Keyword Analysis

### Target Keywords
- **Primary:** {page_audit.get('primary_keyword', 'N/A')}
- **Secondary:** {', '.join(page_audit.get('secondary_keywords', []))}

### Search Intent
[Analysis of search intent and how well page matches it]

---

## 3. Competitive SERP Analysis

### SERP Landscape
[Overview of what's ranking and why]

### Competitor Patterns
[What successful competitors are doing]

### Content Gaps & Opportunities
[Specific gaps in the SERP that can be exploited]

---

## 4. Prioritized Recommendations

### 🔴 P0 - Critical (Fix Immediately)
1. [Most urgent issue with specific action steps]
2. [Second critical issue]
[etc.]

### 🟡 P1 - High Priority (Fix This Week)
1. [Important optimization with implementation details]
2. [Second high priority item]
[etc.]

### 🟢 P2 - Medium Priority (Fix This Month)
1. [Valuable improvement with steps]
2. [Second medium priority item]
[etc.]

---

## 5. Implementation Roadmap

### Week 1: Critical Fixes
- [Specific action items]

### Week 2-3: Content Enhancements
- [Specific action items]

### Month 2: Strategic Improvements
- [Specific action items]

---

## 6. Expected Impact

### Quick Wins (1-4 weeks)
- [Expected improvements]

### Medium-term (1-3 months)
- [Expected improvements]

### Long-term (3-6 months)
- [Expected improvements]

---

## Next Steps

1. [First action to take]
2. [Second action to take]
3. [Third action to take]

---

*Report generated by AI SEO Audit Agent*

Make the report detailed, specific, and actionable. Use real data from the audit results. Include character counts, specific examples, and concrete next steps. Write in a professional but accessible tone."""

        try:
            response = self.model.generate_content(prompt)
            report = response.text.strip()
            print("✅ Report generation complete")
            return report

        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return None

    def run(self, url: str, page_audit: Dict, serp_analysis: Dict) -> Optional[str]:
        """Main execution method for Optimization Advisor Agent"""
        print("\n" + "="*70)
        print("🤖 AGENT 3: OPTIMIZATION ADVISOR")
        print("="*70)

        report = self.generate_report(url, page_audit, serp_analysis)

        if report:
            print("\n✅ Comprehensive SEO report ready!")

        return report


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class SEOAuditOrchestrator:
    """
    Main orchestrator that runs all 3 agents sequentially
    and manages the overall workflow.
    """

    def __init__(self):
        print("\n" + "="*70)
        print("🚀 AI SEO AUDIT AGENT")
        print("="*70)
        print("\nInitializing system...")

        # Validate API keys
        if not validate_api_keys():
            raise ValueError("Missing required API keys")

        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.gemini_model = genai.GenerativeModel(Config.GEMINI_MODEL)

        # Initialize agents
        self.page_auditor = PageAuditorAgent(self.gemini_model)
        self.serp_analyst = SerpAnalystAgent(self.gemini_model)
        self.optimization_advisor = OptimizationAdvisorAgent(self.gemini_model)

        print("\n✅ All systems initialized successfully!")

    def run_audit(self, url: str) -> bool:
        """
        Execute the complete 3-agent SEO audit pipeline
        """
        url = clean_url(url)

        print(f"\n{'='*70}")
        print(f"🎯 Starting SEO audit for: {url}")
        print(f"{'='*70}")

        try:
            # Agent 1: Page Audit
            page_audit = self.page_auditor.run(url)
            if not page_audit:
                print("\n❌ Page audit failed. Aborting.")
                return False

            # Agent 2: SERP Analysis
            serp_analysis = self.serp_analyst.run(page_audit)
            if not serp_analysis:
                print("\n❌ SERP analysis failed. Aborting.")
                return False

            # Agent 3: Generate Report
            report = self.optimization_advisor.run(url, page_audit, serp_analysis)
            if not report:
                print("\n❌ Report generation failed. Aborting.")
                return False

            # Save report
            filepath = save_report(report, url)

            print("\n" + "="*70)
            print("✅ SEO AUDIT COMPLETE!")
            print("="*70)
            print(f"\n📄 Report saved to: {filepath}")
            print("\n" + "="*70)

            return True

        except Exception as e:
            print(f"\n❌ Error during audit: {e}")
            return False


# ============================================================================
# ENTRY POINT
# ============================================================================

def main():
    """Main entry point for the SEO audit agent"""
    try:
        # Create reports directory if it doesn't exist
        os.makedirs(Config.REPORTS_DIR, exist_ok=True)

        # Initialize orchestrator
        orchestrator = SEOAuditOrchestrator()

        # Get URL from user
        print("\n" + "="*70)
        url = input("Enter the URL to audit: ").strip()

        if not url:
            print("❌ No URL provided. Exiting.")
            return

        # Run the audit
        success = orchestrator.run_audit(url)

        if success:
            print("\n🎉 Thank you for using AI SEO Audit Agent!")
        else:
            print("\n⚠️  Audit completed with errors. Please check the output above.")

    except KeyboardInterrupt:
        print("\n\n⚠️  Audit cancelled by user.")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")


if __name__ == "__main__":
    main()
