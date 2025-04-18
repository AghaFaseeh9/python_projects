import streamlit as st
import random
import string


def generate_password(length, use_digits, use_special):
    characters = string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special:
        characters += string.punctuation
    return "".join(random.choice(characters) for _ in range(length))


st.title("Password Generator")
length = st.slider(
    "Select the length of the password", min_value=6, max_value=32, value=18
)
use_digits = st.checkbox("Select if you want to use digits in your password")
use_special = st.checkbox(
    "Select if you want to use special character in your password"
)
if st.button("Generte password"):
    password = generate_password(length, use_digits, use_special)
    st.success(f"Password Generated successfully : {password}")
