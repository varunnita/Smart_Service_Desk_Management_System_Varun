from typing import Dict

from domain.exceptions import InvalidPriorityError, RequestAlreadyResolvedError


class ServiceRequest:
    """Domain entity representing an employee's service request."""

    VALID_PRIORITIES = ("LOW", "MEDIUM", "HIGH")
    VALID_STATUSES = ("OPEN", "RESOLVED")

    def __init__(
        self,
        request_id: str,
        employee_name: str,
        issue: str,
        priority: str,
        status: str = "OPEN",
    ) -> None:
        self.request_id = self._require_non_empty(request_id, "Request ID")
        self.employee_name = self._require_non_empty(
            employee_name, "Employee Name"
        )
        self.issue = self._require_non_empty(issue, "Issue")

        normalized_priority = priority.strip().upper()
        if normalized_priority not in self.VALID_PRIORITIES:
            raise InvalidPriorityError(
                "Priority must be LOW, MEDIUM or HIGH"
            )
        self.priority = normalized_priority

        if status not in self.VALID_STATUSES:
            raise ValueError("Status must be OPEN or RESOLVED")
        self.status = status

    @staticmethod
    def _require_non_empty(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} cannot be empty")
        return value.strip()

    def resolve(self) -> None:
        """Apply the OPEN -> RESOLVED business transition."""
        if self.status == "RESOLVED":
            raise RequestAlreadyResolvedError(
                f"Request {self.request_id} is already RESOLVED"
            )
        self.status = "RESOLVED"

    def to_dict(self) -> Dict[str, str]:
        return {
            "request_id": self.request_id,
            "employee_name": self.employee_name,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "ServiceRequest":
        return cls(
            request_id=data["request_id"],
            employee_name=data["employee_name"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "OPEN"),
        )

    def __str__(self) -> str:
        return (
            f"{self.request_id} | {self.employee_name} | {self.issue} | "
            f"{self.priority} | {self.status}"
        )
