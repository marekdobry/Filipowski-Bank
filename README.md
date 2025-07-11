# Filipowski Bank Project

Flask-based web application for managing bank accounts, user administration, and transactions.

## Features

- User authentication and admin reset functionality
- Account management with database integration
- Responsive UI built with HTML templates using **Jinja** templating engine
- Static assets management (CSS, JavaScript, images)
- Secure handling of environment variables for sensitive data
- Modular Python code structure for easy maintenance

## Project Structure

- `app.py` — Main Flask application entry point  
- `adminreset.py` — Script for administrative reset tasks  
- `database/` — Contains database files (SQLite)  
- `static/` — Static assets like CSS, images  
- `templates/` — HTML templates rendered with **Jinja**  
- `venv/` — Python virtual environment (excluded from repo)  
- `.env` — Environment variables (excluded from repo)  

## Usage

The application is hosted online and accessible through a web browser. Users can create and manage bank accounts via the web interface. Admins can reset user data with the `adminreset.py` script.
