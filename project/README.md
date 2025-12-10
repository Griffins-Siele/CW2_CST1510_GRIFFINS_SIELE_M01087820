# Portfolio Project: Analytics Dashboard

## Overview

This is a **capstone project** that integrates comprehensive learning from **Weeks 7-11** of the Data Communications and Networks course. It demonstrates professional software engineering practices through a fully functional **Streamlit-based analytics dashboard**.

**Pathway**: Data Science  
**Application Type**: Cyber Incident Analytics Dashboard  
**Status**: Production-Ready

---

## Learning Integration

### Week 7: Security & Authentication
- **File**: `app/services/auth_service.py`
- **Concepts**: 
  - ✅ Bcrypt password hashing
  - ✅ User registration with validation
  - ✅ Secure login verification
  - ✅ Error handling

```python
# Example: Secure authentication
success, message = login_user("alice", "password123")
if success:
    st.session_state.logged_in = True
```

### Week 8: Database & Data Management
- **File**: `app/services/data_service.py`
- **Concepts**:
  - ✅ CSV data loading
  - ✅ Data filtering and aggregation
  - ✅ Summary statistics
  - ✅ Error handling for data operations

```python
# Example: Data processing
data_service = get_data_service()
df = data_service.load_csv("incidents.csv")
filtered = data_service.filter_data(df, severity="High")
```

### Week 9: Streamlit Framework
- **Files**: `Home.py`, `pages/*.py`
- **Concepts**:
  - ✅ Multi-page applications
  - ✅ Session state management
  - ✅ Interactive UI components
  - ✅ Data visualization

```python
# Example: Session state
from app.session_state import init_session, is_logged_in
init_session()
if is_logged_in():
    st.success(f"Welcome, {get_current_user()}")
```

### Week 10: API Integration & Networking
- **Planned Feature**: External data source integration
- **Concepts**:
  - HTTP requests to APIs
  - Data transformation
  - Real-time updates

### Week 11: Object-Oriented Programming
- **File**: `app/data/models.py`
- **Concepts**:
  - ✅ Class design with encapsulation
  - ✅ Private attributes and getters
  - ✅ Inheritance (Entity → User → AnalyticsRecord)
  - ✅ Polymorphism in data models
  - ✅ Error handling with validation

```python
# Example: OOP with inheritance
class User(Entity):
    def __init__(self, user_id, username, email, role):
        super().__init__(user_id, username)
        self.__email = email
        self.__role = role

user = User(1, "alice", "alice@example.com", "analyst")
```

---

## Project Architecture

```
project/
├── Home.py                          # Main Streamlit app
├── requirements.txt                 # Dependencies
├── app/
│   ├── __init__.py
│   ├── session_state.py            # Session management (Week 9)
│   ├── data/
│   │   ├── __init__.py
│   │   ├── models.py               # OOP models (Week 11)
│   │   └── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py         # Authentication (Week 7)
│       └── data_service.py         # Data management (Week 8)
├── pages/
│   ├── 📊Dashboard.py              # Dashboard visualization
│   ├── 📈Analytics.py              # Advanced analytics
│   └── 📋DataManager.py            # Data CRUD operations
└── DATA/
    └── (sample data files)
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- pip or conda

### Installation

1. **Clone the repository**:
```bash
cd project
```

2. **Create virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
# From the project directory
streamlit run Home.py
```

The app will be available at `http://localhost:8501`

---

## Features

### ✅ Implemented

1. **User Authentication** (Week 7)
   - Secure bcrypt password hashing
   - User registration and login
   - Input validation
   - Error handling

2. **Data Management** (Week 8)
   - CSV file loading
   - Data filtering and aggregation
   - Statistics calculation
   - Caching for performance

3. **Interactive Dashboard** (Week 9)
   - Multi-page Streamlit app
   - Session state management
   - Real-time data updates
   - Responsive UI

4. **Object-Oriented Design** (Week 11)
   - Base `Entity` class
   - Specialized `User` and `AnalyticsRecord` classes
   - Encapsulation with private attributes
   - Getter methods for data access
   - Inheritance and polymorphism
   - Input validation in constructors

### Key Pages

| Page | Features |
|------|----------|
| **Home** | Login/Register, Dashboard overview, KPIs |
| **📊 Dashboard** | Executive KPIs, incident charts, status distribution |
| **📈 Analytics** | Incident analysis, ticket analytics, user activity |
| **📋 Data Manager** | View datasets, upload data, create records, settings |

---

## Security Features

- ✅ **Bcrypt Password Hashing**: Industry-standard password security
- ✅ **Input Validation**: All user inputs validated
- ✅ **Error Handling**: Comprehensive try-catch blocks
- ✅ **Session Management**: Secure session state in Streamlit
- ✅ **Data Validation**: Type checking and range validation

---

## Sample Data

The application comes with sample data for demonstration:

### Cyber Incidents
```
ID | Date       | Type           | Severity | Status      | Analyst
---|------------|----------------|----------|-------------|--------
1  | 2024-01-01 | Phishing       | High     | Resolved    | alice
2  | 2024-01-02 | Malware        | Critical | In Progress | bob
```

### IT Tickets
```
ID   | Priority | Status        | Assigned To
-----|----------|---------------|-------------
1001 | High     | Assigned      | tech1
1002 | Critical | In Progress   | tech2
```

### Users
```
Username | Email           | Role    | Status
---------|-----------------|---------|--------
alice    | alice@ex.com    | Analyst | Active
bob      | bob@ex.com      | Admin   | Active
```

---

## Testing

### Test Authentication
```python
from app.services.auth_service import register_user, login_user

# Register
success, msg = register_user("testuser", "password123")
print(msg)  # User 'testuser' registered successfully!

# Login
success, msg = login_user("testuser", "password123")
print(msg)  # Login successful for testuser!
```

### Test OOP Models
```python
from app.data.models import User, AnalyticsRecord

# Create user with validation
user = User(1, "alice", "alice@example.com", "analyst")
print(user)  # User(alice, role=analyst, logins=0)

# Create analytics record
record = AnalyticsRecord(1, "User Growth", "percentage", 12.5)
print(record)  # AnalyticsRecord(User Growth: 12.5 percentage)
```

### Test Data Service
```python
from app.services.data_service import get_data_service

service = get_data_service()
# This will work with actual CSV files in DATA/
```

---

## Learning Outcomes

By completing this project, you should be able to:

1. ✅ **Understand OOP Principles**
   - Classes, objects, inheritance, polymorphism
   - Encapsulation with private attributes
   - Type validation and error handling

2. ✅ **Build Secure Applications**
   - Implement password hashing
   - Validate user input
   - Handle authentication errors

3. ✅ **Create Data-Driven Applications**
   - Load and process CSV data
   - Generate analytics and insights
   - Visualize data effectively

4. ✅ **Develop Web Applications**
   - Build multi-page Streamlit apps
   - Manage application state
   - Create responsive user interfaces

5. ✅ **Follow Best Practices**
   - Modular code organization
   - Comprehensive error handling
   - Clear documentation
   - Professional code structure

---

## License

This project is part of the CST1510 coursework.

---

## Author

**GRIFFINS SIELE**  
M01087820  
Data Communications and Networks  
CW2_CST1510_GRIFFINS_SIELE_M01087820

**GitHub**: https://github.com/Griffins-Siele/CW2_CST1510_GRIFFINS_SIELE_M01087820
