import requests
from typing import Dict, List, Optional, Any, Union
import logging
import json

# Configure logging at INFO level instead of DEBUG
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class APIFootballClient:
    """Client for interacting with the API-Football API via RapidAPI"""
    
    BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
    
    def __init__(self, api_key: str, api_host: str):
        self.api_key = api_key
        self.api_host = api_host
        self.headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": api_host,
            "Content-Type": "application/json"
        }
        logger.info(f"Initialized API client for {api_host}")
        # Log truncated API key for debugging (showing only first 10 and last 4 chars)
        if api_key:
            if len(api_key) > 14:
                truncated_key = api_key[:10] + "..." + api_key[-4:]
            else:
                truncated_key = api_key[:5] + "..."
            logger.info(f"API key provided: {truncated_key}")
        else:
            logger.warning("No API key provided!")
        
        # Log full headers (excluding sensitive data)
        safe_headers = self.headers.copy()
        if 'X-RapidAPI-Key' in safe_headers:
            safe_headers['X-RapidAPI-Key'] = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "***"
        logger.debug(f"Request headers: {safe_headers}")
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Make a request to the API-Football API
        
        Args:
            endpoint: API endpoint to call
            params: Query parameters
            
        Returns:
            API response as dictionary
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        logger.info(f"Making request to: {url}")
        logger.info(f"Request parameters: {params}")
        
        try:
            logger.debug(f"Sending GET request...")
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            
            logger.info(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {dict(response.headers)}")
            
            # Log response content for debugging
            try:
                response_json = response.json()
                logger.debug(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except ValueError:
                logger.debug(f"Response text (not JSON): {response.text}")
            
            # Check for various error status codes
            if response.status_code == 401:
                logger.error(f"Authentication error (401): Invalid API key")
                logger.error(f"Response: {response.text}")
                return {"errors": f"Authentication failed: Invalid API key (status 401)"}
                
            elif response.status_code == 403:
                logger.error(f"Forbidden error (403): Access denied or subscription issue")
                logger.error(f"Response: {response.text}")
                return {"errors": f"Access denied: {response.text} (status 403)"}
                
            elif response.status_code == 429:
                logger.error(f"Rate limit error (429): Too many requests")
                logger.error(f"Response: {response.text}")
                return {"errors": f"Rate limit exceeded (status 429)"}
                
            elif response.status_code != 200:
                logger.error(f"HTTP error {response.status_code}: {response.text}")
                return {"errors": f"HTTP {response.status_code}: {response.text}"}
            
            # Success case
            logger.info(f"Request successful!")
            return response.json()
            
        except requests.exceptions.Timeout:
            logger.error(f"Request timeout after 30 seconds")
            return {"errors": "Request timeout"}
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            return {"errors": f"Connection error: {str(e)}"}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            return {"errors": f"Request failed: {str(e)}"}
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            logger.error(f"Response text: {response.text}")
            return {"errors": f"Invalid JSON response: {str(e)}"}
    
    def find_fixture(self, team1: str, team2: str, date: str) -> Optional[Dict]:
        """
        Find a fixture between two teams on a specific date
        
        Args:
            team1: First team name
            team2: Second team name
            date: Date in YYYY-MM-DD format
            
        Returns:
            Fixture data if found, None otherwise
        """
        logger.info(f"Searching for fixture: {team1} vs {team2} on {date}")
        
        # Get fixtures for the specified date
        params = {"date": date}
        response = self._make_request("fixtures", params)
        
        # Check if we have internal errors from _make_request
        if "errors" in response and isinstance(response["errors"], str):
            logger.error(f"Failed to fetch fixtures: {response['errors']}")
            return None
        
        # Check if API-Football returned an error (errors field with non-empty array)
        if response.get("errors") and len(response["errors"]) > 0:
            logger.error(f"API-Football error: {response['errors']}")
            return None
        
        # Look for the specific match
        fixtures = response.get("response", [])
        
        for fixture in fixtures:
            if not fixture.get("teams"):
                continue
                
            home_team = fixture["teams"]["home"]["name"].lower()
            away_team = fixture["teams"]["away"]["name"].lower()
            
            # Normalize team names for comparison
            team1_lower = team1.lower()
            team2_lower = team2.lower()
            
            # Check if teams match (in any order)
            if (team1_lower in home_team and team2_lower in away_team) or (team1_lower in away_team and team2_lower in home_team):
                logger.info(f"Found matching fixture: {fixture['teams']['home']['name']} vs {fixture['teams']['away']['name']}")
                return fixture
        
        logger.warning(f"No fixture found for {team1} vs {team2} on {date}")
        return None
    
    def get_player_stats(self, fixture_id: int) -> List[Dict]:
        """
        Get player statistics for a specific fixture
        
        Args:
            fixture_id: The fixture ID from API-Football
            
        Returns:
            List of player statistics (raw data, nulls preserved for intelligent handling)
        """
        logger.info(f"Fetching player statistics for fixture ID: {fixture_id}")
        
        params = {"fixture": fixture_id}
        response = self._make_request("fixtures/players", params)
        
        # Check if we have internal errors from _make_request
        if "errors" in response and isinstance(response["errors"], str):
            logger.error(f"Failed to fetch player stats: {response['errors']}")
            return []
        
        # Check if API-Football returned an error (errors field with non-empty array)
        if response.get("errors") and len(response["errors"]) > 0:
            logger.error(f"API-Football error: {response['errors']}")
            return []
        
        # Get the player statistics
        stats = response.get("response", [])
        
        if not stats:
            logger.warning(f"No player statistics found for fixture {fixture_id}")
            return []
        
        logger.info(f"Successfully fetched player statistics for {len(stats)} teams")
        return stats 