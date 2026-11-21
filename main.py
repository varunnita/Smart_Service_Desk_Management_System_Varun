from pathlib import Path

from application.request_service import RequestService
from domain.exceptions import (
    DuplicateRequestIdError,
    InvalidMenuChoiceError,
    InvalidPriorityError,
    RequestAlreadyResolvedError,
    RequestNotFoundError,
    ServiceDeskError,
)
from infrastructure.file_repository import FileRepository


class SmartServiceDeskApp:
    """Presentation and CLI flow."""

    def __init__(self) -> None:
        data_file = Path(__file__).resolve().parent / "data" / "requests.json"
        repository = FileRepository(data_file)
        self.service = RequestService(repository)

    def run(self) -> None:
        while True:
            self.print_menu()
            try:
                choice = input("Enter your choice: ").strip()
                if choice not in {"1", "2", "3", "4", "5"}:
                    raise InvalidMenuChoiceError(
                        "Invalid menu choice. Enter a number from 1 to 5."
                    )

                if choice == "1":
                    self.create_request()
                elif choice == "2":
                    self.view_requests()
                elif choice == "3":
                    self.search_request()
                elif choice == "4":
                    self.resolve_request()
                else:
                    print("Thank you for using Smart Service Desk.")
                    break
            except (
                DuplicateRequestIdError,
                RequestNotFoundError,
                InvalidPriorityError,
                RequestAlreadyResolvedError,
                InvalidMenuChoiceError,
                ValueError,
                RuntimeError,
            ) as error:
                print(error)

    @staticmethod
    def print_menu() -> None:
        print("\nSMART SERVICE DESK SYSTEM")
        print("1. Create Service Request")
        print("2. View All Requests")
        print("3. Search Request")
        print("4. Resolve Request")
        print("5. Exit")

    def create_request(self) -> None:
        request_id = input("Enter Request ID: ").strip()
        employee_name = input("Enter Employee Name: ").strip()
        issue = input("Enter Issue: ").strip()
        priority = input("Enter Priority: ").strip()

        request = self.service.create_request(
            request_id, employee_name, issue, priority
        )
        print("Service Request created successfully.")

    def view_requests(self) -> None:
        requests = self.service.view_requests()
        if not requests:
            print("No service requests found.")
            return
        for request in requests:
            print(request)

    def search_request(self) -> None:
        request_id = input("Enter Request ID: ").strip()
        print(self.service.search_request(request_id))

    def resolve_request(self) -> None:
        request_id = input("Enter Request ID: ").strip()
        request = self.service.resolve_request(request_id)
        print(f"Request {request.request_id} resolved successfully.")


if __name__ == "__main__":
    SmartServiceDeskApp().run()
