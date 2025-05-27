import streamlit as st

try:
    from cryptography.fernet import Fernet
except ImportError:
    st.error("Failed to import required cryptography module.")
    st.stop()

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = {}
if "key" not in st.session_state:
    st.session_state.key = Fernet.generate_key()
    st.session_state.cipher = Fernet(st.session_state.key)

# Simple encryption function
def encrypt(text):
    try:
        return st.session_state.cipher.encrypt(text.encode()).decode()
    except:
        return None

# Simple decryption function
def decrypt(text):
    try:
        return st.session_state.cipher.decrypt(text.encode()).decode()
    except:
        return None

# Main UI
st.title("🔒 Secure Data Encryption")

# Input
text = st.text_area("Enter text to encrypt/decrypt:")
password = st.text_input("Enter password:", type="password")

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Encrypt"):
        if text and password:
            encrypted = encrypt(text)
            if encrypted:
                st.session_state.data[encrypted] = password
                st.success("Encrypted successfully!")
                st.code(encrypted)
            else:
                st.error("Encryption failed")
        else:
            st.error("Please enter both text and password")

with col2:
    if st.button("Decrypt"):
        if text and password:
            if text in st.session_state.data and st.session_state.data[text] == password:
                decrypted = decrypt(text)
                if decrypted:
                    st.success("Decrypted successfully!")
                    st.write(decrypted)
                else:
                    st.error("Decryption failed")
            else:
                st.error("Invalid password or encrypted text")
        else:
            st.error("Please enter both encrypted text and password")
