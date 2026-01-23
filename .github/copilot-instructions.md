# Copilot Instructions

## Repository Context
- This repository is the persistent memory store for the CTO Autonomous Brain system.
- Most files are operational logs, documentation, and automation configuration—keep changes minimal and targeted.

## Working in This Repository
- Prefer small, surgical edits focused on the request.
- Avoid touching historical logs unless the task explicitly calls for it.
- Maintain existing tone and formatting in documentation.

## Python Test Project
- The `copilot_test_project/` directory contains a Python demo with pytest-based tests.
- Keep updates isolated to that directory when changing demo code or tests.
- If tests are required, run `python -m pytest` from `copilot_test_project/`.

## Safety and Operations
- Do not add secrets or credentials to the repository.
- Avoid changing automation scripts (`auto_backup.*`, `auto_startup.*`) unless requested.
- Ensure any new files are documented if they affect operations.
