#!/usr/bin/env python3
"""
Football MVP Selector Agent - Demo Script

This script demonstrates the LangGraph implementation with Gemini 1.5 Flash.
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Add parent directory to path to import from utils and tools
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from utils.api_client import APIFootballClient
from tools.football_tools import create_football_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

def run_demo():
    """Run a demonstration of the Football MVP Selector Agent"""
    load_dotenv()
    
    print("🚀 Football MVP Selector Agent - LangGraph + Gemini Demo")
    print("🆓 Using FREE Google Gemini 1.5 Flash with 1M context window")
    print("=" * 60)
    
    # Initialize API client
    api_client = APIFootballClient(
        os.getenv("RAPID_API_KEY"), 
        os.getenv("RAPID_API_HOST")
    )
    
    # Use Gemini 1.5 Flash
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # Create tools and agent
    tools = create_football_tools(api_client, llm)
    agent_executor = create_react_agent(llm, tools)
    
    print("✅ Agent initialized with LangGraph and Gemini 1.5 Flash")
    print("🔧 Available tools:", [tool.name for tool in tools])
    
    # Demo query
    query = """Find the MVP for the football match between Real Madrid and Barcelona on 2023-10-28.
    
    Please follow these steps:
    1. Validate if this match exists using the validate_match tool
    2. Fetch the player statistics using fetch_match_stats tool
    3. Analyze the statistics and determine the MVP using determine_mvp tool
    
    Provide a detailed analysis of why the chosen player deserves to be the MVP."""
    
    print(f"\n📝 Demo Query:")
    print(f"   Real Madrid vs Barcelona on 2023-10-28")
    print(f"\n🤖 Gemini agent thinking and using tools...")
    print("-" * 50)
    
    # Run the agent
    result = agent_executor.invoke({"messages": [HumanMessage(content=query)]})
    
    # Extract the final message
    final_message = result["messages"][-1]
    
    print(f"\n🏆 Final Result:")
    print(f"{final_message.content}")
    
    print(f"\n✨ Demo completed successfully!")
    print(f"📊 Tools used: validate_match → fetch_match_stats → determine_mvp")
    print(f"🆓 Cost: $0.00 (Gemini 1.5 Flash is FREE)")

if __name__ == "__main__":
    run_demo() 