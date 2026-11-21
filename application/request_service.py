from abc import ABC, abstractmethod
from typing import Dict, List

from domain.exceptions import (
    DuplicateRequestIdError,
    RequestNotFoundError,
)
from domain.service_request import ServiceRequest


class RequestRepository(ABC):
    """Port for request persistence; infrastructure provides the adapter."""

    @abstractmethod
    def load(self) -> List[ServiceRequest]:
        raise NotImplementedError

    @abstractmethod
    def save(self, requests: List[ServiceRequest]) -> None:
        raise NotImplementedError


class RequestService:
    """Coordinates service-request use cases without knowing JSON details."""

    def __init__(self, repository: RequestRepository) -> None:
        self.repository = repository
        self.requests: Dict[str, ServiceRequest] = {}
        for request in repository.load():
            self.requests[request.request_id] = request

    def create_request(
        self,
        request_id: str,
        employee_name: str,
        issue: str,
        priority: str,
    ) -> ServiceRequest:
        if request_id.strip().upper() in self.requests:
            raise DuplicateRequestIdError(
                f"Request ID {request_id.strip().upper()} already exists"
            )

        request = ServiceRequest(
            request_id=request_id.strip().upper(),
            employee_name=employee_name,
            issue=issue,
            priority=priority,
        )
        self.requests[request.request_id] = request
        self.repository.save(list(self.requests.values()))
        return request

    def view_requests(self) -> List[ServiceRequest]:
        return list(self.requests.values())

    def search_request(self, request_id: str) -> ServiceRequest:
        normalized_id = request_id.strip().upper()
        request = self.requests.get(normalized_id)
        if request is None:
            raise RequestNotFoundError(
                f"Request not found: {normalized_id}"
            )
        return request

    def resolve_request(self, request_id: str) -> ServiceRequest:
        request = self.search_request(request_id)
        request.resolve()
        self.repository.save(list(self.requests.values()))
        return request
