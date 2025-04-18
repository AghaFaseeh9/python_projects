import streamlit as st
import random
import time
import requests


def generate_money():
    return random.randint(100, 1000)


st.title(
    "Money Maaking Machine",
)
st.subheader("Instant Cash Generator")
if st.button("Generate Money"):
    st.write("Counting Your Money....")
    time.sleep(5)
    amount = generate_money()
    st.success(f"You Made ${amount}")


def get_side_hustle():
    try:
        response = requests.get("http://127.0.0.1:8000/side_hustles")
        if response.status_code == 200:
            hustle = response.json()
            return hustle["side_hustle"]
        else:
            return "Freelancing"

    except:
        return "Something wents wrong!"


st.subheader("Side Hustle Ideas")
if st.button("Generate Hastle"):
    Idea = get_side_hustle()
    st.success(f"{Idea}")


def get_money_quotes():
    try:
        response = requests.get("http://127.0.0.1:8000/money_quotes")
        if response.status_code == 200:
            hustle = response.json()
            return hustle["money_quotes"]
        else:
            return "Money is buy to happiness"

    except:
        return "Something wents wrong"


st.subheader("Money Quotes")
if st.button("Generate Quote"):
    quotes = get_money_quotes()
    st.success(f"{quotes}")
