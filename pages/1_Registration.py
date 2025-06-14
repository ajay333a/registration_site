import re
import random
import smtplib
import os
import json
from datetime import datetime
from email.mime.text import MIMEText
import streamlit as st
import base64

# Load environment variables from Streamlit secrets
EMAIL_USER = st.secrets["EMAIL_USER"]
EMAIL_PASS = st.secrets["EMAIL_PASS"]

# Constants
GUESTS_FILE = 'registered_guests.json'

def load_guests():
    """Load registered guests from JSON file"""
    if os.path.exists(GUESTS_FILE):
        try:
            with open(GUESTS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_guest(name, email, dob, city, state, country, profession):
    """Save a new guest to the JSON file"""
    guests = load_guests()
    
    # Check if guest already exists
    for guest in guests:
        if guest['email'].lower() == email.lower():
            st.error("This email is already registered. Please use a different email address.")
            return False
            
    guest_data = {
        'name': name,
        'email': email,
        'date_of_birth': dob,
        'city': city,
        'state': state,
        'country': country,
        'profession': profession,
        'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    guests.append(guest_data)
    with open(GUESTS_FILE, 'w') as f:
        json.dump(guests, f, indent=4)
    return True

def search_guests(query):
    """Search guests by name or email"""
    guests = load_guests()
    query = query.lower()
    return [
        guest for guest in guests
        if query in guest['name'].lower() or query in guest['email'].lower()
    ]

def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def generate_otp(length=6):
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def send_otp_email(receiver_email, otp):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    sender_email = EMAIL_USER.strip('"')
    sender_password = EMAIL_PASS.strip('"')
    
    # Validate email credentials
    if not sender_email or not sender_password:
        st.error("Email configuration is missing. Please check your environment variables.")
        return False
        
    subject = 'Your OTP Code'
    body = f'Your OTP code is: {otp}'
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'Moonlanding Org'
    msg['To'] = receiver_email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except smtplib.SMTPAuthenticationError:
        st.error("Email authentication failed. Please check your email credentials.")
        return False
    except smtplib.SMTPException as e:
        st.error(f"Failed to send email: {str(e)}")
        return False
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return False
    return True

def reset_session_state():
    """Reset all session state variables to their initial values"""
    st.session_state.step = 'register'
    st.session_state.otp = ''
    st.session_state.email = ''
    st.session_state.name = ''
    st.session_state.dob = ''
    st.session_state.city = ''
    st.session_state.state = ''
    st.session_state.country = ''
    st.session_state.profession = ''
    st.session_state.attempts = 0
    st.session_state.otp_sent_time = None

# ---- Streamlit App ----
st.set_page_config(page_title="Moonlanding Event Registration", page_icon="🚀")
st.title("🚀 Moonlanding Event Registration")

# --- State Initialization ---
if 'step' not in st.session_state:
    st.session_state.step = 'register'
if 'otp' not in st.session_state:
    st.session_state.otp = ''
if 'email' not in st.session_state:
    st.session_state.email = ''
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'dob' not in st.session_state:
    st.session_state.dob = ''
if 'city' not in st.session_state:
    st.session_state.city = ''
if 'state' not in st.session_state:
    st.session_state.state = ''
if 'country' not in st.session_state:
    st.session_state.country = ''
if 'profession' not in st.session_state:
    st.session_state.profession = ''
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'otp_sent_time' not in st.session_state:
    st.session_state.otp_sent_time = None

if st.session_state.step == 'register':
    with st.form("register_form", clear_on_submit=False):
        st.subheader("Fill the required fields")
        name = st.text_input("Full Name *", value=st.session_state.name, key="name_input")
        email = st.text_input("Email *", value=st.session_state.email, key="email_input")
        
        # Add new fields
        col1, col2 = st.columns(2)
        with col1:
            dob = st.date_input(
                "Date of Birth *",
                value=None,
                min_value=datetime(1990, 1, 1),
                max_value=datetime(2015, 12, 31),
                format="YYYY-MM-DD",
                key="dob_input"
            )
            city = st.text_input("City", value=st.session_state.city, key="city_input")
            state = st.text_input("State/Province", value=st.session_state.state, key="state_input")
        with col2:
            country = st.text_input("Country *", value=st.session_state.country, key="country_input")
            profession = st.text_input("Profession *", value=st.session_state.profession, key="profession_input")
        
        submitted = st.form_submit_button("Register & Send OTP", use_container_width=True)
        if submitted:
            if not name.strip():
                st.warning("Please enter your name.")
            elif not is_valid_email(email):
                st.warning("Invalid email address. Enter a valid email.")
            elif not dob:
                st.warning("Please enter your date of birth.")
            elif not city.strip():
                st.warning("Please enter your city.")
            elif not state.strip():
                st.warning("Please enter your state/province.")
            elif not country.strip():
                st.warning("Please enter your country.")
            elif not profession.strip():
                st.warning("Please enter your profession.")
            else:
                otp = generate_otp()
                if send_otp_email(email, otp):
                    st.session_state.otp = otp
                    st.session_state.email = email
                    st.session_state.name = name
                    st.session_state.dob = dob.strftime('%Y-%m-%d')
                    st.session_state.city = city
                    st.session_state.state = state
                    st.session_state.country = country
                    st.session_state.profession = profession
                    st.session_state.attempts = 0
                    st.session_state.step = 'otp'
                    st.success(f"OTP sent to {email}. Please check your inbox.")
                else:
                    st.error("Failed to send OTP. Please try again.")

if st.session_state.step == 'otp':
    with st.form("otp_form", clear_on_submit=False):
        st.write(f"Enter the OTP sent to {st.session_state.email}")
        otp_input = st.text_input("OTP", type="password", key="otp_input")
        submitted = st.form_submit_button("Verify OTP", use_container_width=True)
        if submitted:
            st.session_state.attempts += 1
            if otp_input == st.session_state.otp:
                st.session_state.step = 'done'
                st.success("Email verified and registration complete!")
            elif st.session_state.attempts >= 3:
                st.error("Verification failed. Maximum attempts reached. Please register again.")
                reset_session_state()
            else:
                st.error(f"Invalid OTP. Attempts left: {3 - st.session_state.attempts}")
                # Generate new OTP after failed attempt
                new_otp = generate_otp()
                if send_otp_email(st.session_state.email, new_otp):
                    st.session_state.otp = new_otp
                    st.success("A new OTP has been sent to your email.")
                else:
                    st.error("Failed to send new OTP. Please try registering again.")
                    reset_session_state()

if st.session_state.step == 'done':
    st.snow()
    st.write(f"Thank you, {st.session_state.name}! You are registered for the Moonlanding event.")
    st.write(f"A confirmation has been sent to: {st.session_state.email}")
    
    # Save the guest data and handle the result
    if save_guest(
        st.session_state.name,
        st.session_state.email,
        st.session_state.dob,
        st.session_state.city,
        st.session_state.state,
        st.session_state.country,
        st.session_state.profession
    ):
        st.success("Registration completed successfully!")
    else:
        st.error("Registration failed. Please try again with a different email address.")
        reset_session_state()
    
    if st.button("Register Another Guest"):
        reset_session_state()

# Add note about guest list
st.markdown("---")
st.info("""
### 👥 View Registered Guests
To view the complete list of registered guests, please visit the **Guests List** page using the sidebar navigation.
There you can:
- View all registered guests
- Search for specific guests
- Download the guest list as CSV
""")

