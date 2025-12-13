"""AI Chat Assistant Page - Intelligent Platform Assistant (Week 10 Integration)

This page provides an AI-powered chatbot that helps users navigate the platform,
understand their data, and get insights from analytics.
"""

import streamlit as st
import sys
from pathlib import Path
from datetime import datetime
import os
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.session_state import is_logged_in, get_current_user

# Load environment variables
load_dotenv()

try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

st.set_page_config(page_title="AI Assistant", page_icon="🤖", layout="wide")

# Check authentication
if not is_logged_in():
    st.error("⚠️ Please log in first!")
    st.stop()

st.title("🤖 AI Assistant")
st.markdown("### Your Intelligent Platform Guide")

with st.sidebar:
    st.header("Navigation")
    st.success(f"✅ User: {get_current_user()}")
    
    st.divider()
    
    st.subheader(" OpenAI Configuration")
    
    # Check if API key is in environment variables
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    
    if openai_api_key:
        st.success("✅ OpenAI API Key Loaded from .env")
        st.caption("Key configured in environment variables")
        
        # Try to validate the key
        try:
            client = OpenAI(api_key=openai_api_key)
            client.models.list()
            st.session_state.openai_api_key = openai_api_key
        except Exception as e:
            st.error(f"❌ Invalid API Key in .env: {str(e)[:50]}")
    else:
        st.warning("⚠️ No API Key Found")
        st.markdown("""
        **To enable OpenAI features:**
        
        1. Create a `.env` file in the `project/` folder
        2. Add this line:
           ```
           OPENAI_API_KEY=sk-your-key-here
           ```
        3. Get your key from [OpenAI Platform](https://platform.openai.com/api-keys)
        4. Restart the Streamlit app
        
        Without an API key, the assistant uses the built-in knowledge base.
        """)
    
    st.divider()
    
    if st.button("🚪 Logout", use_container_width=True):
        from app.session_state import logout
        logout()
        st.rerun()

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "chat_session_id" not in st.session_state:
    st.session_state.chat_session_id = datetime.now().isoformat()

# AI Knowledge Base
KNOWLEDGE_BASE = {
    "dashboard": {
        "description": "Executive dashboard with KPIs",
        "info": "The Dashboard tab shows key performance indicators including total incidents, critical issues, resolution rate, and average response time.",
        "keywords": ["dashboard", "kpi", "metrics", "incidents", "critical"]
    },
    "analytics": {
        "description": "Advanced analytics and data analysis",
        "info": "Analytics page provides detailed incident analysis, ticket tracking, user activity monitoring, and custom analysis tools for deeper insights.",
        "keywords": ["analytics", "analysis", "incidents", "tickets", "users", "trends"]
    },
    "data manager": {
        "description": "Data management and CRUD operations",
        "info": "Data Manager allows you to view datasets, upload CSV files, create new analytics records with validation, export data, and customize settings.",
        "keywords": ["data", "upload", "download", "export", "csv", "crud"]
    },
    "authentication": {
        "description": "User login and security",
        "info": "The platform uses bcrypt password hashing for security. Your passwords are never stored in plain text and are protected with industry-standard cryptography.",
        "keywords": ["login", "register", "password", "security", "authentication", "bcrypt"]
    },
    "incidents": {
        "description": "Cyber security incidents tracking",
        "info": "Track and analyze cyber incidents including phishing attacks, malware, DDoS attacks, and SQL injections. Each incident has severity levels and status tracking.",
        "keywords": ["incidents", "phishing", "malware", "ddos", "security", "cyber"]
    },
    "tickets": {
        "description": "IT support tickets",
        "info": "Manage IT support tickets with different priority levels. Track tickets assigned to technicians and monitor resolution times.",
        "keywords": ["tickets", "support", "issues", "priority", "technician"]
    },
    "users": {
        "description": "User management and activity",
        "info": "Monitor user activity, track login counts, and manage user roles (User, Analyst, Admin) with different permission levels.",
        "keywords": ["users", "roles", "activity", "login", "management"]
    },
    "visualization": {
        "description": "Charts and data visualization",
        "info": "The platform provides various visualizations including bar charts for severity distribution, line charts for trends over time, and data tables with statistics.",
        "keywords": ["charts", "visualization", "graphs", "bar chart", "line chart", "tables"]
    },
    "architecture": {
        "description": "System architecture and design",
        "info": "Built with Streamlit framework, using bcrypt authentication (Week 7), pandas data processing (Week 8), multi-page structure (Week 9), and OOP principles (Week 11).",
        "keywords": ["architecture", "design", "structure", "system", "layers", "framework"]
    },
    "help": {
        "description": "Getting help",
        "info": "You can ask me about any feature! Try asking about: Dashboard, Analytics, Data Manager, or any specific feature you want to learn about.",
        "keywords": ["help", "guide", "tutorial", "how to"]
    }
}

def find_matching_topic(user_input):
    """Find the best matching topic from knowledge base"""
    user_input_lower = user_input.lower()
    
    # Direct keyword matching
    for topic, data in KNOWLEDGE_BASE.items():
        for keyword in data["keywords"]:
            if keyword in user_input_lower:
                return topic, data
    
    # Fuzzy matching for common phrases
    if "what is" in user_input_lower or "what's" in user_input_lower:
        return "help", KNOWLEDGE_BASE["help"]
    
    if "how" in user_input_lower or "how to" in user_input_lower:
        return "help", KNOWLEDGE_BASE["help"]
    
    return None, None

def generate_ai_response(user_input):
    """Generate AI response based on OpenAI API or knowledge base"""
    
    # Get API key from environment
    openai_api_key = os.getenv("OPENAI_API_KEY", "").strip()
    
    # Use OpenAI if API key is available
    if openai_api_key:
        try:
            client = OpenAI(api_key=openai_api_key)
            
            # System prompt for the AI
            system_prompt = """You are an intelligent assistant for a Portfolio Analytics Dashboard platform.
You help users understand and navigate the application which includes:
- Dashboard: Executive KPIs and metrics
- Analytics: Detailed incident analysis and reporting
- Data Manager: CSV file management and CRUD operations
- Authentication: Secure bcrypt-based login system
- Incident Tracking: Cyber security incidents (phishing, malware, DDoS, SQL injection)
- IT Tickets: Support ticket management
- User Management: User roles and activity tracking

Provide helpful, concise answers about the platform features and how to use them.
When users ask technical questions, explain in simple terms.
Always be friendly and professional."""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"⚠️ OpenAI Error: {str(e)}\n\nFalling back to knowledge base response...\n\n{generate_kb_response(user_input)}"
    else:
        # Use knowledge base if no API key
        return generate_kb_response(user_input)

def generate_kb_response(user_input):
    """Generate response from local knowledge base"""
    topic, topic_data = find_matching_topic(user_input)
    
    if topic:
        return f"**{topic_data['description'].title()}**\n\n{topic_data['info']}"
    else:
        # Generic response for unrecognized queries
        return (
            "I'm not sure about that topic. Here's what I can help you with:\n\n"
            "📊 **Dashboard** - Executive KPIs and metrics\n"
            "📈 **Analytics** - Detailed analysis and insights\n"
            "📋 **Data Manager** - Upload and manage data\n"
            "🔐 **Authentication** - Security and login\n"
            "🐛 **Incidents** - Cyber security tracking\n"
            "🎫 **Tickets** - IT support management\n"
            "👥 **Users** - User activity and roles\n"
            "📊 **Visualization** - Charts and graphs\n\n"
            "Try asking: 'What is the dashboard?' or 'How do I use analytics?'"
        )

# Main chat interface
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Chat with AI Assistant")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask me about the platform features...")
    
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.now()
        })
        
        # Generate AI response
        ai_response = generate_ai_response(user_input)
        
        # Add AI message to history
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": datetime.now()
        })
        
        # Rerun to display new messages
        st.rerun()

with col2:
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.success("Chat history cleared!")
        st.rerun()

st.divider()
