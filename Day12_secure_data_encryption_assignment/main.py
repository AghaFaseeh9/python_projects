import streamlit as st
import hashlib
from pathlib import Path

try:
    from cryptography.fernet import Fernet
except ImportError:
    st.error("Failed to import required cryptography module. Please check the logs for details.")
    st.stop()

# Initialize session state for security
if "failed_attempts" not in st.session_state:
    st.session_state.failed_attempts = 0
if "authorized" not in st.session_state:
    st.session_state.authorized = True
if "cipher" not in st.session_state:
    try:
        # Try to load existing key or generate new one
        key_file = Path("encryption_key.key")
        if key_file.exists():
            with open(key_file, "rb") as f:
                KEY = f.read()
        else:
            KEY = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(KEY)
        st.session_state.cipher = Fernet(KEY)
    except Exception as e:
        st.error("Failed to initialize encryption system. Please check the logs for details.")
        st.stop()

# In-memory data store
if "stored_data" not in st.session_state:
    st.session_state.stored_data = {}

# Hash passkey
def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

# Encrypt
def encrypt_data(text):
    try:
        return st.session_state.cipher.encrypt(text.encode()).decode()
    except Exception:
        st.error("Failed to encrypt data. Please try again.")
        return None

# Decrypt
def decrypt_data(encrypted_text, passkey):
    try:
        hashed_passkey = hash_passkey(passkey)
        for key, value in st.session_state.stored_data.items():
            if key == encrypted_text and value["passkey"] == hashed_passkey:
                st.session_state.failed_attempts = 0
                return st.session_state.cipher.decrypt(encrypted_text.encode()).decode()
        st.session_state.failed_attempts += 1
        return None
    except Exception:
        st.error("Failed to decrypt data. Please check your input and try again.")
        return None

# Streamlit UI
st.title("🔒 Secure Data Encryption System")

menu = ["Home", "Store Data", "Retrieve Data", "Login"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "Home":
    st.subheader("🏠 Welcome")
    st.write("Use this app to **securely store and retrieve data** with a unique passkey.")

elif choice == "Store Data":
    st.subheader("📂 Store Data")
    user_data = st.text_area("Enter Data:")
    passkey = st.text_input("Enter Passkey:", type="password")

    if st.button("Encrypt & Save"):
        if user_data and passkey:
            encrypted_text = encrypt_data(user_data)
            if encrypted_text:
                st.session_state.stored_data[encrypted_text] = {
                    "encrypted_text": encrypted_text,
                    "passkey": hash_passkey(passkey)
                }
                st.success("✅ Data stored securely!")
                st.write("🔐 Encrypted Data (save this!):")
                st.code(encrypted_text)
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
                st.success(f"✅ Decrypted Data: {result}")
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
        if password == "admin123":  # Replace with secure auth
            st.session_state.failed_attempts = 0
            st.session_state.authorized = True
            st.success("✅ Reauthorized successfully!")
            st.experimental_rerun()
        else:
            st.error("❌ Incorrect password!")
