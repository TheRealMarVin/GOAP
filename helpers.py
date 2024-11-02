from goal import Goal


def is_goal_satisfied(goals, current_state):
    """
    Determines if any of the specified goals are satisfied in the current state.

    Args:
        goals (Union[Goal, List[Goal]]): A single goal or a list of goals to check against the current state.
        current_state (Dict): The current state of the agent as a dictionary where keys are state variables
                              and values are their respective values.

    Returns:
        bool: True if at least one goal is achieved in the current state, False otherwise.
    """
    if goals is not None:
        if isinstance(goals, Goal):
            goals = [goals]

        for goal in goals:
            if goal.is_goal_achieved(current_state):
                return True

    return False
