# 🚀 AI SEO Audit Agent

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

**A powerful, automated 3-agent system that analyzes websites and generates comprehensive SEO optimization reports using Google's Gemini AI.**

[Features](#-features) • [Quick Start](#-quick-start) • [Demo](#-how-it-works) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 What This Does

Transform any website URL into a professional SEO audit report in under 2 minutes! This AI agent automatically:

- 🔍 **Scrapes & analyzes** webpage structure and content
- 🎯 **Identifies** target keywords and search intent
- 🔎 **Researches** Google search results for competitive analysis
- 📊 **Analyzes** top 10 competitors on Google
- 📝 **Generates** a comprehensive, prioritized SEO report

**No manual work. No complex setup. Just results.**

---

## ✨ Features

### 🤖 3-Agent Architecture

1. **Page Auditor Agent**
   - Scrapes webpages using Jina AI Reader (reliable, no auth required)
   - Analyzes title tags, meta descriptions, headings, content
   - Identifies target keywords and search intent
   - Detects technical SEO issues

2. **SERP Analyst Agent**
   - Fetches live Google search results via SerpAPI
   - Analyzes top 10 ranking competitors
   - Identifies content patterns and opportunities
   - Finds competitive gaps

3. **Optimization Advisor Agent**
   - Combines insights from both previous agents
   - Generates professional Markdown reports
   - Prioritizes recommendations (P0/P1/P2)
   - Provides implementation roadmap

### 🌟 Why This Solution?

| Feature | This Agent | Original Tutorial |
|---------|------------|-------------------|
| **Reliability** | ✅ REST APIs (no MCP issues) | ❌ Firecrawl MCP (known issues) |
| **Setup** | ✅ Simple Python script | ❌ Complex Google ADK |
| **Cost** | ✅ 100% Free tier available | ⚠️ Limited free options |
| **Complexity** | ✅ ~200 lines, readable | ❌ Multiple frameworks |
| **Maintenance** | ✅ Easy to debug | ❌ Framework dependencies |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Internet connection
- 10 minutes for setup

### 1. Get Free API Keys

#### Gemini API Key (Google)
1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Click "Create API Key"
3. Copy your key (starts with `AIza...`)

#### SerpAPI Key
1. Visit [SerpAPI](https://serpapi.com)
2. Sign up for free account (no credit card required)
3. Copy your API key from dashboard
4. **Free tier includes 100 searches/month**

**Note:** Jina AI Reader requires NO API key - completely free!

### 2. Clone & Install

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-seo-audit-agent.git
cd ai-seo-audit-agent

# Run automated setup
chmod +x setup.sh
./setup.sh

# Or install manually
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API keys
# Use any text editor: nano, vim, VS Code, etc.
nano .env
```

Your `.env` file should look like:
```env
GEMINI_API_KEY=AIzaXXXXXXXXXXXXXXXXXXXX
SERPAPI_KEY=your_serpapi_key_here
```

### 4. Run Your First Audit

```bash
python seo_agent.py
```

When prompted, enter a URL:
```
Enter the URL to audit: https://example.com
```

Your report will be saved to `reports/` folder!

---

## 📖 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  User Input: https://example.com                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT 1: PAGE AUDITOR                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Scrape with Jina AI Reader                         │  │
│  │ • Extract: title, meta, headings, content            │  │
│  │ • Analyze: keywords, word count, structure           │  │
│  │ • Identify: technical issues, opportunities          │  │
│  └──────────────────────────────────────────────────────┘  │
│  Output: Page audit data + primary keyword                  │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT 2: SERP ANALYST                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Search Google via SerpAPI (primary keyword)        │  │
│  │ • Fetch top 10 organic results                       │  │
│  │ • Analyze: titles, content types, patterns           │  │
│  │ • Identify: opportunities, gaps, strategies          │  │
│  └──────────────────────────────────────────────────────┘  │
│  Output: SERP analysis + competitor insights                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  🤖 AGENT 3: OPTIMIZATION ADVISOR                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ • Combine insights from Agent 1 & 2                  │  │
│  │ • Generate professional SEO report                   │  │
│  │ • Prioritize recommendations (P0/P1/P2)              │  │
│  │ • Create implementation roadmap                      │  │
│  └──────────────────────────────────────────────────────┘  │
│  Output: Comprehensive Markdown report                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  📄 Saved Report: reports/seo_report_example.com_xxx.md     │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Example Output

The agent generates a comprehensive report including:

### Report Sections

1. **Executive Summary**
   - Overall SEO health assessment
   - Key opportunities identified
   - Expected impact overview

2. **Technical & On-Page Analysis**
   - Title tag analysis (with character count)
   - Meta description review
   - Heading structure (H1, H2, H3)
   - Content length and quality
   - Technical SEO issues

3. **Keyword Analysis**
   - Primary and secondary keywords
   - Search intent matching
   - Keyword optimization opportunities

4. **Competitive SERP Analysis**
   - SERP landscape overview
   - Competitor content patterns
   - Content gaps and opportunities
   - Differentiation strategies

5. **Prioritized Recommendations**
   - 🔴 **P0 - Critical** (fix immediately)
   - 🟡 **P1 - High Priority** (fix this week)
   - 🟢 **P2 - Medium Priority** (fix this month)

6. **Implementation Roadmap**
   - Week-by-week action plan
   - Expected timelines
   - Resource requirements

7. **Expected Impact**
   - Quick wins (1-4 weeks)
   - Medium-term goals (1-3 months)
   - Long-term objectives (3-6 months)

### Sample Report

```markdown
# SEO Audit Report

**Website:** https://example.com
**Date:** January 12, 2025
**Primary Keyword:** example domain

---

## Executive Summary

The website has a solid foundation but shows opportunities for
improvement in content depth and technical optimization...

---

## 🔴 P0 - Critical Issues

1. **Missing meta description** - Add a compelling 150-160 character
   meta description to improve CTR in search results...

[Full report continues...]
```

---

## 💰 Cost Breakdown

All services offer generous free tiers:

| Service | Free Tier | What It Does | Cost After Free |
|---------|-----------|--------------|-----------------|
| **Jina AI Reader** | ∞ Unlimited | Web scraping | Always free |
| **Gemini API** | 15 req/min | AI analysis | $0.00015/1K chars |
| **SerpAPI** | 100 searches/month | Google results | $50/month for 5K |

**For 5-20 websites/month:** You'll stay within all free tiers!

---

## 🛠️ Configuration

### Change AI Model

Edit `seo_agent.py` line 38:

```python
GEMINI_MODEL = "gemini-2.5-flash"  # Fast and latest
# or
GEMINI_MODEL = "gemini-1.5-pro"    # More powerful, slower
```

### Adjust SERP Results

Edit `seo_agent.py` line 306:

```python
"num": 10,  # Change to 20 for more competitor data
```

### Customize Report Structure

Edit the prompt in `OptimizationAdvisorAgent.generate_report()` method (line 373+) to customize the report format and content.

---

## 📁 Project Structure

```
ai-seo-audit-agent/
├── seo_agent.py          # Main agent script (run this)
├── requirements.txt      # Python dependencies
├── .env.example         # Template for API keys
├── .env                 # Your actual API keys (not in git)
├── .gitignore           # Files to exclude from git
├── README.md            # This file
├── QUICKSTART.md        # Quick start guide
├── LICENSE              # MIT License
├── setup.sh             # Auto-installer (Mac/Linux)
├── setup.bat            # Auto-installer (Windows)
└── reports/             # Generated SEO reports
    └── *.md             # Individual audit reports
```

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'google.generativeai'"

**Solution:**
```bash
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

### "Missing API keys" error

**Solution:**
1. Ensure `.env` file exists (not `.env.example`)
2. Verify API keys are correct (no quotes, no spaces)
3. Check the file is in the same directory as `seo_agent.py`

### "Error scraping page"

**Possible causes:**
- Invalid URL or website is down
- Internet connection issue
- Website blocks automated access

**Solution:**
- Verify the URL is correct and accessible
- Try a different website
- Check your internet connection

### "Rate limit exceeded" (Gemini)

**Solution:**
- Wait 1-2 minutes between requests
- Switch to a different model: `gemini-1.5-flash`
- Consider upgrading to paid tier for higher limits

### "Rate limit exceeded" (SerpAPI)

**Solution:**
- You've used 100 free monthly searches
- Wait until next month for reset
- Upgrade to paid tier if needed

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

### Ways to Contribute

1. 🐛 **Report bugs** - Open an issue describing the problem
2. 💡 **Suggest features** - Share your ideas for improvements
3. 📝 **Improve documentation** - Fix typos, add examples
4. 🔧 **Submit pull requests** - Fix bugs or add features

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/ai-seo-audit-agent.git
cd ai-seo-audit-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Make your changes
# Test your changes
# Submit a pull request
```

### Code Style

- Follow PEP 8 style guidelines
- Add comments for complex logic
- Update documentation for new features
- Include docstrings for functions

---

## 🗺️ Roadmap

Future enhancements planned:

- [ ] **Batch processing** - Audit multiple URLs at once
- [ ] **Parallel workflows** - Run Agent 1 & 2 simultaneously
- [ ] **Backlink analysis** - Integrate backlink checking
- [ ] **Historical tracking** - Track SEO changes over time
- [ ] **Web dashboard** - Visual interface for reports
- [ ] **Email reports** - Automatic report delivery
- [ ] **Scheduled audits** - Automatic recurring audits
- [ ] **Content scoring** - Detailed content quality metrics
- [ ] **Schema markup** - Generate schema.org JSON-LD
- [ ] **Competitor tracking** - Monitor competitor changes

Want to work on any of these? Open an issue or PR!

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

✅ Commercial use
✅ Modification
✅ Distribution
✅ Private use

---

## 🙏 Acknowledgments

Built with these amazing tools:

- **[Google Gemini AI](https://ai.google.dev/)** - AI analysis and report generation
- **[Jina AI Reader](https://jina.ai/)** - Reliable web scraping (more stable than Firecrawl MCP)
- **[SerpAPI](https://serpapi.com/)** - Google search results API

Inspired by the [AI SEO Audit Team tutorial](https://www.theunwindai.com/p/build-an-ai-seo-audit-team-with-gemini) but redesigned for reliability and simplicity.

---

## 💬 Support

Need help? Here's how to get it:

- 📖 **Documentation**: Read the [full README](README.md)
- 🐛 **Bug reports**: [Open an issue](https://github.com/YOUR_USERNAME/ai-seo-audit-agent/issues)
- 💡 **Feature requests**: [Open an issue](https://github.com/YOUR_USERNAME/ai-seo-audit-agent/issues)
- ❓ **Questions**: [Start a discussion](https://github.com/YOUR_USERNAME/ai-seo-audit-agent/discussions)

---

## ⭐ Star History

If this project helped you, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=YOUR_USERNAME/ai-seo-audit-agent&type=Date)](https://star-history.com/#YOUR_USERNAME/ai-seo-audit-agent&Date)

---

<div align="center">

**Built with ❤️ using AI**

[⬆ Back to Top](#-ai-seo-audit-agent)

</div>
