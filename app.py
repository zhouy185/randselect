import random
import time

import streamlit as st

from randselect.selector import random_selection

FLASH_SECONDS = 3.0
FLASH_INTERVAL = 0.1

st.title("Random Question Picker")

state = st.session_state
state.setdefault("names", [])
state.setdefault("questions", [])
state.setdefault("used_names", [])
state.setdefault("used_questions", [])
state.setdefault("last_pick", None)
state.setdefault("rng", random.Random())


def add_item(label, key, items):
    with st.form(f"add_{key}", clear_on_submit=True):
        value = st.text_input(label)
        if st.form_submit_button("Add"):
            value = value.strip()
            if not value:
                st.warning("Enter something first.")
            elif value in items:
                st.warning(f"'{value}' is already in the list.")
            else:
                items.append(value)


col_names, col_questions = st.columns(2)
with col_names:
    st.subheader("Roster")
    add_item("Name", "name", state.names)
    for n in state.names:
        st.write(f"- {n}")
with col_questions:
    st.subheader("Questions")
    add_item("Question", "question", state.questions)
    for q in state.questions:
        st.write(f"- {q}")

st.divider()

no_repeats = st.checkbox("No repeats")
used_names = state.used_names if no_repeats else ()
used_questions = state.used_questions if no_repeats else ()

display = st.empty()

if st.button("Draw", type="primary"):
    try:
        # Validate a pick is possible before animating.
        random_selection(state.names, state.questions, state.rng, used_names, used_questions)
    except ValueError:
        if no_repeats and state.names and state.questions:
            st.error("Everyone (or every question) has been used. Untick 'No repeats' or add more.")
        else:
            st.error("Add at least one name and one question first.")
    else:
        end = time.monotonic() + FLASH_SECONDS
        while time.monotonic() < end:
            name, question = random_selection(state.names, state.questions, state.rng)
            display.markdown(f"### {name}\n{question}")
            time.sleep(FLASH_INTERVAL)

        name, question = random_selection(
            state.names, state.questions, state.rng, used_names, used_questions
        )
        state.used_names.append(name)
        state.used_questions.append(question)
        state.last_pick = (name, question)

if state.last_pick:
    name, question = state.last_pick
    display.success(f"**{name}**, please answer: {question}")
