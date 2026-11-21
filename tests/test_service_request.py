import tempfile
import unittest
from pathlib import Path

from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestIdError,
    InvalidPriorityError,
    RequestAlreadyResolvedError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest
from infrastructure.file_repository import FileRepository


class SmartServiceDeskTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory()
        data_file = Path(self.temp_directory.name) / "requests.json"
        self.repository = FileRepository(data_file)
        self.service = RequestService(self.repository)

    def tearDown(self) -> None:
        self.temp_directory.cleanup()

    def test_create_and_persist_request(self) -> None:
        created = self.service.create_request(
            "sr101", "Rahul", "Laptop is not starting", "HIGH"
        )
        reloaded = RequestService(self.repository).search_request("SR101")
        self.assertEqual(created.request_id, "SR101")
        self.assertEqual(created.status, "OPEN")
        self.assertEqual(reloaded.status, "OPEN")

    def test_duplicate_request_id_is_rejected(self) -> None:
        self.service.create_request(
            "SR101", "Rahul", "Laptop issue", "HIGH"
        )
        with self.assertRaises(DuplicateRequestIdError):
            self.service.create_request(
                "SR101", "Priya", "Other issue", "LOW"
            )

    def test_invalid_priority_is_rejected(self) -> None:
        with self.assertRaises(InvalidPriorityError):
            ServiceRequest("SR101", "Rahul", "Laptop issue", "URGENT")

    def test_resolve_and_persist_request(self) -> None:
        self.service.create_request(
            "SR101", "Rahul", "Laptop issue", "HIGH"
        )
        resolved = self.service.resolve_request("SR101")
        reloaded = RequestService(self.repository).search_request("SR101")
        self.assertEqual(resolved.status, "RESOLVED")
        self.assertEqual(reloaded.status, "RESOLVED")

    def test_resolve_twice_is_rejected(self) -> None:
        self.service.create_request(
            "SR101", "Rahul", "Laptop issue", "HIGH"
        )
        self.service.resolve_request("SR101")
        with self.assertRaises(RequestAlreadyResolvedError):
            self.service.resolve_request("SR101")

    def test_request_not_found_is_rejected(self) -> None:
        with self.assertRaises(RequestNotFoundError):
            self.service.search_request("SR999")


if __name__ == "__main__":
    unittest.main()
