# Smart Service Desk Management System

## Overview

The **Smart Service Desk Management System** is a command-line application developed using Python for an employee IT support process. Support staff can create service requests, review stored requests, find a request by Request ID, and resolve open requests.

All request information is stored in a JSON file, so it remains available after the application is closed and restarted.

**Technology:** Python  
**Application type:** Individual practical assignment  
**Interface:** Command-line interface (CLI)  
**Repository:** https://github.com/varunnita/Smart_Service_Desk_Management_System_Varun.git

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Implemented Features](#implemented-features)
- [Required Menu](#required-menu)
- [Allowed Values](#allowed-values)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Class and Module Responsibilities](#class-and-module-responsibilities)
- [Exception Handling](#exception-handling)
- [JSON Persistence](#json-persistence)
- [Software-Engineering Concepts](#software-engineering-concepts)
- [Prerequisites](#prerequisites)
- [Installation and Running](#installation-and-running)
- [CLI Demonstration](#cli-demonstration)
- [Running Automated Tests](#running-automated-tests)
- [Git Workflow](#git-workflow)
- [Submission Details](#submission-details)
- [Evaluation Notes](#evaluation-notes)

---

## Problem Statement

A company receives IT support requests from employees for issues involving laptops, software, networks, passwords, accounts, and system access. Previously, these requests were maintained manually.

This application provides a small, structured solution that allows support staff to:

1. Create a service request.
2. View all service requests.
3. Search for a request using its Request ID.
4. Resolve an open request.
5. Preserve request details and status using a JSON file.

Advanced features such as engineer assignment, notifications, filtering, reporting, databases, APIs, and multiple status transitions are not required.

---

## Implemented Features

### 1. Create a Service Request

The user enters:

- Request ID
- Employee name
- Issue description
- Priority

The status is automatically set to `OPEN`.

Business rules:

- The Request ID must not already exist.
- Priority must be `LOW`, `MEDIUM`, or `HIGH`.
- Request IDs are normalized to uppercase.
- Request details are saved immediately after creation.

### 2. View All Requests

The application displays every saved request in the format:

```text
SR101 | Rahul | Laptop is not starting | HIGH | OPEN
```

No sorting or filtering is applied.

### 3. Search a Request

The application accepts only a Request ID for searching. If the ID exists, all request fields are displayed. If it does not exist, the application prints a friendly `Request not found` message.

### 4. Resolve a Request

When an open request is resolved:

```text
OPEN -> RESOLVED
```

The change is saved to JSON immediately.

If the request is already resolved, the application does not change or resave it and instead reports that it is already resolved.

### 5. Persistence

Requests are loaded from `data/requests.json` when the application starts. The application handles missing and empty JSON files safely.

---

## Required Menu

```text
SMART SERVICE DESK SYSTEM

1. Create Service Request
2. View All Requests
3. Search Request
4. Resolve Request
5. Exit

Enter your choice:
```

Any menu value outside `1` to `5` produces a clear validation message instead of stopping the application.

---

## Allowed Values

| Field | Allowed Values |
|---|---|
| Priority | `LOW`, `MEDIUM`, `HIGH` |
| Status | `OPEN`, `RESOLVED` |

Priority input is normalized to uppercase, so values such as `high`, `HIGH`, and `High` are accepted consistently.

---

## Project Structure

```text
Smart_Service_Desk_Management_System_Varun/
|-- domain/
|   |-- __init__.py
|   |-- service_request.py
|   `-- exceptions.py
|-- application/
|   |-- __init__.py
|   `-- request_service.py
|-- infrastructure/
|   |-- __init__.py
|   `-- file_repository.py
|-- data/
|   `-- requests.json
|-- tests/
|   `-- test_service_request.py
|-- main.py
|-- README.md
`-- .gitignore
```

---

## Architecture

The application follows a basic Domain-Driven Design (DDD) structure and separates presentation, application, domain, and infrastructure concerns.

```text
Presentation: main.py
      |
      v
Application: RequestService
      |
      +--> Domain: ServiceRequest
      |
      +--> Repository abstraction: RequestRepository
                    |
                    v
Infrastructure: FileRepository
                    |
                    v
              data/requests.json
```

### Request Flow

1. `main.py` collects menu choices and user input.
2. `RequestService` coordinates the requested operation.
3. `ServiceRequest` validates domain values and applies request behavior.
4. `RequestRepository` defines the persistence contract.
5. `FileRepository` converts domain objects to JSON and back.

This separation allows the domain and application layers to remain independent of JSON implementation details.

---

## Class and Module Responsibilities

### `domain/service_request.py`

Contains the `ServiceRequest` domain entity.

It provides:

- The request constructor and attributes
- Priority validation
- Status validation
- The `resolve()` behavior
- Conversion to and from dictionary/JSON-compatible data

The `OPEN` to `RESOLVED` transition is implemented inside `ServiceRequest.resolve()`. Other application code does not directly assign the status.

### `domain/exceptions.py`

Contains custom exceptions used to represent predictable application failures.

### `application/request_service.py`

Contains the `RequestService` use cases:

- `create_request()`
- `view_requests()`
- `search_request()`
- `resolve_request()`

It coordinates duplicate checking and persistence while depending on an abstract repository rather than a concrete JSON implementation.

### `infrastructure/file_repository.py`

Contains the `FileRepository` adapter:

- Loads JSON data
- Creates the data directory if needed
- Writes JSON safely through a temporary file
- Converts stored dictionaries into `ServiceRequest` objects

### `main.py`

Contains the CLI presentation logic:

- Displays the menu
- Reads user input
- Calls application use cases
- Prints success, status, and friendly error messages
- Controls application exit

---

## Exception Handling

The application uses custom exceptions for expected errors and does not rely on unrestricted `except:` blocks.

| Exception | Meaning | Example Message |
|---|---|---|
| `DuplicateRequestIdError` | Request ID already exists | `Request ID SR101 already exists` |
| `RequestNotFoundError` | Search or resolution ID was not found | `Request not found: SR999` |
| `InvalidPriorityError` | Priority is not allowed | `Priority must be LOW, MEDIUM or HIGH` |
| `RequestAlreadyResolvedError` | An already resolved request was resolved again | `Request SR101 is already RESOLVED` |
| `InvalidMenuChoiceError` | Menu choice is outside `1` to `5` | `Invalid menu choice. Enter a number from 1 to 5.` |

The CLI catches these specific exceptions and continues running instead of crashing.

---

## JSON Persistence

Request data is stored in:

```text
data/requests.json
```

Example JSON structure:

```json
[
    {
        "request_id": "SR101",
        "employee_name": "Rahul",
        "issue": "Laptop is not starting",
        "priority": "HIGH",
        "status": "OPEN"
    }
]
```

Persistence behavior:

- A missing file is treated as an empty request collection.
- An empty file is handled safely.
- A request is saved immediately after creation.
- A resolution is saved immediately after the status changes.
- A temporary file is used for writing, then replaced with `requests.json`.
- Invalid JSON or invalid top-level JSON format produces a clear runtime error.

---

## Software-Engineering Concepts

### Object-Oriented Programming

- Encapsulation of request data and resolve behavior
- Constructor and attribute initialization
- Domain methods and object conversion behavior
- Reusable objects returned by application use cases

### Exception Handling

- Custom domain exceptions
- Specific exception handling in the CLI
- Friendly messages for invalid input and expected business errors

### File Handling

- Reading from JSON
- Writing to JSON
- Safe handling of missing and empty files
- Temporary-file replacement to reduce the risk of partially written data

### Separation of Responsibilities

- `main.py` manages presentation and application flow.
- `RequestService` manages use cases.
- `ServiceRequest` manages domain behavior.
- `FileRepository` manages technical persistence.

### SOLID Principles

- **Single Responsibility:** Every major class has one primary responsibility.
- **Dependency Inversion:** `RequestService` uses the `RequestRepository` abstraction, while `FileRepository` provides the concrete implementation.
- **Open/Closed Direction:** Persistence can be replaced by another repository implementation without changing domain behavior.

### Domain-Driven Design

- Domain logic belongs in the domain layer.
- JSON and file-system concerns do not belong inside `ServiceRequest`.
- The application layer coordinates use cases.
- Infrastructure implements persistence details.

### Git

- Development work is performed on `development`.
- Tested changes are merged into `main`.
- Commits use clear, meaningful descriptions.

---

## Prerequisites

- Python 3.9 or newer
- Git
- A terminal or command prompt

No third-party Python packages are required.

---

## Installation and Running

### 1. Clone the Repository

```bash
git clone https://github.com/varunnita/Smart_Service_Desk_Management_System_Varun.git
cd Smart_Service_Desk_Management_System_Varun
```

### 2. Run the Application

From the project directory:

```bash
python main.py
```

If the `python` command is unavailable on Windows, try:

```bash
py main.py
```

The application creates or uses `data/requests.json` automatically.

---

## CLI Demonstration

### Create SR101

```text
Enter Request ID: SR101
Enter Employee Name: Rahul
Enter Issue: Laptop is not starting
Enter Priority: HIGH

Service Request created successfully.
```

### Try to Create SR101 Again

```text
Request ID SR101 already exists
```

### View and Search

```text
SR101 | Rahul | Laptop is not starting | HIGH | OPEN
```

### Resolve SR101

```text
Request SR101 resolved successfully.
```

### Resolve It Again

```text
Request SR101 is already RESOLVED
```

### Restart Persistence Test

1. Exit using menu choice `5`.
2. Restart the application with `python main.py`.
3. Search for `SR101`.
4. Confirm that the saved status is `RESOLVED`.

---

## Running Automated Tests

Run all unit tests from the project directory:

```bash
python -m unittest discover -s tests -v
```

The test suite covers:

- Creating and reloading a request
- Duplicate Request IDs
- Invalid priority
- Request-not-found handling
- Resolving and persisting a request
- Rejecting resolution of an already resolved request

---

## Git Workflow

The repository uses two branches:

- `main`: final, tested code
- `development`: active implementation work

Meaningful commits include:

1. Initial project structure
2. ServiceRequest domain model
3. JSON repository and request service
4. CLI application and tests

Review the branch and merge history with:

```bash
git branch
git log --oneline --graph --decorate --all
```

Typical merge workflow:

```bash
git switch development
# make and test changes
git add .
git commit -m "Add requested feature"

git switch main
git merge development
git push -u origin main
git push -u origin development
```

---

## Submission Details

```text
Name: Varun
Participant ID:
Git Repository URL: https://github.com/varunnita/Smart_Service_Desk_Management_System_Varun.git
Final Commit ID:
```

The participant ID and final commit ID can be added by the student before submission.

---

## Evaluation Notes

### Explainable Design Points

- `ServiceRequest` belongs in the domain layer because it represents core business data and behavior.
- `resolve()` implements the `OPEN` to `RESOLVED` business rule.
- JSON is separate from the domain entity so that request behavior is not coupled to file storage.
- `RequestService` demonstrates application-level use-case coordination.
- `FileRepository` demonstrates separation of infrastructure concerns.
- Custom exceptions represent predictable business and input failures.

### Mandatory Demonstration Sequence

1. Show the `development` branch and commit history.
2. Create `SR101` with priority `HIGH`.
3. Try to create `SR101` again.
4. View all requests.
5. Search for `SR101`.
6. Resolve `SR101`.
7. Try to resolve `SR101` again.
8. Exit the application.
9. Restart it.
10. Search for `SR101` and prove that it is `RESOLVED`.
