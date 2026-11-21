# Smart Service Desk Management System

A reduced-scope Python CLI application for creating, viewing, searching, and resolving IT support service requests. Requests are persisted in JSON so their data remains available after the application is closed and restarted.

## Implemented features

- Create requests with an automatically assigned `OPEN` status
- Prevent duplicate Request IDs
- View every stored request
- Search by Request ID
- Resolve open requests and persist the `RESOLVED` status
- Validate priorities and menu choices
- Safely handle missing or empty JSON files
- Friendly handling of duplicate IDs, missing requests, invalid priority, and repeated resolution

## Python concepts and architecture

- **OOP:** `ServiceRequest` encapsulates request data and the resolve behavior.
- **Exceptions:** Custom exceptions represent domain and input failures.
- **File handling:** `FileRepository` reads and writes JSON using atomic temporary-file replacement.
- **SOLID:** `RequestService` depends on the `RequestRepository` abstraction rather than directly on JSON.
- **DDD:** Domain, application, infrastructure, and presentation responsibilities are separated.
- **Git:** Development is performed on `development`; tested work is merged into `main`.

## Project structure

```text
smart-service-desk/
|-- domain/
|   |-- service_request.py
|   `-- exceptions.py
|-- application/
|   `-- request_service.py
|-- infrastructure/
|   `-- file_repository.py
|-- data/
|   `-- requests.json
|-- tests/
|   `-- test_service_request.py
|-- main.py
|-- README.md
`-- .gitignore
```

## Run

From the project directory:

```bash
python main.py
```

On first run, `data/requests.json` is created or reused as needed.

## Allowed values

- Priority: `LOW`, `MEDIUM`, `HIGH`
- Status: `OPEN`, `RESOLVED`

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Git branch workflow

Development work is committed on `development`, with at least four meaningful commits. After testing, the branch is merged into `main` using a merge commit or fast-forward merge.

Useful demonstration commands:

```bash
git branch
git log --oneline --graph --all
git switch main
git merge development
git push -u origin main
```
