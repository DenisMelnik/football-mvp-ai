#!/usr/bin/env python3
"""
Football MVP Selector Agent

This application uses AI to analyze football match statistics and determine the Most Valuable Player (MVP)
based on comprehensive performance metrics including goals, assists, ratings, and other key statistics.
"""

import os
from dotenv import load_dotenv
import logging

# Configure logging at INFO level
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

from utils.input_parser import parse_user_input
from utils.api_client import APIFootballClient
from tools.football_tools import create_football_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage

def create_llm():
    """Create Gemini LLM instance"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key or google_api_key == "your_google_api_key_here":
        raise ValueError("GOOGLE_API_KEY not found in environment variables or is placeholder")
    
    logger.info("🚀 Using Google Gemini 1.5 Flash (1M context window, FREE)")
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        google_api_key=google_api_key
    )

def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    rapid_api_key = os.getenv("RAPID_API_KEY")
    rapid_api_host = os.getenv("RAPID_API_HOST")
    
    if not rapid_api_key or not rapid_api_host:
        logger.error("RAPID_API_KEY and RAPID_API_HOST not found in environment variables")
        return
    
    print("🤖 Football MVP Selector Agent - Powered by Google Gemini 1.5 Flash")
    print("🆓 FREE model with 1M context window for handling large datasets")
    
    # Initialize API client
    api_client = APIFootballClient(rapid_api_key, rapid_api_host)
    
    # Initialize Gemini LLM
    try:
        llm = create_llm()
    except ValueError as e:
        logger.error(str(e))
        return
    
    # Create tools
    tools = create_football_tools(api_client, llm)
    
    # Create LangGraph ReAct agent
    agent_executor = create_react_agent(llm, tools)
    
    logger.info("⚽ Football MVP Selector Agent initialized successfully!")
    logger.info("💡 Enter match details in format: 'Team1 vs Team2 on YYYY-MM-DD'")
    logger.info("📊 Example: 'Barcelona vs Real Madrid on 2024-03-17'")
    
    # Main interaction loop
    while True:
        try:
            user_input = input("\nEnter match details (or 'exit' to quit): ").strip()
            
            if user_input.lower() in ['exit', 'quit', 'q']:
                logger.info("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Parse and validate input
            parsed_input = parse_user_input(user_input)
            if not parsed_input:
                print("❌ Invalid format. Please use: 'Team1 vs Team2 on YYYY-MM-DD'")
                continue
            
            team1, team2, date = parsed_input
            
            # Create the query for the agent
            query = f"""
            Find the MVP for the football match between {team1} and {team2} on {date}. 
            
            Please follow these steps:
            1. First, validate if this match exists using the validate_match tool
            2. If the match exists, fetch the player statistics using fetch_match_stats tool
            3. Finally, analyze the statistics and determine the MVP using determine_mvp tool
            
            Provide a detailed analysis of why the chosen player deserves to be the MVP.
            """.strip()
            
            # Run the agent
            result = agent_executor.invoke({"messages": [HumanMessage(content=query)]})
            
            # Extract the final message from the agent
            final_message = result["messages"][-1]
            print(f"\n🏆 Result:\n{final_message.content}")
            
        except KeyboardInterrupt:
            logger.info("\n👋 Goodbye!")
            break
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            print("❌ An error occurred. Please try again.")

if __name__ == "__main__":
    main() 