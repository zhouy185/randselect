import time

import streamlit as st

from randselect.selector import random_selection

st.title("Random Selector")

for key, default in [
    ("names", []),
    ("questions", []),
    ("drawn_names", set()),
    ("drawn_questions", set()),
    ("last_result", None),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def _add(list_key, input_key):
    text = st.session_state[input_key].strip()
    if text and text not in st.session_state[list_key]:
        st.session_state[list_key].append(text)
    st.session_state[input_key] = ""


st.subheader("Names")
st.text_input("Add a name", key="name_input")
st.button("Add name", on_click=_add, args=("names", "name_input"))
st.write(st.session_state.names or "No names added yet.")

st.subheader("Questions")
st.text_input("Add a question", key="question_input")
st.button("Add question", on_click=_add, args=("questions", "question_input"))
st.write(st.session_state.questions or "No questions added yet.")

st.subheader("Draw")
no_repeats = st.checkbox("No repeats this session", key="no_repeats")

eligible_names = (
    [n for n in st.session_state.names if n not in st.session_state.drawn_names]
    if no_repeats
    else st.session_state.names
)
eligible_questions = (
    [q for q in st.session_state.questions if q not in st.session_state.drawn_questions]
    if no_repeats
    else st.session_state.questions
)

can_draw = bool(eligible_names) and bool(eligible_questions)

if not st.session_state.names or not st.session_state.questions:
    st.info("Add at least one name and one question to draw.")
elif not can_draw:
    exhausted = []
    if not eligible_names:
        exhausted.append("names")
    if not eligible_questions:
        exhausted.append("questions")
    st.warning(
        f"All {' and '.join(exhausted)} have been drawn. Add more, "
        "or uncheck 'No repeats' to allow repeats."
    )

placeholder = st.empty()

if st.button("Draw", disabled=not can_draw):
    end_time = time.time() + 3.0
    while time.time() < end_time:
        flash_name, flash_question = random_selection(
            st.session_state.names, st.session_state.questions
        )
        placeholder.markdown(f"### {flash_name} — {flash_question}")
        time.sleep(0.08)

    chosen_name, chosen_question = random_selection(eligible_names, eligible_questions)

    st.session_state.last_result = (chosen_name, chosen_question)
    if no_repeats:
        st.session_state.drawn_names.add(chosen_name)
        st.session_state.drawn_questions.add(chosen_question)

if st.session_state.last_result:
    chosen_name, chosen_question = st.session_state.last_result
    placeholder.markdown(f"## {chosen_name}, please answer: {chosen_question}")
else:
    placeholder.info("No draw yet.")
