---
name: backend-python-env
description: Defines the active Python virtual environment (.venv) and exact interpreter path for the Django backend. Use this whenever executing Python scripts, manage.py commands, tests, or database operations.
---

# Backend Python Environment & Virtualenv Guide

## Virtual Environment Location & Executable
The backend uses a dedicated Windows Python virtual environment (`.venv`) located inside `backend/.venv`.

- **Python Virtualenv Root**: `d:\Axinix Projects\Billing-ERP\backend\.venv`
- **Exact Python Executable**: `d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe`
- **Django Manage.py Path**: `d:\Axinix Projects\Billing-ERP\backend\manage.py`
- **Working Directory (Cwd)**: `d:\Axinix Projects\Billing-ERP\backend`

---

## Command Execution Syntax (PowerShell)

Always invoke the virtual environment python using quotes and the call operator `&`:

```powershell
# Django Management Commands
& "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" manage.py <command>

# Django Shell Command Execution
& "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" manage.py shell -c "<python_code>"

# Running Migrations
& "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" manage.py migrate

# Pip package operations inside virtualenv
& "d:\Axinix Projects\Billing-ERP\backend\.venv\Scripts\python.exe" -m pip <pip_command>
```

