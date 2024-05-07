import json
import os
from typing import Dict, List

from src.application.session_management import SessionManagement
from src.config import DEFAULT_PROFILE_NAME, DEFAULT_SESSION_ID


class SetupManagement:
    def __init__(
        self,
        profile_path: str,
        session_directory: str,
        session_manager: SessionManagement,
    ):
        self.profile_path = profile_path
        self.session_directory = session_directory
        self.session_manager = session_manager
        self.profiles = self.load_profiles()
        self.sessions = self.load_sessions()

    def load_profiles(self) -> List[Dict]:
        profiles = []
        for file_name in os.listdir('./src/profiles'):
            if file_name.endswith(".json"):
                file_path = os.path.join('./src/profiles', file_name)
                with open(file_path, "r") as file:
                    profile = json.load(file)
                    profiles.append(profile)
        return profiles

    def load_sessions(self) -> List[str]:
        return [f for f in os.listdir(self.session_directory) if f.endswith(".json")]

    def list_profiles(self):
        print("Available Co-Driver Profiles:")
        for i, profile in enumerate(self.profiles, 1):
            print(f"{i}. {profile['static_profile']['name']}")

    def list_sessions(self):
        print("\nExisting Sessions:")
        for i, session_file in enumerate(self.sessions, 1):
            print(f"{i}. Session ID: {session_file.replace('.json', '')}")
        print(f"{len(self.sessions) + 1}. [New Session]")

    def select_profile(self) -> Dict:
        self.list_profiles()
        choice = int(input("Select a profile number: ")) - 1
        return self.profiles[choice]

    def select_session(self) -> str:
        self.list_sessions()
        choice = int(input("Enter your choice: "))
        if choice == len(self.sessions) + 1:
            return "new"
        else:
            return self.sessions[choice - 1]


    def setup_initial_session(self):
        has_session = False
        has_profile = False

        if DEFAULT_SESSION_ID in self.sessions and DEFAULT_SESSION_ID != "new":
            self.session_manager.set_current_session(DEFAULT_SESSION_ID)
            has_session = True
            print(f"Loaded session: {DEFAULT_SESSION_ID}")
            return
        else:
            if DEFAULT_SESSION_ID not in self.sessions and DEFAULT_SESSION_ID != "new":
                print(
                    "No existing default session found. Abort, check DEFAULT_SESSION_ID in config.py"
                )
                return

        if DEFAULT_SESSION_ID == "new":
            new_session = self.session_manager.create_session()
            has_session = True
            print("Created new session")

            if DEFAULT_PROFILE_NAME:
                profile = next((x for x in self.profiles if x["static_profile"]["name"] == DEFAULT_PROFILE_NAME), None)

                if profile is None:
                    print(
                        f"No profile found with the name {DEFAULT_PROFILE_NAME}. Abort, check DEFAULT_PROFILE_NAME in config.py"
                    )
                    return

                print(f"Loaded profile: {profile['static_profile']['name']}")
                has_profile = True

                self.session_manager.load_co_driver_profile(
                    new_session.session_id, profile
                )
            else:
                print("No default profile found.")
                return

        if has_session and has_profile:
            print("Session and profile loaded")
            return

        session_choice = self.select_session()

        if session_choice == "new":
            selected_profile = self.select_profile()
            new_session = self.session_manager.create_session()
            self.session_manager.load_co_driver_profile(
                new_session.session_id, selected_profile
            )
            self.session_manager.set_current_session(new_session.session_id)
            print(
                f"Created new session with {selected_profile['static_profile']['name']}"
            )
        else:
            # Load existing session
            session_id = session_choice.replace(".json", "")
            self.session_manager.set_current_session(session_id)
            print(f"Loaded session: {session_id}")
