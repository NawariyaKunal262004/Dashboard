import streamlit as st
from datetime import datetime
import time

def run_sms_sender():
    """Run the SMS sender tool"""
    st.markdown("## 📱 SMS Sender")
    
    st.info("📞 This is a simulated SMS sender interface. In a real implementation, you would integrate with SMS services like Twilio, AWS SNS, etc.")
    
    # Initialize session state
    if 'sms_history' not in st.session_state:
        st.session_state.sms_history = []
    
    # SMS configuration
    with st.expander("⚙️ SMS Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            sender_name = st.text_input("Sender Name", value="YourApp")
            api_key = st.text_input("API Key", type="password", placeholder="Enter your SMS API key")
            service_provider = st.selectbox("Service Provider", ["Twilio", "AWS SNS", "Vonage", "Custom"])
        
        with col2:
            default_country_code = st.selectbox("Default Country Code", ["+1", "+44", "+91", "+86", "+81", "+49"])
            delivery_reports = st.checkbox("Enable Delivery Reports", value=True)
            retry_failed = st.checkbox("Retry Failed Messages", value=True)
    
    # Contact management
    st.markdown("### 👥 Contact Management")
    
    contacts = st.session_state.get('sms_contacts', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Add Contact")
        new_contact_name = st.text_input("Contact Name")
        new_contact_number = st.text_input("Phone Number", placeholder="+1234567890")
        new_contact_group = st.selectbox("Group", ["Family", "Friends", "Work", "Other"])
        
        if st.button("Add Contact") and new_contact_name and new_contact_number:
            contacts.append({
                "name": new_contact_name,
                "number": new_contact_number,
                "group": new_contact_group
            })
            st.session_state.sms_contacts = contacts
            st.success(f"Added {new_contact_name} to contacts!")
            st.rerun()
    
    with col2:
        st.markdown("#### Contact List")
        if contacts:
            for contact in contacts:
                st.write(f"📞 **{contact['name']}** - {contact['number']} ({contact['group']})")
        else:
            st.info("No contacts added yet.")
    
    # Send SMS
    st.markdown("### 📤 Send SMS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Single recipient
        st.markdown("#### Send to Single Recipient")
        
        if contacts:
            recipient = st.selectbox("Select Recipient", [contact['name'] for contact in contacts])
        else:
            recipient = st.text_input("Recipient Name")
        
        phone_number = st.text_input("Phone Number", placeholder="+1234567890")
        message_content = st.text_area("Message Content", height=150)
        
        # Message options
        col1, col2 = st.columns(2)
        with col1:
            priority = st.selectbox("Priority", ["Normal", "High", "Urgent"])
        with col2:
            schedule_send = st.checkbox("Schedule Send")
        
        if schedule_send:
            schedule_date = st.date_input("Schedule Date", min_value=datetime.now().date())
            schedule_time = st.time_input("Schedule Time", value=datetime.now().time())
        
        if st.button("📤 Send SMS", type="primary"):
            if phone_number and message_content:
                # Simulate sending
                with st.spinner("Sending SMS..."):
                    time.sleep(1)
                    
                    new_sms = {
                        "id": len(st.session_state.sms_history) + 1,
                        "recipient": recipient if recipient else "Unknown",
                        "number": phone_number,
                        "content": message_content,
                        "status": "Sent",
                        "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "priority": priority
                    }
                    
                    st.session_state.sms_history.append(new_sms)
                    st.success("SMS sent successfully!")
                    st.rerun()
            else:
                st.error("Please fill in all required fields!")
    
    with col2:
        # Bulk SMS
        st.markdown("#### Send Bulk SMS")
        
        bulk_recipients = st.multiselect("Select Recipients", 
                                       [contact['name'] for contact in contacts] if contacts else [])
        
        bulk_message = st.text_area("Bulk Message Content", height=150)
        
        # Bulk options
        col1, col2 = st.columns(2)
        with col1:
            bulk_priority = st.selectbox("Priority", ["Normal", "High", "Urgent"], key="bulk_priority")
        with col2:
            delay_between_messages = st.slider("Delay (seconds)", 1, 10, 2)
        
        if st.button("📤 Send Bulk SMS", disabled=not bulk_recipients or not bulk_message):
            if bulk_recipients and bulk_message:
                with st.spinner(f"Sending {len(bulk_recipients)} messages..."):
                    for i, recipient in enumerate(bulk_recipients):
                        time.sleep(0.5)  # Simulate delay
                        
                        new_sms = {
                            "id": len(st.session_state.sms_history) + 1 + i,
                            "recipient": recipient,
                            "number": "Bulk SMS",
                            "content": bulk_message,
                            "status": "Sent",
                            "sent_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "priority": bulk_priority
                        }
                        
                        st.session_state.sms_history.append(new_sms)
                    
                    st.success(f"Bulk SMS sent to {len(bulk_recipients)} recipients!")
                    st.rerun()
    
    # Message templates
    st.markdown("### 📝 Message Templates")
    
    templates = {
        "Appointment Reminder": "Hi [Name], this is a reminder about your appointment on [Date] at [Time]. Please confirm your attendance.",
        "Meeting Notification": "Hi [Name], you have a meeting scheduled for [Date] at [Time]. Location: [Location]",
        "Birthday Wish": "Happy Birthday [Name]! 🎉 Wishing you a wonderful day filled with joy and happiness!",
        "Custom": ""
    }
    
    selected_template = st.selectbox("Select Template", list(templates.keys()))
    
    if selected_template == "Custom":
        custom_template = st.text_area("Custom Template")
    else:
        custom_template = templates[selected_template]
        st.text_area("Template Preview", custom_template, disabled=True)
    
    if st.button("📝 Use Template"):
        st.session_state.selected_template = custom_template
        st.rerun()
    
    # SMS history
    st.markdown("### 📋 SMS History")
    
    if not st.session_state.sms_history:
        st.info("No SMS messages sent yet.")
    else:
        for sms in reversed(st.session_state.sms_history[-10:]):  # Show last 10 messages
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                
                with col1:
                    st.write(f"**{sms['recipient']}** ({sms['number']})")
                    st.caption(sms['content'][:50] + "..." if len(sms['content']) > 50 else sms['content'])
                
                with col2:
                    st.write(f"📅 {sms['sent_time']}")
                
                with col3:
                    priority_color = {"Normal": "🟢", "High": "🟡", "Urgent": "🔴"}
                    st.write(f"{priority_color[sms['priority']]} {sms['priority']}")
                
                with col4:
                    status_color = {"Sent": "✅", "Failed": "❌", "Pending": "⏳"}
                    st.write(f"{status_color[sms['status']]} {sms['status']}")
                
                st.divider()
    
    # Statistics
    st.markdown("### 📊 Statistics")
    
    total_sent = len(st.session_state.sms_history)
    successful_sends = len([sms for sms in st.session_state.sms_history if sms['status'] == 'Sent'])
    failed_sends = total_sent - successful_sends
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Sent", total_sent)
    
    with col2:
        st.metric("Successful", successful_sends)
    
    with col3:
        st.metric("Failed", failed_sends)
    
    with col4:
        success_rate = (successful_sends / total_sent * 100) if total_sent > 0 else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")
