import re
from typing import Tuple, Optional

def parse_user_input(input_text: str) -> Optional[Tuple[str, str, str]]:
    """
    Parse user input to extract team names and date
    
    Expected format: "Team1 vs Team2 on YYYY-MM-DD"
    
    Args:
        input_text: User input string
        
    Returns:
        Tuple of (team1, team2, date) if valid, None if invalid
    """
    # Clean input (remove extra spaces)
    input_text = input_text.strip()
    
    if not input_text:
        return None
    
    # Match the pattern: "Team1 vs Team2 on YYYY-MM-DD"
    # Using .+? (one or more) instead of .*? (zero or more) to require non-empty teams
    pattern = r"(.+?)\s+(?:vs|VS|v|V)\s+(.+?)\s+(?:on|ON)\s+(\d{4}-\d{2}-\d{2})"
    match = re.match(pattern, input_text)
    
    if not match:
        return None
    
    team1 = match.group(1).strip()
    team2 = match.group(2).strip()
    date = match.group(3).strip()
    
    return team1, team2, date 