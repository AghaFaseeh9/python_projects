import streamlit as st
import random
import time

questions = [
    {
        "question": "What is the capital of Australia?",
        "options": ["Sydney", "Melbourne", "Canberra", "Brisbane"],
        "answer": "Canberra",
    },
    {
        "question": "Which data structure uses FIFO (First In, First Out) principle?",
        "options": ["Stack", "Queue", "Array", "Tree"],
        "answer": "Queue",
    },
    {
        "question": "What is the chemical symbol for Gold?",
        "options": ["Gd", "Au", "Ag", "Go"],
        "answer": "Au",
    },
    {
        "question": "Who is known as the father of the computer?",
        "options": ["Alan Turing", "Charles Babbage", "Bill Gates", "Steve Jobs"],
        "answer": "Charles Babbage",
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Mars", "Jupiter", "Venus", "Saturn"],
        "answer": "Mars",
    },
]


if "current_question" not in st.session_state:
    st.session_state.current_question = random.choice(questions)

question = st.session_state.current_question

st.subheader(question["question"])
selected_option = st.radio("Choose your answer", question["options"], key="answer")
if st.button("Submit Answer"):
    if selected_option == question["answer"]:
        st.success("Congratulation your answer is correct!")
    else:
        st.error(
            f"Your answer is incorrect and the correct answer is {question['answer']}"
        )

    time.sleep(3)
    st.session_state.current_question = random.choice(questions)
    st.rerun()
