# Backend Python Environment & Virtualenv Management

## Purpose
Defines the standard procedure for managing, activating, and executing Django CLI commands inside the dedicated backend Python virtual environment.

## When to use
Whenever running `manage.py` commands, migrations, seeds, tests, or installing backend dependencies.

## Scope and assumptions
- Windows PowerShell environment
- Python 3.12+ / 3.15 installed
- Virtualenv located at `backend/.venv`

## Prerequisites
- Windows PowerShell with execution permissions

## Procedure
1. **Creation**:
   ```powershell
   python -m venv "backend/.venv"
   ```
2. **Execution syntax in PowerShell**:
   Always use quotes and the call operator `&`:
   ```powershell
   & "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" backend/manage.py migrate
   & "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" backend/manage.py seed_db
   ```
3. **Dependency installation**:
   ```powershell
   & "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" -m pip install -r backend/requirements.txt
   ```

## Security and safety constraints
- Never install project packages into system-level global Python.
- Do not commit `.venv` to version control.

## Verification
Run `& "backend/.venv/Scripts/python.exe" --version` and `manage.py check`.

## Common failure modes
- Invoking `python manage.py` without specifying virtualenv path uses system Python which lacks dependencies.
