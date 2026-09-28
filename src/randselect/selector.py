import random

def random_selection(n_list, q_list, rng=random):

  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name, chosen_question)


def random_selection_excluding(n_list, q_list, used_names, used_questions, rng=random):
  # Returns None when either pool has no unused entries left.
  remaining_names = [n for n in n_list if n not in used_names]
  remaining_questions = [q for q in q_list if q not in used_questions]

  if not remaining_names or not remaining_questions:
    return None

  return random_selection(remaining_names, remaining_questions, rng)
