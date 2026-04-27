AI-Enhanced SOC & Helpdesk Decision-Support System
Group: Cameron Edenburn & Jacob Moore

--- FOLDER STRUCTURE ---
/soc_logic   - Contains the AI API client, data normalization, and severity scoring modules.
/templates   - Contains the HTML views for the Staff and Employee dashboards.
/static      - Contains the CSS styling.
app.py       - The core Flask application, routing, and SQLite database initialization.

--- HOW TO RUN LOCALLY ---
1. Ensure Python 3.10+ is installed on your machine.
2. Open your terminal and navigate to the root directory of this project.
3. Install the required dependencies by running:
   pip install -r requirements.txt
4. Rename the ".env.example" file to ".env" and insert a valid Cohere API key.
5. Launch the application by running:
   python app.py
6. Open your web browser and navigate to:
   http://127.0.0.1:8081

Test Credentials:
- Staff Login: jacob / pass123
- Employee Login: john / user123

We are going to use the git function.
We just ran short of time this week,
but we will be implementing that next week.