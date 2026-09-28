import time

import streamlit as st

from randselect.selector import random_selection

st.title("Random Selector")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "last_pick" not in st.session_state:
    st.session_state.last_pick = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("Roster")
    with st.form("add_name_form", clear_on_submit=True):
        name_input = st.text_input("Name")
        if st.form_submit_button("Add") and name_input.strip():
            st.session_state.names.append(name_input.strip())
    if st.session_state.names:
        st.write("\n".join(f"- {n}" for n in st.session_state.names))
    else:
        st.caption("No names added yet.")

with col2:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        question_input = st.text_input("Question")
        if st.form_submit_button("Add") and question_input.strip():
            st.session_state.questions.append(question_input.strip())
    if st.session_state.questions:
        st.write("\n".join(f"- {q}" for q in st.session_state.questions))
    else:
        st.caption("No questions added yet.")

st.divider()

no_repeats = st.checkbox("No repeats (this session)", key="no_repeats")

names_exhausted = (
    no_repeats
    and bool(st.session_state.names)
    and set(st.session_state.names) <= st.session_state.used_names
)
questions_exhausted = (
    no_repeats
    and bool(st.session_state.questions)
    and set(st.session_state.questions) <= st.session_state.used_questions
)

if names_exhausted:
    st.warning("All names are selected!")
if questions_exhausted:
    st.warning("All questions are selected!")

draw_disabled = (
    not st.session_state.names
    or not st.session_state.questions
    or names_exhausted
    or questions_exhausted
)

if st.button("Draw", disabled=draw_disabled):
    placeholder = st.empty()

    for _ in range(15):
        flash_name, flash_question = random_selection(
            st.session_state.names, st.session_state.questions
        )
        placeholder.write(f"{flash_name} — {flash_question}")
        time.sleep(0.2)

    chosen_name, chosen_question = random_selection(
        st.session_state.names,
        st.session_state.questions,
        exclude_names=st.session_state.used_names if no_repeats else (),
        exclude_questions=st.session_state.used_questions if no_repeats else (),
    )

    st.session_state.used_names.add(chosen_name)
    st.session_state.used_questions.add(chosen_question)
    st.session_state.last_pick = (chosen_name, chosen_question)

    placeholder.success(f"{chosen_name}, please answer: {chosen_question}")
elif st.session_state.last_pick:
    chosen_name, chosen_question = st.session_state.last_pick
    st.success(f"{chosen_name}, please answer: {chosen_question}")
