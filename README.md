# 🤖 Automation Tools Dashboard

A comprehensive Streamlit-based dashboard for automation tools, SSH management, and AI capabilities.

## 🚀 Features

### 🧰 Utility Tools
- **🛒 Grocery Manager**: Manage your shopping lists with categories and priorities
- **📱 WhatsApp Bot**: Simulated WhatsApp automation interface
- **📧 Email Scheduler**: Schedule and manage email campaigns
- **💼 LinkedIn Automation**: LinkedIn networking and content automation
- **📸 Instagram Bot**: Instagram engagement and content automation
- **📱 SMS Sender**: Send SMS messages and manage contacts

### 💻 Linux & Docker Commands
- Execute remote Linux commands via SSH
- Docker container and image management
- System monitoring and administration
- Network and security commands

### 🌐 Apache Launcher
- One-click Apache server management
- Start, stop, and monitor Apache services
- Configuration management

### 🤖 LLMs Panel
- Chat interface with multiple AI models
- Text generation and analysis
- Code generation capabilities
- Integration with GPT-4, Claude-3, Gemini Pro, and Llama 2

## 📦 Installation

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 🔧 Dependencies

- `streamlit>=1.28.0`: Web application framework
- `paramiko>=3.3.1`: SSH client library (optional, for SSH functionality)

## 🎯 Usage

1. **Start the app**: Run `streamlit run app.py`
2. **Navigate**: Use the sidebar to switch between different sections
3. **Configure**: Set up SSH connections for remote server management
4. **Use tools**: Each tool has its own interface and functionality

## 📁 Project Structure

```
10_aug/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── tools/                # Tool modules
    ├── __init__.py
    ├── ssh_utils.py      # SSH functionality
    ├── grocery_manager.py
    ├── whatsapp_bot.py
    ├── email_scheduler.py
    ├── linkedin_automation.py
    ├── instagram_bot.py
    ├── sms_sender.py
    └── llm_tools.py
```

## ⚠️ Important Notes

- **SSH Functionality**: Requires `paramiko` library for SSH connections
- **Simulated Features**: Some tools (WhatsApp, Instagram, etc.) are simulated interfaces
- **API Keys**: Real implementations would require API keys for external services
- **Security**: Always use secure credentials and follow best practices

## 🛠️ Customization

Each tool module can be customized by:
1. Modifying the respective `.py` file in the `tools/` directory
2. Adding new tools by creating new modules
3. Updating the main `app.py` to include new tools

## 📞 Support

For issues or questions:
1. Check the console output for error messages
2. Ensure all dependencies are installed
3. Verify SSH credentials if using remote functionality

## 🔄 Updates

- Version 1.0: Initial release with basic automation tools
- Future updates will include more advanced features and integrations
