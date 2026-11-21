import json
from pathlib import Path
from typing import Dict, List

from application.request_service import RequestRepository
from domain.service_request import ServiceRequest


class FileRepository(RequestRepository):
    """Persists service requests in a JSON file."""

    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    def load(self) -> List[ServiceRequest]:
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    return []
                raw_requests = json.loads(content)
        except json.JSONDecodeError as error:
            raise RuntimeError(
                f"Could not read request data: invalid JSON in {self.file_path}"
            ) from error
        except OSError as error:
            raise RuntimeError(
                f"Could not read request data from {self.file_path}"
            ) from error

        if not isinstance(raw_requests, list):
            raise RuntimeError(
                f"Could not read request data: expected a JSON list in {self.file_path}"
            )

        return [
            ServiceRequest.from_dict(data)
            for data in raw_requests
            if isinstance(data, dict)
        ]

    def save(self, requests: List[ServiceRequest]) -> None:
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = self.file_path.with_suffix(".tmp")
        data: List[Dict[str, str]] = [
            request.to_dict() for request in requests
        ]

        try:
            with temporary_path.open("w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
            temporary_path.replace(self.file_path)
        except OSError as error:
            raise RuntimeError(
                f"Could not save request data to {self.file_path}"
            ) from error
