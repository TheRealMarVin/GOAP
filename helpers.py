from goal import Goal


def is_goal_satisfied(goals, current_state):
    if goals is not None:
        if isinstance(goals, Goal):
            goals = [goals]

        for goal in goals:
            if goal.is_goal_achieved(current_state):
                return True

    return False
