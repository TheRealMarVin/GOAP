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
        """
            Checks if the goal state has been achieved given the current state.

            Args:
                current_state (Dict): The current state of the agent as a dictionary where keys are state variables
                                      and values are their respective values.

            Returns:
                bool: True if all conditions in the goal state match a goal, False otherwise.
            """
        goal_achieved = all(current_state.get(k, 0) == v for k, v in self.goal_state.items())
        return goal_achieved
