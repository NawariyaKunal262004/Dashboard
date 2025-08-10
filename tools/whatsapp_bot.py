import streamlit as st
import time
from datetime import datetime

def run_whatsapp_bot():
    """Run the WhatsApp bot tool"""
    st.markdown("## 📱 WhatsApp Bot")
    
    st.info("🤖 This is a simulated WhatsApp bot interface. In a real implementation, you would integrate with WhatsApp Web API or similar services.")
    
    # Bot configuration
    with st.expander("⚙️ Bot Configuration", expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            auto_reply = st.checkbox("Enable Auto-Reply", value=False)
            reply_message = st.text_area("Auto-Reply Message", 
                                        value="Thanks for your message! I'll get back to you soon.",
                                        disabled=not auto_reply)
        
        with col2:
            working_hours = st.slider("Working Hours", 0, 24, (9, 17))
            timezone = st.selectbox("Timezone", ["UTC", "EST", "PST", "IST", "GMT"])
    
    # Message templates
    st.markdown("### 📝 Message Templates")
    
    templates = {
        "Greeting": "Hello! How can I help you today?",
        "Busy": "I'm currently busy. I'll respond as soon as possible.",
        "Out of Office": "I'm out of office until [date]. I'll respond when I return.",
        "Meeting": "I'm in a meeting right now. I'll call you back later.",
        "Custom": ""
    }
    
    selected_template = st.selectbox("Select Template", list(templates.keys()))
    
    if selected_template == "Custom":
        custom_message = st.text_area("Custom Message")
    else:
        custom_message = templates[selected_template]
        st.text_area("Message Preview", custom_message, disabled=True)
    
    # Contact management
    st.markdown("### 👥 Contact Management")
    
    contacts = st.session_state.get('whatsapp_contacts', [])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Add Contact")
        new_contact = st.text_input("Contact Name")
        new_number = st.text_input("Phone Number")
        
        if st.button("Add Contact") and new_contact and new_number:
            contacts.append({"name": new_contact, "number": new_number})
            st.session_state.whatsapp_contacts = contacts
            st.success(f"Added {new_contact} to contacts!")
            st.rerun()
    
    with col2:
        st.markdown("#### Contact List")
        if contacts:
            for contact in contacts:
                st.write(f"📞 **{contact['name']}** - {contact['number']}")
        else:
            st.info("No contacts added yet.")
    
    # Message history
    st.markdown("### 💬 Message History")
    
    messages = st.session_state.get('whatsapp_messages', [])
    
    if messages:
        for message in reversed(messages[-10:]):  # Show last 10 messages
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col1:
                    st.write(f"**{message['sender']}**")
                    st.caption(message['time'])
                with col2:
                    st.write(message['content'])
                st.divider()
    else:
        st.info("No messages in history.")
    
    # Send message
    st.markdown("### 📤 Send Message")
    
    recipient = st.selectbox("Select Recipient", [contact['name'] for contact in contacts] if contacts else ["No contacts"])
    message_content = st.text_area("Message Content")
    
    if st.button("Send Message", disabled=not contacts or not message_content):
        if contacts and message_content:
            new_message = {
                "sender": "You",
                "recipient": recipient,
                "content": message_content,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "type": "sent"
            }
            messages.append(new_message)
            st.session_state.whatsapp_messages = messages
            st.success("Message sent!")
            st.rerun()
    
    # Bot status
    st.markdown("### 🤖 Bot Status")
    
    status_col1, status_col2, status_col3 = st.columns(3)
    
    with status_col1:
        st.metric("Total Contacts", len(contacts))
    
    with status_col2:
        st.metric("Total Messages", len(messages))
    
    with status_col3:
        status = "🟢 Online" if auto_reply else "🔴 Offline"
        st.metric("Bot Status", status)
