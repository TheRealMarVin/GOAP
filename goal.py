from typing import Callable, Dict


class Goal:
    def __init__(self, goal_state:Dict[str, int], heuristic: Callable[[Dict[str, int], Dict[str, int], Dict], int]):
        """
            Initializes the GOAP goal with a goal state and a heuristic function.

            Args:
                goal_state (Dict[str, int]): The desired goal state(s).
                heuristic (Callable[[Dict[str, int], Dict[str, int], Dict], int]):
                    A heuristic function used to estimate the cost to reach the goal from a given state.
        """
        self.goal_state = goal_state
        self.heuristic = heuristic

    def is_goal_achieved(self, current_state):
        goal_achieved = all(current_state.get(k, 0) == v for k, v in self.goal_state.items())
        return goal_achieved
