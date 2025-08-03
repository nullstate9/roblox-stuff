import requests
import json
import time
import random
from typing import Optional, List, Dict, Any

class Client:
    def __init__(self, roblosecurity: str):
        self.roblosecurity = roblosecurity
        self.session = requests.Session()
        self.session.cookies.set(".ROBLOSECURITY", roblosecurity)
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en;q=0.9",
            "Origin": "https://www.roblox.com/",
            "Referer": "https://www.roblox.com/",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 15_6) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Safari/605.1.15"
            )
        }

    def get_online_friends(self) -> []:
        """
        Gets a list of friends for a ROBLOX account

        Args:
            roblosecurity (string): The authentication cookie

        Returns:
            data (table): List of joinable friends that are InGame, along with any other useful information.
        """

        self.session.cookies.set(".ROBLOSECURITY", self.roblosecurity)

        cookie_data = self.session.get("https://users.roblox.com/v1/users/authenticated", headers=self.headers)
        cookie_data.raise_for_status()
        cookie_data = cookie_data.json()

        user_name = cookie_data['name']
        display_name = cookie_data['displayName']
        user_id = cookie_data['id']

        friends_data = self.session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/online")
        friends_data.raise_for_status()

    def get_url_scheme(self, game_id: int, job_id: Optional[str] = None) -> str:
        """
        Generate a Roblox player launch URL.

        Args:
            game_id (int): The Roblox game ID.
            job_id (Optional[str]): Specific server/job ID. Defaults to None.

        Returns:
            str: A formatted Roblox player URL that can be used to launch a game.
        """

        # Get CSRF token
        csrf_response = self.session.post("https://auth.roblox.com/v2/signup")
        csrf_token = csrf_response.headers.get("x-csrf-token")
        self.headers["X-Csrf-Token"] = csrf_token

        # Get clientAssertion
        client_assertion_response = self.session.get(
            "https://auth.roblox.com/v1/client-assertion", headers=self.headers
        )
        client_assertion_response.raise_for_status()
        client_assertion = client_assertion_response.json()["clientAssertion"]

        # Get browserTracker ID
        tracker_response = self.session.get("https://roblox.com/home", headers=self.headers)
        tracker_response.raise_for_status()
        tracker_cookie = tracker_response.cookies.get("RBXEventTrackerV2")
        browser_tracker_id = tracker_cookie.split("browserid=")[1] if tracker_cookie else ""

        # Get authentication ticket
        auth_ticket_response = self.session.post(
            "https://auth.roblox.com/v1/authentication-ticket/",
            headers=self.headers,
            json={"clientAssertion": client_assertion}
        )
        auth_ticket_response.raise_for_status()
        auth_ticket = auth_ticket_response.headers.get("Rbx-Authentication-Ticket")

        # Get public servers
        servers_response = self.session.get(
            f"https://games.roblox.com/v1/games/{game_id}/servers/Public?cursor=&sortOrder=Desc&excludeFullGames=false"
        )
        servers_response.raise_for_status()
        servers = servers_response.json()["data"]

        # Choose a job if not provided
        if job_id is None:
            available = [s for s in servers if (s["maxPlayers"] - s["playing"]) >= 3]
            job_id = random.choice(available)["id"] if available else None

        launch_time = int(time.time())

        base_url = (
            f"roblox-player:1+launchmode:play+gameinfo:{auth_ticket}+launchtime:{launch_time}"
            f"+placelauncherurl:https%3A%2F%2Fwww.roblox.com%2FGame%2FPlaceLauncher.ashx"
        )

        if job_id is None:
            launch_url = (
                f"{base_url}%3Frequest%3DRequestGameJob%26browserTrackerId%3D{browser_tracker_id}"
                f"%26placeId%3D{game_id}%26isPlayTogetherGame%3Dfalse%26joinAttemptOrigin%3DServerListJoin"
            )
        else:
            launch_url = (
                f"{base_url}%3Frequest%3DRequestGameJob%26browserTrackerId%3D{browser_tracker_id}"
                f"%26placeId%3D{game_id}%26gameId%3D{job_id}%26isPlayTogetherGame%3Dfalse"
                f"%26joinAttemptId%3D{job_id}%26joinAttemptOrigin%3DServerListJoin"
            )

        full_url = (
            f"{launch_url}+browsertrackerid:{browser_tracker_id}"
            f"+robloxLocale:en_us+gameLocale:en_us+channel:"
        )

        return full_url
