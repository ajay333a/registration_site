# Moonlanding Event Registration System 🚀

A modern, secure, and user-friendly event registration system built with Streamlit, featuring automated OTP verification and comprehensive guest management.

## Overview

The Moonlanding Event Registration System is a full-featured web application designed to streamline the event registration process. It provides a secure, efficient, and user-friendly interface for managing event registrations with features like email verification, guest list management, and data export capabilities.

## Key Features

### 1. Secure Registration Process
- **Email Verification**: Implements OTP (One-Time Password) verification
- **Data Validation**: Ensures all required fields are properly filled
- **Duplicate Prevention**: Prevents multiple registrations with the same email
- **Age Verification**: Date of birth validation (1990-2015)

### 2. Comprehensive Guest Information
- Full Name
- Email Address
- Date of Birth
- Location Details (City, State, Country)
- Professional Information
- Registration Timestamp

### 3. Guest Management
- **Search Functionality**: Search guests by name or email
- **Guest List View**: Organized display of all registered guests
- **Data Export**: Download guest list as CSV
- **Real-time Updates**: Instant reflection of new registrations

### 4. User Interface
- **Responsive Design**: Adapts to different screen sizes
- **Intuitive Navigation**: Easy-to-use sidebar menu
- **Clear Instructions**: Step-by-step registration guide
- **Visual Feedback**: Success/error messages for all actions

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Data Storage**: JSON
- **Email Service**: SMTP (Gmail)
- **Version Control**: Git/GitHub

## Setup and Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ajay333a/registration_site.git
   ```

2. Install required packages:
   ```bash
   pip install streamlit pandas python-dotenv pillow requests
   ```

3. Configure environment variables:
   - For local development:
     - Create a `.streamlit/secrets.toml` file in your project directory
     - Add your email credentials:
       ```toml
       EMAIL_USER = "your_email@gmail.com"
       EMAIL_PASS = "your_app_password"
       ```
   - For Streamlit Cloud deployment:
     - Go to your app settings in Streamlit Cloud
     - Add the same secrets in the "Secrets" section

4. Run the application:
   ```bash
   streamlit run home.py
   ```

## Security Features

- **OTP Verification**: Ensures email ownership
- **Secure Storage**: Sensitive data handling through Streamlit secrets
- **Input Validation**: Prevents malicious input
- **Session Management**: Secure user sessions

## Usage

1. **Registration**:
   - Fill in personal details
   - Verify email with OTP
   - Receive confirmation

2. **Guest Management**:
   - View all registered guests
   - Search for specific guests
   - Export guest list

3. **Administration**:
   - Monitor registrations
   - Manage guest data
   - Export reports

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For support or queries, please contact the development team.

---

Built with ❤️ for the Moonlanding Event
