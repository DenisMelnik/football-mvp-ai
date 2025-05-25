# Demo Directory

This directory contains demonstration files for the Football MVP Selector Agent.

## 📁 Contents

- **`demo.py`** - Python script that runs a complete demo with Real Madrid vs Barcelona (2023-10-28)
- **`run_demo.sh`** - Automated bash script that sets up environment and runs the demo
- **`README.md`** - This file

## 🚀 Quick Demo

### Automated Demo (Recommended)
From the project root directory, run:
```bash
./demo/run_demo.sh
```

This script will:
- ✅ Validate environment setup
- ✅ Check dependencies and API keys
- ✅ Run the complete demo automatically
- ✅ Show colorful, easy-to-follow output

### Manual Demo
From the project root directory, run:
```bash
python demo/demo.py
```

## 🔧 What the Demo Shows

1. **Match Validation** - Verifies the Real Madrid vs Barcelona match exists
2. **Data Fetching** - Retrieves comprehensive player statistics 
3. **MVP Analysis** - Uses Gemini 1.5 Flash to analyze and determine the MVP
4. **Tool Workflow** - Demonstrates the complete LangGraph ReAct agent process

## 🎯 Expected Output

The demo will show:
- 🏆 **MVP Result**: Jude Bellingham with detailed analysis
- 📊 **Statistics**: Player performance data and filtering
- 🔧 **Tool Usage**: validate_match → fetch_match_stats → determine_mvp
- 💰 **Cost**: $0.00 (100% FREE with Gemini 1.5 Flash)

## 🛠️ Customizing the Demo

To test different matches, edit `demo.py` and change the query:

```python
query = """Find the MVP for the football match between [TEAM1] and [TEAM2] on [YYYY-MM-DD]."""
```

## 📋 Requirements

- All dependencies from `../requirements.txt`
- Environment variables in `../.env`:
  - `GOOGLE_API_KEY` (FREE Google AI key)
  - `RAPID_API_KEY` (RapidAPI key)
  - `RAPID_API_HOST` (api-football-v1.p.rapidapi.com)

## 🔙 Back to Main Project

See the main [README.md](../README.md) for full installation and usage instructions. 