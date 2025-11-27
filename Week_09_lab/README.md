# Week 09 Lab: Streamlit Multi-Page Application

A secure, feature-rich Streamlit application demonstrating authentication, CRUD operations, analytics, and user management.

## Features

### 1. **Authentication & Security**
- **Secure Login/Register** with bcrypt password hashing
- Session state management for user authentication
- Protected pages (login required)
- User account persistence to `users.txt`

### 2. **Data Management (CRUD)**
- **Create**: Add new IT support tickets with auto-incrementing IDs
- **Read**: View all tickets with real-time filtering by status and priority
- **Update**: Edit ticket details (title, priority, status, assignee)
- **Delete**: Remove tickets with confirmation
- Sample data: IT tickets dataset with 10+ records

### 3. **Analytics Dashboard**
- **KPI Metrics**: Total tickets, high priority count, open/closed statistics
- **Visualizations**: 
  - Status distribution (bar chart)
  - Priority breakdown (pie/bar chart)
  - Assignee workload distribution
- **Filtering**: Multi-select filters for status and priority
- **Export**: Download filtered data as CSV or JSON

### 4. **User Settings**
- **Profile Management**: Username, email, full name, department
- **Preferences**: Theme, language, notifications, data retention
- **Security**: Password change, active sessions, 2FA setup info, account deletion
- **Logout**: Secure session termination

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project folder:**
   ```bash
   cd "C:\Users\Hp\OneDrive\Desktop\School\Programming for Data Communications and Networks\CW2_CST1510_GRIFFINS_SIELE_M01087820\Week_09_lab"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows (PowerShell):**
     ```bash
     .\.venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   python -m streamlit run .\Home.py
   ```

   The app will open in your default browser at `http://localhost:8501`

## 📁 Project Structure

```
Week_09_lab/
├── Home.py                    # Main entry point (Login/Register)
├── requirements.txt           # Python dependencies
├── users.py                   # User authentication & bcrypt utilities
├── session_state.py           # Session state initialization
├── users.txt                  # Persisted user credentials (auto-created)
├── pages/
│   ├── __init__.py
│   ├── Dashboard.py          # Protected welcome page
│   ├── DataManager.py        # CRUD operations for IT tickets
│   ├── Analytics.py          # Dashboard with visualizations
│   ├── Settings.py           # User profile & preferences
│   └── Analytics.py          # Security/analytics dashboard
├── DATA/
│   ├── it_tickets.csv        # IT support tickets (10 records)
│   ├── cyber_incidents.csv   # Security incidents data
│   └── datasets_metadata.csv # Metadata about datasets
└── README.md                 # This file
```

## Authentication

### Register a New Account
1. On the home page, click the **Register** tab
2. Enter a username and password (confirm password)
3. Click **Create account**
4. Your account is securely stored with bcrypt-hashed password

### Login
1. Click the **Login** tab
2. Enter your username and password
3. Click **Log in**
4. You'll be redirected to the **Dashboard** and can access all protected pages

### Demo Credentials
If you want to test quickly without creating an account, you can manually add to `users.txt`:
```
test_user:$2b$12$... (bcrypt hash)
```
Or use the app's register feature.

## Pages Overview

### Home (Home.py)
- Entry point with Login/Register tabs
- Secure authentication with bcrypt
- Redirects to DataManager post-login

### Dashboard (pages/Dashboard.py)
- Protected page (login required)
- Welcome message with username
- Links to other sections

### Data Manager (pages/DataManager.py)
- **Read Tab**: View and filter IT tickets by status/priority
- **Create Tab**: Add new tickets with auto-generated IDs (TCK-####)
- **Update Tab**: Edit existing tickets
- **Delete Tab**: Remove tickets with confirmation
- Data stored in session (persists during session, resets on refresh)

### Analytics (pages/Analytics.py)
- **KPI Cards**: Total, high-priority, open/closed ticket metrics
- **Visualizations**: Charts for status, priority, and assignee workload
- **Filters**: Multi-select status and priority filters
- **Export**: Download data as CSV or JSON
- Real-time updates from `DATA/it_tickets.csv`

### Settings (pages/Settings.py)
- **Profile Tab**: View/edit username, email, department
- **Preferences Tab**: Theme, language, notifications, data retention
- **Security Tab**: Change password, view active sessions, setup 2FA, logout
- User-friendly interface for account management

## Security Features

✅ **Bcrypt Password Hashing**: Passwords are hashed with 12 rounds of bcrypt (not plaintext)
✅ **Session State Management**: Login state tracked securely
✅ **Protected Pages**: All pages except Home require authentication
✅ **Atomic File Operations**: User data saved atomically to prevent corruption
✅ **User Isolation**: Each user can only access their own data (in session)

**Demo Limitations**:
- No database (uses CSV & plaintext file storage)
- Session data resets on page refresh
- No HTTPS/SSL in demo environment
- For production, use a proper database and authentication provider

## Dependencies

- **streamlit** (1.0+): Web framework
- **bcrypt**: Password hashing
- **pandas**: Data manipulation
- **numpy**: Numerical computing

See `requirements.txt` for exact versions.

## Testing

### Test Login Flow
1. Start the app: `python -m streamlit run .\Home.py`
2. Register a new account with username "testuser" and password "testpass123"
3. Verify `users.txt` contains the new account (hashed password)
4. Log out and log back in with the same credentials
5. Verify you're authenticated and can access all pages

### Test CRUD Operations
1. Navigate to **Data Manager** page
2. Create a new ticket (status, priority, assignee)
3. Verify it appears in the Read tab
4. Update the ticket (change priority/status)
5. Delete the ticket with confirmation
6. Verify it's removed from the list

### Test Analytics
1. Navigate to **Analytics** page
2. Apply filters (status, priority)
3. Verify filtered data updates in real-time
4. Download as CSV/JSON and verify file content
5. Check KPI metrics for accuracy

