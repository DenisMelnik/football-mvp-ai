# Football MVP Selector Agent

An AI-powered agent built with **LangGraph** and **Google Gemini 1.5 Flash** that determines the Most Valuable Player (MVP) of a football match using comprehensive player statistics and advanced AI reasoning.

## 🌟 Features

- **🚀 Google Gemini 1.5 Flash**: FREE model with 1M context window
- **⚡ LangGraph ReAct Agent**: Uses proper tool calling instead of manual text parsing
- **🔍 Match Validation**: Automatically verifies match existence using real-time API data
- **📊 Advanced Analytics**: Fetches and analyzes comprehensive player statistics
- **🏆 Intelligent MVP Selection**: AI-powered analysis considering goals, assists, ratings, and more
- **🆓 100% FREE AI**: No paid API costs for the AI model
- **🛡️ Smart Filtering**: Automatically filters out players with minimal playing time
- **📈 Large Context Processing**: Handles massive datasets with 1M token context window

## 🏗️ Architecture

### LangGraph ReAct Agent
```
User Query → LangGraph Agent → Tool Selection → API Calls → Gemini Analysis → MVP Result
```

### Available Tools
1. **`validate_match`** - Checks if a match exists between two teams on a specific date
2. **`fetch_match_stats`** - Retrieves detailed player statistics from API-Football
3. **`determine_mvp`** - Analyzes player data and determines the MVP using Gemini AI

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Google AI API key (FREE - get it at [Google AI Studio](https://makersuite.google.com/app/apikey))
- RapidAPI key with API-Football access

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd football-mvp-ai
```

2. **Create and activate virtual environment:**
```bash
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
Copy `env.template` to `.env` and fill in your API keys:
```bash
cp env.template .env
```

Edit `.env` with your API keys:
```env
# Google API key for Gemini (FREE model with 1M context window)
GOOGLE_API_KEY=your_google_api_key_here

# RapidAPI credentials (required for football data)
RAPID_API_KEY=your_rapid_api_key_here
RAPID_API_HOST=api-football-v1.p.rapidapi.com
```

### Usage

**Run the application:**
```bash
python main.py
```

**Enter match details:**
```
Enter match details: Barcelona vs Real Madrid on 2023-10-28
```

## 🎬 Demo

### Automated Demo
Run a complete demonstration with a pre-configured example:

```bash
./demo/run_demo.sh
```

The script will:
- ✅ Check environment setup (virtual environment, dependencies, API keys)
- 🚀 Run a demo with Real Madrid vs Barcelona (2023-10-28)
- 🏆 Show the complete MVP analysis process
- 📊 Display tool usage and results


## 🔧 Technical Implementation

### LangGraph ReAct Agent
- **Framework**: LangGraph's `create_react_agent`
- **Pattern**: ReAct (Reasoning + Acting) for iterative problem-solving
- **Tool Calling**: Native function calling instead of text parsing
- **State Management**: Automatic conversation history tracking

### Key Components

**1. Model Selection (`main.py`)**
```python
# Uses Google Gemini 1.5 Flash (FREE)
llm = create_llm()
agent_executor = create_react_agent(llm, tools)
```

**2. Tool Implementation (`tools/football_tools.py`)**
```python
@tool
def validate_match(team1: str, team2: str, date: str) -> str:
    """Validate if a match exists between two teams on a specific date."""
    # Implementation with proper error handling
```

**3. API Integration (`utils/api_client.py`)**
- Real-time data from API-Football
- Intelligent caching and error handling
- Data cleaning and optimization

## 🎯 Analysis Metrics

The MVP selection considers:
- **🥅 Goals & Assists** (highest weight)
- **⭐ Player Rating** (overall performance)
- **⚽ Passing Statistics** (accuracy, key passes)
- **🛡️ Defensive Actions** (tackles, interceptions)
- **⚔️ Duels Won** (individual battles)
- **🟨 Disciplinary Record** (cards)
- **⏱️ Minutes Played** (impact duration)

## 🆓 Why Gemini 1.5 Flash?

| Feature | Gemini 1.5 Flash | Traditional Options |
|---------|------------------|-------------------|
| **Cost** | 100% FREE | $$ per request |
| **Context** | 1M tokens | 4K-32K tokens |
| **Speed** | Fast | Varies |
| **Capability** | Handles massive datasets | Limited by context |

## 🛠️ Dependencies

- **LangGraph**: ReAct agent framework
- **LangChain**: Tool integration and model abstraction
- **Google GenAI**: Gemini 1.5 Flash model access
- **API-Football**: Real-time football data

## 📈 Performance Features

- **Smart Filtering**: Excludes players with <5 minutes playtime
- **Large Context**: Processes comprehensive match data without truncation
- **Error Handling**: Graceful degradation for API issues
- **Efficient Processing**: Optimized data flow for complex analysis

## 🔮 Future Enhancements

- Multi-match comparison
- Historical MVP tracking
- Custom scoring weights
- Team performance analysis
- Match prediction capabilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for improvements.

## 📄 License

This project is licensed under the MIT License.