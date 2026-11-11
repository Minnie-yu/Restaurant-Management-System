# Restaurant Management System — MGIS320 Team 5 Nexolutions

> **Academic team project (MGIS320) · Nexolutions**  
> This repository contains a Python desktop application and its MySQL database schema. It is a **collaborative project**, not an individual end-to-end implementation.

## Overview

A restaurant operations management application built using **Python Tkinter** for the desktop interface and **MySQL** for relational data storage. Its modules cover customers, orders, inventory, budgeting, and database reporting.

## Features

- **Login & module navigation:** `AAAlog_in.py` provides the application entry point and module launcher.
- **Customer management:** `customer_manage.py` displays and manages customer information.
- **Order management:** `order_manage.py` supports order tracking and related reporting.
- **Inventory management:** `inventory_manage.py` handles ingredients and inventory information.
- **Budget management:** `budget_manage.py` tracks expenses and budget metrics with charts.
- **Database viewer:** `show_database.py` presents information from several operational tables.
- **Relational database:** `database_schema.sql` creates the MySQL schema and inserts sample data.

## Technologies

Python · Tkinter · MySQL · mysql-connector-python · PyMySQL · Pillow · tkcalendar · Matplotlib · NumPy

## Repository layout

```text
.
├── AAAlog_in.py             # Desktop application entry point
├── customer_manage.py       # Customer module
├── order_manage.py          # Orders module
├── inventory_manage.py      # Inventory module
├── budget_manage.py         # Budget and expense module
├── show_database.py         # Data viewer
├── database_schema.sql      # MySQL schema + illustrative sample records
├── *.png / *.ico            # UI images and icons
├── requirements.txt         # Python dependencies
├── .env.example             # Names of local configuration variables
└── README.md
```

## Local setup (development/demo)

1. Install Python 3 and a local MySQL server. Tkinter must also be available in your Python installation.
2. Create and activate a Python virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create the sample MySQL database:

   ```bash
   mysql -u root -p < database_schema.sql
   ```

   The SQL creates the `restaurant_test1` database and inserts **illustrative sample data**. Do not run it against a database containing important information without review.

4. Set local credentials in your Terminal (never commit real values):

   ```bash
   export MYSQL_PASSWORD='YOUR_LOCAL_MYSQL_PASSWORD'
   export APP_LOGIN_PASSWORD='YOUR_CHOSEN_DEMO_LOGIN_PASSWORD'
   ```

5. Start the Tkinter application:

   ```bash
   python3 AAAlog_in.py
   ```

   The login window asks for the application password and separately for your local MySQL password. Use the two values you chose above.

**Important:** This is an academic code snapshot, **not a hardened production service**. The scripts were syntax-checked for publication but **not end-to-end tested on a live MySQL environment**. The source uses a local MySQL `root` user, passes its password between modules in process arguments, and uses a simplified demo login. Do not expose it to an untrusted network or use real customer data. Consider refactoring to least-privilege database credentials, hashed user authentication, and safer credential handling before real deployment.

## Sample database

`database_schema.sql` defines these tables: `customer`, `meal`, `ingredient`, `customer_order`, `order_line_item`, `meal_ingredient`, `ingredient_purchase`, `expense`. It includes example records (not a production database export).

The standalone uploaded SQL file was used as the latest schema: it adds `cancelled` as a possible `customer_order_status` value compared with the copy found inside the original ZIP.

## Team attribution

Developed collaboratively by **MGIS320 Team 5 — Nexolutions**. The individual responsibilities of team members should be added here once confirmed. Please obtain agreement from the team before distributing code or assets publicly.

## Publication notes

- Do not upload the original ZIP: it includes `.venv/`, `.idea/`, and a runtime log.
- This published copy removes local development artifacts and replaces hard-coded default credential values with environment variables. It also aligns one inventory database connection with the supplied SQL schema.
- Keep passwords, API keys, and personal data out of the repository **and its commit history**.
- No open-source license has been assigned. Please confirm ownership and licensing with all contributors before adding one.
