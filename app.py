import time

import streamlit as st

from randselect.selector import available_choices, random_selection

FLASH_SECONDS = 3
FLASH_INTERVAL = 0.1

st.title("Random Name & Question Picker")

for key, default in (
    ("names", []),
    ("questions", []),
    ("used_names", set()),
    ("used_questions", set()),
    ("last_pick", None),
):
    st.session_state.setdefault(key, default)

col_names, col_questions = st.columns(2)

with col_names:
    st.subheader("Names")
    with st.form("add_name", clear_on_submit=True):
        new_name = st.text_input("Add a name")
        if st.form_submit_button("Add") and new_name.strip():
            st.session_state.names.append(new_name.strip())
    for name in st.session_state.names:
        st.write(f"- {name}")

with col_questions:
    st.subheader("Questions")
    with st.form("add_question", clear_on_submit=True):
        new_question = st.text_input("Add a question")
        if st.form_submit_button("Add") and new_question.strip():
            st.session_state.questions.append(new_question.strip())
    for question in st.session_state.questions:
        st.write(f"- {question}")

st.divider()

no_repeats = st.checkbox("No repeats this session")

result_placeholder = st.empty()
if st.session_state.last_pick:
    name, question = st.session_state.last_pick
    result_placeholder.markdown(f"### {name}, please answer: {question}")

if st.button("Draw"):
    if not st.session_state.names or not st.session_state.questions:
        st.warning("Add at least one name and one question first.")
    else:
        candidate_names = st.session_state.names
        candidate_questions = st.session_state.questions
        if no_repeats:
            candidate_names = available_choices(
                st.session_state.names, st.session_state.used_names
            )
            candidate_questions = available_choices(
                st.session_state.questions, st.session_state.used_questions
            )

        if no_repeats and (not candidate_names or not candidate_questions):
            st.warning(
                "All combinations used - uncheck 'no repeats' or add more names/questions."
            )
        else:
            end_time = time.time() + FLASH_SECONDS
            while time.time() < end_time:
                flash_name, flash_question = random_selection(
                    st.session_state.names, st.session_state.questions
                )
                result_placeholder.markdown(f"### {flash_name}: {flash_question}")
                time.sleep(FLASH_INTERVAL)

            chosen_name, chosen_question = random_selection(
                candidate_names, candidate_questions
            )
            result_placeholder.markdown(
                f"### {chosen_name}, please answer: {chosen_question}"
            )
            st.session_state.last_pick = (chosen_name, chosen_question)
            st.session_state.used_names.add(chosen_name)
            st.session_state.used_questions.add(chosen_question)
