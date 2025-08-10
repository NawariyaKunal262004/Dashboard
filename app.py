import streamlit as st
import os
import sys
from datetime import datetime
import logging

# Add tools directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'tools'))

# Import all tools
from tools.ssh_utils import *
from tools.grocery_manager import run_grocery_manager
from tools.whatsapp_bot import run_whatsapp_bot
from tools.email_scheduler import run_email_scheduler
from tools.linkedin_automation import run_linkedin_automation
from tools.instagram_bot import run_instagram_bot
from tools.sms_sender import run_sms_sender
from tools.llm_tools import run_llm_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🤖 Automation Tools Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .tool-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        color: white;
        text-align: center;
        transition: transform 0.3s ease;
    }
    .tool-card:hover {
        transform: translateY(-5px);
    }
    .section-header {
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        color: #333;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin: 0.5rem;
    }
    .ssh-section {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header" style="text-align: center;">🌟 The Ultimate Astra</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-header" style="text-align: center;">🤖 Automation Tools Dashboard</h2>', unsafe_allow_html=True)
    st.markdown("**Your one-stop solution for automation, SSH management, and AI tools!**")
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    
    # Main sections
    sections = {
        "🏠 Dashboard": "dashboard",
        "🧰 Utility Tools": "utility_tools",
        "💻 Linux & Docker Commands": "linux_docker",
        "🌐 Apache Launcher": "apache_launcher",
        "🤖 LLMs Panel": "llm_panel"
    }
    
    selected_section = st.sidebar.selectbox(
        "Choose a section:",
        list(sections.keys()),
        index=0
    )
    
    # Dashboard section
    if sections[selected_section] == "dashboard":
        show_dashboard()
    
    # Utility Tools section
    elif sections[selected_section] == "utility_tools":
        show_utility_tools()
    
    # Linux & Docker Commands section
    elif sections[selected_section] == "linux_docker":
        show_linux_docker_commands()
    
    # Apache Launcher section
    elif sections[selected_section] == "apache_launcher":
        show_apache_launcher()
    
    # LLMs Panel section
    elif sections[selected_section] == "llm_panel":
        show_llm_panel()

def show_dashboard():
    """Show the main dashboard"""
    st.markdown('<h2 class="section-header">📊 Dashboard Overview</h2>', unsafe_allow_html=True)
    
    # Welcome message
    st.info("🎉 Welcome to your Automation Tools Dashboard! This comprehensive platform provides access to various automation tools, SSH management, and AI capabilities.")
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>🧰</h3>
            <h4>6 Tools</h4>
            <p>Utility Tools</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>💻</h3>
            <h4>50+ Commands</h4>
            <p>Linux & Docker</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>🌐</h3>
            <h4>Apache</h4>
            <p>One-Click Launch</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🤖</h3>
            <h4>4 LLMs</h4>
            <p>AI Models</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown("### 📈 Recent Activity")
    st.info("No recent activity to display. Start using the tools to see activity here!")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🛒 Open Grocery Manager", use_container_width=True):
            st.session_state.show_grocery_manager = True
            st.rerun()
        
        if st.button("📱 Open WhatsApp Bot", use_container_width=True):
            st.session_state.show_whatsapp_bot = True
            st.rerun()
        
        if st.button("📧 Open Email Scheduler", use_container_width=True):
            st.session_state.show_email_scheduler = True
            st.rerun()
    
    with col2:
        if st.button("💼 Open LinkedIn Automation", use_container_width=True):
            st.session_state.show_linkedin_automation = True
            st.rerun()
        
        if st.button("📸 Open Instagram Bot", use_container_width=True):
            st.session_state.show_instagram_bot = True
            st.rerun()
        
        if st.button("🤖 Open LLM Tools", use_container_width=True):
            st.session_state.show_llm_tools = True
            st.rerun()

def show_utility_tools():
    """Show utility tools section"""
    st.markdown('<h2 class="section-header">🧰 Utility Tools</h2>', unsafe_allow_html=True)
    
    # Tool selection
    tools = {
        "🛒 Grocery Manager": "grocery_manager",
        "📱 WhatsApp Bot": "whatsapp_bot",
        "📧 Email Scheduler": "email_scheduler",
        "💼 LinkedIn Automation": "linkedin_automation",
        "📸 Instagram Bot": "instagram_bot",
        "📱 SMS Sender": "sms_sender"
    }
    
    selected_tool = st.selectbox(
        "Choose a tool to run:",
        list(tools.keys())
    )
    
    # Run selected tool
    if tools[selected_tool] == "grocery_manager":
        run_grocery_manager()
    elif tools[selected_tool] == "whatsapp_bot":
        run_whatsapp_bot()
    elif tools[selected_tool] == "email_scheduler":
        run_email_scheduler()
    elif tools[selected_tool] == "linkedin_automation":
        run_linkedin_automation()
    elif tools[selected_tool] == "instagram_bot":
        run_instagram_bot()
    elif tools[selected_tool] == "sms_sender":
        run_sms_sender()

def show_linux_docker_commands():
    """Show Linux and Docker commands section"""
    st.markdown('<h2 class="section-header">💻 Linux & Docker Commands</h2>', unsafe_allow_html=True)
    
    # SSH Configuration
    with st.expander("🔐 SSH Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            hostname = st.text_input("Server IP/Hostname", placeholder="192.168.1.100")
            username = st.text_input("Username", placeholder="ubuntu")
        
        with col2:
            password = st.text_input("Password", type="password")
            port = st.number_input("SSH Port", value=22, min_value=1, max_value=65535)
    
    # Command categories
    tab1, tab2 = st.tabs(["🐧 Linux Commands", "🐳 Docker Commands"])
    
    with tab1:
        st.subheader("Linux System Commands")
        
        # Predefined Linux commands
        linux_commands = {
            "System Info": [
                "uname -a",
                "cat /etc/os-release",
                "df -h",
                "free -h",
                "top -n 1"
            ],
            "Network": [
                "ip addr show",
                "netstat -tuln",
                "ping -c 4 google.com",
                "curl -I https://google.com",
                "nslookup google.com"
            ],
            "Processes": [
                "ps aux",
                "ps aux | grep -i apache",
                "systemctl status",
                "systemctl list-units --type=service",
                "htop"
            ],
            "Files & Directories": [
                "ls -la /",
                "du -sh /*",
                "find / -name '*.log' -type f | head -10",
                "cat /var/log/syslog | tail -20",
                "ls -la /etc/"
            ],
            "Security": [
                "who",
                "last",
                "sudo cat /var/log/auth.log | tail -10",
                "netstat -tuln | grep LISTEN",
                "ss -tuln"
            ]
        }
        
        selected_category = st.selectbox("Select command category:", list(linux_commands.keys()))
        
        st.markdown(f"### {selected_category}")
        
        for i, cmd in enumerate(linux_commands[selected_category]):
            col1, col2 = st.columns([3, 1])
            col1.code(cmd)
            
            if col2.button(f"Run {i+1}", key=f"linux_{i}"):
                if hostname and username and password:
                    with st.spinner(f"Executing: {cmd}"):
                        success, output = run_remote_command(hostname, username, password, cmd)
                        
                        if success:
                            st.success("✅ Command executed successfully!")
                            st.code(output)
                        else:
                            st.error(f"❌ Command failed: {output}")
                else:
                    st.warning("Please configure SSH connection first")
    
    with tab2:
        st.subheader("Docker Commands")
        
        # Predefined Docker commands
        docker_commands = {
            "Container Management": [
                "docker ps -a",
                "docker images",
                "docker system df",
                "docker stats --no-stream",
                "docker version"
            ],
            "Container Operations": [
                "docker run -d nginx:latest",
                "docker stop $(docker ps -q)",
                "docker rm $(docker ps -aq)",
                "docker rmi $(docker images -q)",
                "docker container prune -f"
            ],
            "Docker Compose": [
                "docker-compose ps",
                "docker-compose up -d",
                "docker-compose down",
                "docker-compose logs",
                "docker-compose pull"
            ],
            "Docker System": [
                "docker system prune -f",
                "docker system info",
                "docker network ls",
                "docker volume ls",
                "docker info"
            ],
            "Docker Images": [
                "docker build -t myapp .",
                "docker push myapp:latest",
                "docker pull ubuntu:latest",
                "docker save myapp:latest > myapp.tar",
                "docker load < myapp.tar"
            ]
        }
        
        selected_docker_category = st.selectbox("Select Docker command category:", list(docker_commands.keys()), key="docker_cat")
        
        st.markdown(f"### {selected_docker_category}")
        
        for i, cmd in enumerate(docker_commands[selected_docker_category]):
            col1, col2 = st.columns([3, 1])
            col1.code(cmd)
            
            if col2.button(f"Run {i+1}", key=f"docker_{i}"):
                if hostname and username and password:
                    with st.spinner(f"Executing: {cmd}"):
                        success, output = run_remote_command(hostname, username, password, cmd)
                        
                        if success:
                            st.success("✅ Command executed successfully!")
                            st.code(output)
                        else:
                            st.error(f"❌ Command failed: {output}")
                else:
                    st.warning("Please configure SSH connection first")

def show_apache_launcher():
    """Show Apache launcher section"""
    st.markdown('<h2 class="section-header">🌐 Apache One-Click Launcher</h2>', unsafe_allow_html=True)
    
    st.info("🚀 Launch Apache web server on your remote machine with one click!")
    
    # SSH Configuration
    with st.expander("🔐 SSH Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            hostname = st.text_input("Server IP/Hostname", placeholder="192.168.1.100", key="apache_host")
            username = st.text_input("Username", placeholder="ubuntu", key="apache_user")
        
        with col2:
            password = st.text_input("Password", type="password", key="apache_pass")
            port = st.number_input("SSH Port", value=22, min_value=1, max_value=65535, key="apache_port")
    
    # Apache actions
    st.markdown("### 🚀 Apache Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🚀 Start Apache", type="primary", use_container_width=True):
            if hostname and username and password:
                with st.spinner("Starting Apache server..."):
                    success, message = start_apache_server(hostname, username, password)
                    
                    if success:
                        st.success("✅ Apache started successfully!")
                        st.info(message)
                    else:
                        st.error(f"❌ Failed to start Apache: {message}")
            else:
                st.warning("Please configure SSH connection first")
    
    with col2:
        if st.button("📊 Check Status", use_container_width=True):
            if hostname and username and password:
                with st.spinner("Checking Apache status..."):
                    success, output = run_remote_command(hostname, username, password, "systemctl status apache2")
                    
                    if success:
                        st.success("✅ Status retrieved!")
                        st.code(output)
                    else:
                        st.error(f"❌ Failed to get status: {output}")
            else:
                st.warning("Please configure SSH connection first")
    
    with col3:
        if st.button("🛑 Stop Apache", use_container_width=True):
            if hostname and username and password:
                with st.spinner("Stopping Apache server..."):
                    success, output = run_remote_command(hostname, username, password, "sudo systemctl stop apache2")
                    
                    if success:
                        st.success("✅ Apache stopped successfully!")
                    else:
                        st.error(f"❌ Failed to stop Apache: {output}")
            else:
                st.warning("Please configure SSH connection first")
    
    # Apache configuration
    st.markdown("### ⚙️ Apache Configuration")
    
    with st.expander("📝 Quick Configuration"):
        st.markdown("""
        **Common Apache Commands:**
        
        ```bash
        # Start Apache
        sudo systemctl start apache2
        
        # Stop Apache
        sudo systemctl stop apache2
        
        # Restart Apache
        sudo systemctl restart apache2
        
        # Check Status
        sudo systemctl status apache2
        
        # Enable Auto-start
        sudo systemctl enable apache2
        
        # View Logs
        sudo tail -f /var/log/apache2/access.log
        sudo tail -f /var/log/apache2/error.log
        ```
        """)

def show_llm_panel():
    """Show LLM tools panel"""
    st.markdown('<h2 class="section-header">🤖 LLMs Panel</h2>', unsafe_allow_html=True)
    
    # Run LLM tools
    run_llm_tools()

# Check for tool-specific sessions
if st.session_state.get("show_grocery_manager", False):
    st.session_state.show_grocery_manager = False
    run_grocery_manager()

elif st.session_state.get("show_whatsapp_bot", False):
    st.session_state.show_whatsapp_bot = False
    run_whatsapp_bot()

elif st.session_state.get("show_email_scheduler", False):
    st.session_state.show_email_scheduler = False
    run_email_scheduler()

elif st.session_state.get("show_linkedin_automation", False):
    st.session_state.show_linkedin_automation = False
    run_linkedin_automation()

elif st.session_state.get("show_instagram_bot", False):
    st.session_state.show_instagram_bot = False
    run_instagram_bot()

elif st.session_state.get("show_llm_tools", False):
    st.session_state.show_llm_tools = False
    run_llm_tools()

else:
    # Run main dashboard
    main()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🤖 Automation Tools Dashboard | Built with Streamlit</p>
    <p>Version 1.0 | © 2024</p>
</div>
""", unsafe_allow_html=True) 