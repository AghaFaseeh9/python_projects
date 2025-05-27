import streamlit as st
import hashlib
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get encryption key from environment variable or generate new one
KEY = os.getenv('ENCRYPTION_KEY')
if not KEY:
    KEY = Fernet.generate_key()
    print("Warning: Using generated key. For production, set ENCRYPTION_KEY environment variable.")
cipher = Fernet(KEY)

# Get master password from environment variable
MASTER_PASSWORD = os.getenv('MASTER_PASSWORD', 'admin123')  # Default for development only

# Initialize session state for security
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "authorized" not in st.session_state:
    st.session_state.authorized = True

# In-memory data store (in production, use a proper database)
stored_data = {}

# Hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt
def encrypt_data(text):
    return cipher.encrypt(text.encode()).decode()

# Decrypt
def decrypt_data(encrypted_text, passkey):
    try:
        hashed_passkey = hash_passkey(passkey)
        for key, value in stored_data.items():
            if key == encrypted_text and value["passkey"] == hashed_passkey:
                st.session_state.failed_attempts = 0
                return cipher.decrypt(encrypted_text.encode()).decode()
        st.session_state.failed_attempts += 1
        return None
    except Exception as e:
        st.error(f"Decryption error: {str(e)}")
        return None

# Streamlit UI
st.set_page_config(
    page_title="Secure Data Encryption System",
    page_icon="🔒",
    layout="wide"
)

st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Use this app to **securely store and retrieve data** with a unique passkey.")
    st.write("### Features:")
    st.write("• 🔐 Secure encryption using Fernet (symmetric encryption)")
    st.write("• 🔑 Password-protected data storage")
    st.write("• 🔒 Master password protection")
    st.write("• ⚠️ Limited login attempts")

elif choice == "Store Data":
    st.subheader("📂 Store Data")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            try:
                encrypted_text = encrypt_data(user_data)
                stored_data[encrypted_text] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hash_passkey(passkey)
                }
                st.success("✅ Data stored securely!")
                st.write("🔐 Encrypted Data (save this!):")
                st.code(encrypted_text)
            except Exception as e:
                st.error(f"Error during encryption: {str(e)}")
        else:
            st.error("⚠️ Please enter both data and passkey.")

elif choice == "Retrieve Data":
    if not st.session_state.authorized:
        st.warning("🔒 You must log in first.")
        st.experimental_rerun()

    st.subheader("🔍 Retrieve Data")
    encrypted_text = st.text_area("Enter Encrypted Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Decrypt"):
        if encrypted_text and passkey:
            result = decrypt_data(encrypted_text, passkey)
            if result:
                st.success("✅ Decrypted Data:")
                st.write(result)
            else:
                remaining = 3 - st.session_state.failed_attempts
                st.error(f"❌ Incorrect passkey! Attempts remaining: {remaining}")
                if st.session_state.failed_attempts >= 3:
                    st.warning("🔐 Too many failed attempts! Redirecting to Login.")
                    st.session_state.authorized = False
                    st.experimental_rerun()
        else:
            st.error("⚠️ Please enter both fields.")

elif choice == "Login":
    st.subheader("🔑 Login Page")
    password = st.text_input("Enter Master Password:", type="password")

    if st.button("Login"):
        if password == MASTER_PASSWORD:
            st.session_state.failed_attempts = 0
            st.session_state.authorized = True
            st.success("✅ Reauthorized successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")
