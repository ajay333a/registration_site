import streamlit as st
import pandas as pd
import json
import os

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

def search_guests(query, guests):
    """Search guests by name or email"""
    query = query.lower()
    return [
        guest for guest in guests
        if query in guest['name'].lower() or query in guest['email'].lower()
    ]

# ---- Streamlit App ----
st.set_page_config(page_title="Guests List", page_icon="👥", layout="wide")
st.title("👥 Registered Guests List")

# Load guests data
guests = load_guests()

if not guests:
    st.info("No guests have registered yet.")
else:
    # Convert to DataFrame for better display
    df = pd.DataFrame(guests)
    
    # Add search functionality
    search_query = st.text_input("🔍 Search guests by name or email")
    
    if search_query:
        filtered_guests = search_guests(search_query, guests)
        if filtered_guests:
            df = pd.DataFrame(filtered_guests)
            st.write(f"Found {len(filtered_guests)} guests:")
        else:
            st.write("No guests found matching your search.")
    
    # Display the table
    if not df.empty:
        # Format the registration date
        df['registration_date'] = pd.to_datetime(df['registration_date'])
        df['registration_date'] = df['registration_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Rename columns for better display
        df = df.rename(columns={
            'name': 'Name',
            'email': 'Email',
            'date_of_birth': 'Date of Birth',
            'city': 'City',
            'state': 'State/Province',
            'country': 'Country',
            'profession': 'Profession',
            'registration_date': 'Registration Date'
        })
        
        # Display the table with custom styling
        st.dataframe(
            df,
            column_config={
                "Name": st.column_config.TextColumn(
                    "Name",
                    width="medium",
                    help="Full name of the registered guest"
                ),
                "Email": st.column_config.TextColumn(
                    "Email",
                    width="medium",
                    help="Email address of the registered guest"
                ),
                "Date of Birth": st.column_config.TextColumn(
                    "Date of Birth",
                    width="small",
                    help="Guest's date of birth"
                ),
                "City": st.column_config.TextColumn(
                    "City",
                    width="medium",
                    help="City of residence"
                ),
                "State/Province": st.column_config.TextColumn(
                    "State/Province",
                    width="medium",
                    help="State or province of residence"
                ),
                "Country": st.column_config.TextColumn(
                    "Country",
                    width="medium",
                    help="Country of residence"
                ),
                "Profession": st.column_config.TextColumn(
                    "Profession",
                    width="medium",
                    help="Guest's profession"
                ),
                "Registration Date": st.column_config.TextColumn(
                    "Registration Date",
                    width="medium",
                    help="Date and time of registration"
                ),
            },
            hide_index=True,
            use_container_width=True,  # Make table use full container width
            height=400  # Set a fixed height with scroll
        )
        
        # Add download button for the guest list
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download Guest List as CSV",
            data=csv,
            file_name="guest_list.csv",
            mime="text/csv",
            use_container_width=True  # Make button use full width
        ) 