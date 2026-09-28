import time

import streamlit as st

from randselect.selector import random_selection, random_selection_excluding

ANIMATION_SECONDS = 3
FRAME_SECONDS = 0.1

st.title("Random Question Picker")

defaults = {
    "names": [],
    "questions": [],
    "used_names": set(),
    "used_questions": set(),
    "result": None,
    "animate": False,
    "exhausted": False,
    "draw_error": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def add_entry_form(label, list_key, used_key):
    # Form submit only mutates state; the list is rendered below from state.
    with st.form(f"add_{list_key}", clear_on_submit=True):
        entry = st.text_input(label)
        submitted = st.form_submit_button("Add")
    if submitted:
        entry = entry.strip()
        if entry in st.session_state[list_key]:
            st.warning(f"'{entry}' is already in the list.")
        elif entry:
            st.session_state[list_key].append(entry)

    if st.button("Clear", key=f"clear_{list_key}"):
        st.session_state[list_key] = []
        st.session_state[used_key] = set()

    items = st.session_state[list_key]
    if items:
        st.markdown("\n".join(f"{i}. {item}" for i, item in enumerate(items, 1)))
    else:
        st.caption("Nothing added yet.")


col_names, col_questions = st.columns(2)
with col_names:
    st.subheader("Roster")
    add_entry_form("Name", "names", "used_names")
with col_questions:
    st.subheader("Questions")
    add_entry_form("Question", "questions", "used_questions")

st.divider()

no_repeats = st.checkbox("No repeats", value=False, key="no_repeats")

if st.button("Draw", type="primary"):
    st.session_state.exhausted = False
    st.session_state.draw_error = False
    names = st.session_state.names
    questions = st.session_state.questions
    if not names or not questions:
        st.session_state.draw_error = True
    elif no_repeats:
        pick = random_selection_excluding(
            names,
            questions,
            st.session_state.used_names,
            st.session_state.used_questions,
        )
        if pick is None:
            st.session_state.exhausted = True
        else:
            st.session_state.result = pick
            st.session_state.used_names.add(pick[0])
            st.session_state.used_questions.add(pick[1])
            st.session_state.animate = True
    else:
        st.session_state.result = random_selection(names, questions)
        st.session_state.animate = True

if st.session_state.exhausted and st.button("Reset draws"):
    st.session_state.used_names = set()
    st.session_state.used_questions = set()
    st.session_state.exhausted = False

# Rendering: reads state on every rerun so the result survives other interactions.
if st.session_state.draw_error:
    st.error("Add at least one name and one question before drawing.")

if st.session_state.exhausted:
    st.info("Every name or question has been used this session. Reset to draw again.")

placeholder = st.empty()

if st.session_state.animate and st.session_state.names and st.session_state.questions:
    end = time.monotonic() + ANIMATION_SECONDS
    while time.monotonic() < end:
        name, question = random_selection(
            st.session_state.names, st.session_state.questions
        )
        placeholder.markdown(f"### {name}\n\n{question}")
        time.sleep(FRAME_SECONDS)
st.session_state.animate = False

if st.session_state.result:
    name, question = st.session_state.result
    placeholder.success(f"### {name}, please answer:\n\n{question}")
