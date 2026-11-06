# Database Initialization & Seeding Rule

## Rule 1: Always Seed Data After Migrations or Database Resets
When initializing a fresh database, running migrations from scratch, or switching to a new local SQLite/MySQL database, you MUST immediately populate it by running the following sequence of commands in the `backend/` directory:

1. `python manage.py migrate` (To create tables)
2. `python manage.py seed_db` (To populate roles, default admin user, demo categories, products, and statutory settings)

## Rule 2: Default Credentials Standard
- **Admin Username**: `admin` / Password: `password123`
- **Cashier Username**: `cashier` / Password: `password123`

## Rule 3: UI Blank State Prevention
If the frontend UI loads successfully but categories, products, or essential dropdowns are empty or not shown, verify that seed data is loaded into the database and run the seeding script.
