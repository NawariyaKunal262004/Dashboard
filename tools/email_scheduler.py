import streamlit as st
from datetime import datetime, timedelta
import time

def run_email_scheduler():
    """Run the email scheduler tool"""
    st.markdown("## 📧 Email Scheduler")
    
    st.info("📅 This is a simulated email scheduler interface. In a real implementation, you would integrate with email services like Gmail API, SMTP, etc.")
    
    # Initialize session state
    if 'scheduled_emails' not in st.session_state:
        st.session_state.scheduled_emails = []
    
    # Email composition
    with st.expander("✍️ Compose Email", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            recipient = st.text_input("To (Email)")
            subject = st.text_input("Subject")
        
        with col2:
            schedule_date = st.date_input("Schedule Date", min_value=datetime.now().date())
            schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
        
        message_body = st.text_area("Message Body", height=200)
        
        # Email options
        col1, col2, col3 = st.columns(3)
        with col1:
            priority = st.selectbox("Priority", ["Normal", "High", "Urgent"])
        with col2:
            repeat = st.selectbox("Repeat", ["Never", "Daily", "Weekly", "Monthly"])
        with col3:
            attachments = st.file_uploader("Attachments", accept_multiple_files=True)
        
        if st.button("📅 Schedule Email", type="primary"):
            if recipient and subject and message_body:
                scheduled_datetime = datetime.combine(schedule_date, schedule_time)
                
                new_email = {
                    "id": len(st.session_state.scheduled_emails) + 1,
                    "recipient": recipient,
                    "subject": subject,
                    "body": message_body,
                    "scheduled_time": scheduled_datetime.strftime("%Y-%m-%d %H:%M"),
                    "priority": priority,
                    "repeat": repeat,
                    "status": "Scheduled",
                    "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.session_state.scheduled_emails.append(new_email)
                st.success(f"Email scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}!")
                st.rerun()
            else:
                st.error("Please fill in all required fields!")
    
    # Scheduled emails list
    st.markdown("### 📋 Scheduled Emails")
    
    if not st.session_state.scheduled_emails:
        st.info("No emails scheduled yet.")
    else:
        for email in st.session_state.scheduled_emails:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"**{email['subject']}**")
                    st.caption(f"To: {email['recipient']}")
                    st.caption(f"Scheduled: {email['scheduled_time']}")
                
                with col2:
                    priority_color = {"Normal": "🟢", "High": "🟡", "Urgent": "🔴"}
                    st.write(f"{priority_color[email['priority']]} {email['priority']}")
                
                with col3:
                    st.write(f"🔄 {email['repeat']}")
                
                with col4:
                    if st.button("❌", key=f"delete_{email['id']}"):
                        st.session_state.scheduled_emails = [e for e in st.session_state.scheduled_emails if e['id'] != email['id']]
                        st.rerun()
                
                st.divider()
    
    # Email templates
    st.markdown("### 📝 Email Templates")
    
    templates = {
        "Meeting Reminder": {
            "subject": "Meeting Reminder - [Topic]",
            "body": "Hi [Name],\n\nThis is a reminder about our meeting scheduled for [Date] at [Time].\n\nAgenda:\n- [Agenda item 1]\n- [Agenda item 2]\n\nPlease let me know if you need to reschedule.\n\nBest regards,\n[Your name]"
        },
        "Follow-up": {
            "subject": "Follow-up - [Previous discussion]",
            "body": "Hi [Name],\n\nI hope this email finds you well. I wanted to follow up on our previous discussion about [topic].\n\n[Additional context or questions]\n\nLooking forward to hearing from you.\n\nBest regards,\n[Your name]"
        },
        "Thank You": {
            "subject": "Thank You - [Event/Meeting]",
            "body": "Hi [Name],\n\nThank you for [event/meeting/opportunity]. I really appreciate [specific detail].\n\n[Additional comments]\n\nBest regards,\n[Your name]"
        }
    }
    
    selected_template = st.selectbox("Select Template", list(templates.keys()))
    
    if selected_template:
        template = templates[selected_template]
        st.text_area("Template Subject", template["subject"], disabled=True)
        st.text_area("Template Body", template["body"], height=150, disabled=True)
        
        if st.button("Use Template"):
            st.session_state.email_template = template
            st.rerun()
    
    # Statistics
    st.markdown("### 📊 Statistics")
    
    total_scheduled = len(st.session_state.scheduled_emails)
    pending_emails = len([e for e in st.session_state.scheduled_emails if e['status'] == 'Scheduled'])
    sent_emails = len([e for e in st.session_state.scheduled_emails if e['status'] == 'Sent'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Scheduled", total_scheduled)
    
    with col2:
        st.metric("Pending", pending_emails)
    
    with col3:
        st.metric("Sent", sent_emails)
