from langchain_core.tools import tool

def create_football_tools(api_client, llm=None):
    """Create and return the tools for the football MVP agent"""
    
    @tool
    def validate_match(team1: str, team2: str, date: str) -> str:
        """
        Validate if a match between two teams on a specific date exists.
        Returns fixture information if match exists, otherwise returns error message.
        
        Args:
            team1: First team name
            team2: Second team name  
            date: Match date in YYYY-MM-DD format
        """
        try:
            fixture = api_client.find_fixture(team1, team2, date)
            
            if fixture:
                result = {
                    "exists": True,
                    "fixture_id": fixture["fixture"]["id"],
                    "home_team": fixture["teams"]["home"]["name"],
                    "away_team": fixture["teams"]["away"]["name"],
                    "date": fixture["fixture"]["date"]
                }
                return f"Match found! Fixture ID: {result['fixture_id']}, {result['home_team']} vs {result['away_team']} on {result['date']}"
            else:
                return f"No match found between {team1} and {team2} on {date}. Please check team names and date."
        except Exception as e:
            return f"Error validating match: {str(e)}"
    
    @tool
    def fetch_match_stats(fixture_id: int) -> str:
        """
        Fetch player statistics for a specific fixture by fixture_id.
        Returns a summary of the match stats.
        
        Args:
            fixture_id: Fixture ID from API-Football
        """
        try:
            stats = api_client.get_player_stats(fixture_id)
            
            if not stats:
                return f"Error: No player statistics found for fixture {fixture_id}"
            
            # Return a summary instead of full data to avoid JSON parsing issues
            total_players = sum(len(team.get("players", [])) for team in stats)
            teams = [team["team"]["name"] for team in stats]
            
            return f"✅ Successfully fetched statistics for {len(stats)} teams ({', '.join(teams)}) with {total_players} total players. Ready for MVP analysis."
        except Exception as e:
            return f"Error fetching match stats: {str(e)}"
    
    @tool  
    def determine_mvp(fixture_id: int) -> str:
        """
        Analyze player statistics and determine the MVP of the match.
        Call this function with the fixture_id after fetching match stats.
        
        Args:
            fixture_id: The fixture ID to analyze for MVP
        """
        
        def _create_player_summary(stats_data):
            """Create a concise text summary of player statistics"""
            summary = ""
            
            for team in stats_data:
                team_name = team["team"]["name"]
                summary += f"\n=== {team_name} ===\n"
                
                for player in team.get("players", []):
                    player_info = player["player"]
                    stats = player["statistics"][0] if player.get("statistics") else {}
                    
                    # Extract stats with intelligent null handling
                    games = stats.get("games", {})
                    goals_stats = stats.get("goals", {})
                    passes_stats = stats.get("passes", {})
                    tackles_stats = stats.get("tackles", {})
                    duels_stats = stats.get("duels", {})
                    shots_stats = stats.get("shots", {})
                    cards_stats = stats.get("cards", {})
                    
                    # Core stats with meaningful defaults
                    minutes = games.get("minutes") or 0
                    position = games.get("position") or "Unknown"
                    rating = games.get("rating") or "N/A"
                    
                    # Performance stats (null = 0 for counting stats)
                    goals = goals_stats.get("total") or 0
                    assists = goals_stats.get("assists") or 0
                    saves = goals_stats.get("saves") or 0
                    
                    # Shooting stats
                    shots_total = shots_stats.get("total") or 0
                    shots_on_target = shots_stats.get("on") or 0
                    
                    # Passing stats
                    passes_total = passes_stats.get("total") or 0
                    passes_accuracy = passes_stats.get("accuracy")
                    key_passes = passes_stats.get("key") or 0
                    
                    # Defensive stats
                    tackles_total = tackles_stats.get("total") or 0
                    interceptions = tackles_stats.get("interceptions") or 0
                    
                    # Duels
                    duels_total = duels_stats.get("total") or 0
                    duels_won = duels_stats.get("won") or 0
                    
                    # Disciplinary
                    yellow_cards = cards_stats.get("yellow") or 0
                    red_cards = cards_stats.get("red") or 0
                    
                    # Basic player info
                    summary += f"• {player_info['name']} ({position}) - {minutes}min"
                    
                    # Only show rating if available
                    if rating != "N/A":
                        summary += f", Rating: {rating}"
                    
                    # Show key performance indicators
                    if goals > 0:
                        summary += f", Goals: {goals}"
                    if assists > 0:
                        summary += f", Assists: {assists}"
                    if saves > 0:
                        summary += f", Saves: {saves}"
                    
                    summary += "\n"
                    
                    # Detailed stats (only show if meaningful data exists)
                    if shots_total > 0 or passes_total > 0:
                        summary += f"  📊 Attack: {shots_total} shots ({shots_on_target} on target), {passes_total} passes"
                        if passes_accuracy is not None:
                            summary += f" ({passes_accuracy}% acc)"
                        if key_passes > 0:
                            summary += f", {key_passes} key passes"
                        summary += "\n"
                    
                    if tackles_total > 0 or interceptions > 0 or duels_total > 0:
                        summary += f"  🛡️ Defense: {tackles_total} tackles, {interceptions} interceptions"
                        if duels_total > 0:
                            summary += f", {duels_won}/{duels_total} duels won"
                        summary += "\n"
                    
                    if yellow_cards > 0 or red_cards > 0:
                        summary += f"  🟨 Cards: {yellow_cards} yellow, {red_cards} red\n"
                    
                    summary += "\n"
            
            return summary
        
        try:
            # Get the player stats directly
            stats_data = api_client.get_player_stats(fixture_id)
            
            if not stats_data:
                return f"No player statistics found for fixture {fixture_id}"
            
            # Filter out players who didn't play meaningful minutes
            filtered_stats = []
            total_players = 0
            filtered_players = 0
            
            for team in stats_data:
                team_copy = team.copy()
                filtered_players_list = []
                
                for player in team.get("players", []):
                    total_players += 1
                    
                    # Check if player played meaningful minutes
                    played_minutes = 0
                    if player.get("statistics") and len(player["statistics"]) > 0:
                        minutes = player["statistics"][0].get("games", {}).get("minutes")
                        if minutes is not None and minutes > 0:
                            played_minutes = minutes
                    
                    # Only include players who played more than 5 minutes
                    if played_minutes > 5:
                        filtered_players_list.append(player)
                        filtered_players += 1
                
                team_copy["players"] = filtered_players_list
                filtered_stats.append(team_copy)
            
            
            # Create a concise summary for the LLM instead of full JSON
            summary = _create_player_summary(filtered_stats)
            
            # Create a prompt for the LLM to determine the MVP
            prompt = f"""
            Based on the following player statistics summary from a football match, determine who was the Most Valuable Player (MVP) and explain why.
            
            Note: Only players who played more than 5 minutes are included in this analysis.
            
            {summary}
            
            Analyze key metrics such as:
            - Goals and assists (most important)
            - Overall rating
            - Passing accuracy and key passes  
            - Defensive actions (tackles, interceptions, blocks)
            - Goalkeeper saves (if applicable)
            - Minutes played and impact on the game
            
            Choose ONE player as MVP and provide a detailed explanation focusing on their most impactful contributions.
            Format your response as: "MVP: [Player Name] - [Detailed explanation of why they deserve MVP]"
            """
            
            # Use Gemini 1.5 Flash to determine MVP
            response = llm.invoke(prompt)
            response_text = response.content
            
            return f"{response_text}\n\n📊 Analysis based on {filtered_players} players (filtered out {total_players - filtered_players} who played ≤5 minutes)"
                
        except Exception as e:
            return f"Error analyzing MVP: {str(e)}"
    
    # Return list of tools
    tools = [validate_match, fetch_match_stats, determine_mvp]
    
    return tools 