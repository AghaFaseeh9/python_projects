# Secure Data Encryption System

A secure web application for storing and retrieving encrypted data using Streamlit.

## Setup Instructions

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run main.py
```

## Deployment

To deploy this application:

1. Make sure all dependencies are installed using `requirements.txt`
2. The application can be deployed on any platform that supports Streamlit apps (e.g., Streamlit Cloud, Heroku, etc.)
3. For production deployment, make sure to:
   - Change the default master password in the login section
   - Store the encryption key securely
   - Use environment variables for sensitive data

## Security Notes

- The current implementation uses a simple master password ("admin123") - change this in production
- The encryption key is generated at runtime - consider storing it securely in production
- Failed login attempts are limited to 3 tries 