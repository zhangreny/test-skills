#!/usr/bin/env python3
"""Minimal TestRail API client for suite/section inspection and testcase upload."""

from __future__ import annotations

from dataclasses import dataclass

import requests
from requests.auth import HTTPBasicAuth

DEFAULT_TESTRAIL_USER = "renyu.zhang@smartx.com"
DEFAULT_TESTRAIL_API_KEY = "Zhangry-2001"


@dataclass
class TestrailClient:
    base_url: str
    user: str
    api_key: str
    timeout: int = 30

    def _api_url(self, path: str) -> str:
        return f"{self.base_url.rstrip('/')}/index.php?/api/v2/{path}"

    def get(self, path: str, params: dict | None = None) -> dict | list:
        response = requests.get(
            self._api_url(path),
            auth=HTTPBasicAuth(self.user, self.api_key),
            headers={"Content-Type": "application/json"},
            params=params or {},
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise RuntimeError(f"TestRail GET failed: {response.status_code} {response.text[:300]}")
        return response.json()

    def post(self, path: str, payload: dict) -> dict:
        response = requests.post(
            self._api_url(path),
            auth=HTTPBasicAuth(self.user, self.api_key),
            headers={"Content-Type": "application/json"},
            json=payload,
            timeout=self.timeout,
        )
        if response.status_code != 200:
            raise RuntimeError(f"TestRail POST failed: {response.status_code} {response.text[:300]}")
        return response.json()

    def get_section(self, section_id: int) -> dict:
        return self.get(f"get_section/{section_id}")

    def get_suites(self, project_id: int) -> list[dict]:
        raw = self.get(f"get_suites/{project_id}")
        return raw if isinstance(raw, list) else []

    def get_sections(self, project_id: int, suite_id: int) -> list[dict]:
        raw = self.get(f"get_sections/{project_id}", {"suite_id": suite_id})
        return raw if isinstance(raw, list) else []

    def add_section(
        self,
        project_id: int,
        suite_id: int,
        name: str,
        parent_id: int = 0,
        description: str = "",
    ) -> dict:
        payload = {"name": name, "suite_id": suite_id, "description": description or ""}
        if parent_id:
            payload["parent_id"] = parent_id
        return self.post(f"add_section/{project_id}", payload)

    def add_case(
        self,
        section_id: int,
        title: str,
        steps: list[str] | None = None,
        description: str = "",
    ) -> dict:
        payload = {"title": title}
        if description:
            payload["custom_preconds"] = description
        if steps:
            payload["custom_steps_separated"] = [{"content": step, "expected": ""} for step in steps]
        return self.post(f"add_case/{section_id}", payload)


def build_section_tree(flat_sections: list[dict]) -> list[dict]:
    by_id = {
        section["id"]: {
            "id": section.get("id"),
            "name": section.get("name") or "",
            "parent_id": section.get("parent_id"),
            "children": [],
        }
        for section in flat_sections
    }
    for section in flat_sections:
        node = by_id[section["id"]]
        parent_id = section.get("parent_id")
        if parent_id is not None and parent_id in by_id:
            by_id[parent_id]["children"].append(node)
    return [by_id[section["id"]] for section in flat_sections if section.get("parent_id") is None]
