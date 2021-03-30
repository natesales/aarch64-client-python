import requests

from .exceptions import ApiException


class Aaarch64Client:
    """Client for the aarch64.com API"""
    api_key: str = ""
    server: str = "https://console.aarch64.com/api"

    def __init__(self, api_key: str):
        self.api_key = api_key

    def _req(self, method: str, endpoint, body: dict = None) -> requests.Response:
        resp = requests.request(method, self.server + endpoint, json=body, headers={"Authorization": self.api_key})
        if not resp.status_code == 200:
            raise ApiException(f"API returned HTTP {resp.status_code}")

        if not resp.json()["meta"]["success"]:
            raise ApiException(resp.json()["meta"]["message"])

        return resp

    def projects(self):
        """Get list of projects"""
        return self._req("GET", "/projects")

    def add_user(self, project_id: str, email: str):
        """Add a user to a project"""
        return self._req("POST", "/project/adduser", {"project": project_id, "email": email})

    def create_vm(self, hostname: str, pop: str, project_id: str, plan: str, os: str):
        """Create a new VM"""
        return self._req("POST", "/vms/create", {
            "hostname": hostname,
            "pop": pop,
            "project": project_id,
            "plan": plan,
            "os": os
        })

    def delete_vm(self, vm: str):
        """Delete a VM"""
        return self._req("DELETE", "/vms/delete", {"vm": vm})

    def get_system(self):
        """Get system information"""
        return self._req("GET", "/system")
