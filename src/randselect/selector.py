import random

def random_selection(n_list, q_list, rng=random, used_names=(), used_questions=()):
  """Pick one name and one question, skipping anything in used_names / used_questions.

  Raises ValueError if no candidates remain.
  """
  names = [n for n in n_list if n not in used_names]
  qs = [q for q in q_list if q not in used_questions]
  if not names or not qs:
    raise ValueError("No names or questions left to choose from.")

  chosen_name = rng.choice(names)
  chosen_question = rng.choice(qs)

  return (chosen_name, chosen_question)
