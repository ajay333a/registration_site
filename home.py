import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Constants
EVENT_IMAGE_URL = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80"
EVENT_DETAILS = {
    "Date": "TBD",
    "Location": "Virtual Event",
    "Registration": "Required",
    "Capacity": "Limited"
}

def display_registration_steps():
    """Display registration steps in a clear format"""
    st.markdown("### How to Register")
    st.markdown("""
    Follow these detailed steps to complete your registration for the Moonlanding Event:
    """)
    
    steps = [
        {
            "title": "1. Start Registration",
            "description": "Click the 'Start Registration Process' button above or use the Registration link in the sidebar."
        },
        {
            "title": "2. Personal Information",
            "description": """
            Fill in your personal details:
            - Full Name (as it appears on your ID)
            - Email Address (for confirmation and updates)
            - Date of Birth, Country, City, State, Profession 
            """
        },
        {
            "title": "3. Email Verification",
            "description": """
            - You will receive a One-Time Password (OTP) at your registered email
            - Enter the OTP within 10 minutes
            - If you don't receive the OTP, check your spam folder or request a new one
            """
        },
        {
            "title": "4. Additional Information",
            "description": """
            Provide any additional required information:
            - Dietary Restrictions (if any)
            - Special Accommodations needed
            - Emergency Contact Details
            """
        },
        {
            "title": "5. Confirmation",
            "description": """
            - Review all entered information
            - Accept the terms and conditions
            - Submit your registration
            - You will receive a confirmation email with your registration ID
            """
        }
    ]
    
    for step in steps:
        st.markdown(f"#### {step['title']}")
        st.markdown(step['description'])
        st.markdown("---")

def handle_registration():
    """Handle the registration button click"""
    st.session_state.registration_clicked = True
    st.switch_page("pages/1_Registration.py")

def load_event_image():
    """Load and display the event image with error handling"""
    try:
        response = requests.get(EVENT_IMAGE_URL)
        image = Image.open(BytesIO(response.content))
        # Display image in a smaller size
        st.image(
            image,
            caption="Moonlanding Event - A Journey to the Stars",
            width=300,  # Control display width
            use_container_width=False  # Don't stretch to container width
        )
    except Exception as e:
        st.warning("Unable to load the event image. Please check your internet connection.")
        st.error(f"Error: {str(e)}")

def display_event_details():
    """Display event details in a structured format"""
    st.markdown("### Event Details")
    for key, value in EVENT_DETAILS.items():
        st.markdown(f"- **{key}**: {value}")


def display_guest_list_info():
    """Display information about viewing the guest list"""
    st.markdown("### View Guest List")
    features = [
        "Click on 'Guests List' in the sidebar to view all registered guests",
        "Use the search function to find specific guests",
        "Download the guest list as CSV if needed"
    ]
    for feature in features:
        st.markdown(f"- {feature}")

def main():
    # Page configuration
    st.set_page_config(
        page_title="Moonlanding Event",
        page_icon="🚀",
    )

    # Initialize session state for registration
    if 'registration_clicked' not in st.session_state:
        st.session_state.registration_clicked = False

    # Main title and description
    st.title("🚀 Welcome to Moonlanding Event")
    st.markdown("""
    ### Event Registration System

    This application helps manage registrations for the Moonlanding Event. You can:

    - 📝 Register new guests
    - 👥 View the list of registered guests
    - 🔍 Search through guest registrations

    Use the sidebar to navigate between different sections of the application.
    """)

    
    
    st.markdown("---")

    # Display registration steps first
    display_registration_steps()

    # Create two columns for button and image
    col1, col2 = st.columns([1, 2])  # 1:2 ratio for better layout
    
    with col1:
        st.markdown("### Ready to Register?")
        # Display registration button
        if st.button("🚀 Start Registration Process", use_container_width=True):
            handle_registration()
    
    with col2:
        # Load and display the event image
        load_event_image()

    # Display event information
    col1, col2 = st.columns(2)
    
    with col1:
        display_event_details()
    
    with col2:
        display_guest_list_info()
        
        # Add a contact section
        st.markdown("### Need Help?")
        st.markdown("""
        If you have any questions or need assistance, please:
        - Check our FAQ section
        - Contact our support team
        - Visit our help center
        """)

if __name__ == "__main__":
    main() 
    