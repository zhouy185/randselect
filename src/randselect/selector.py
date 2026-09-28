import random

def random_selection(n_list, q_list, rng=None):
  rng = rng or random

  chosen_name = rng.choice(n_list)
  chosen_question = rng.choice(q_list)

  return (chosen_name, chosen_question)

def available_choices(items, used):
  return [item for item in items if item not in used]