"""
This module implements the GOAPPlanner class, which is responsible for generating plans
using the Goal-Oriented Action Planning (GOAP) approach. It calculates the optimal sequence
of actions to reach a specified goal state from a start state.
"""

import heapq
from typing import List, Dict, Tuple, Callable
from action import Action


class GOAPPlanner:
    def __init__(self, actions: List[Action], heuristic: Callable[[Dict[str, int], Dict[str, int], Dict], int]):
        """
        Initializes the GOAPPlanner with a list of possible actions and a heuristic function.

        Args:
            actions (List[Action]): A list of possible actions the agent can perform.
            heuristic (Callable[[Dict[str, int], Dict[str, int], Dict], int]):
                A heuristic function used to estimate the cost to reach the goal from a given state.
        """
        self.actions = actions
        self.heuristic = heuristic
        self.plan_requested = 0
        self.node_developed = 0
        self.action_tested = 0

    def plan(self, start_state: Dict[str, int], goal_state: Dict[str, int], context: Dict) -> Tuple[List[str], int]:
        """
        Generates a plan to reach the goal state from the start state using the GOAP approach.

        Args:
            start_state (Dict[str, int]): The initial state of the agent.
            goal_state (Dict[str, int]): The desired goal state.
            context (Dict): Additional context, including callbacks for state updates and environment information.

        Returns:
            Tuple[List[str], int]: A tuple containing the list of actions in the plan and the total cost of the plan.
        """
        self.plan_requested += 1
        frontier = []

        updated_start_state = start_state.copy()
        if "update_state_callback" in context:
            context["update_state_callback"](updated_start_state, context)

        heapq.heappush(frontier, (0, 0, self._state_to_tuple(updated_start_state), [], 0))

        explored = set()

        while frontier:
            self.node_developed += 1
            _, current_cost, current_state_tuple, plan, elapsed_time = heapq.heappop(frontier)
            current_state = dict(current_state_tuple)

            if all(current_state.get(k, 0) == v for k, v in goal_state.items()):
                return plan, current_cost

            if current_state_tuple in explored:
                continue
            explored.add(current_state_tuple)

            for action in self.actions:
                if action.is_applicable(current_state):
                    new_state = current_state.copy()
                    self.action_tested += 1
                    for k, v in action.effects.items():
                        new_state[k] = new_state.get(k, 0) + v

                    if "update_state_callback" in context:
                        context["update_state_callback"](new_state, context)

                    new_plan = plan + [action.name]
                    new_cost = current_cost + action.cost
                    new_elapsed_time = elapsed_time + action.duration

                    h = 0
                    if self.heuristic is not None:
                        h = self.heuristic(new_state, goal_state, context)

                    priority = new_cost + h
                    if priority == float('inf'):
                        raise Exception("infinite weight. Something is wrong")

                    heapq.heappush(frontier, (priority, new_cost, self._state_to_tuple(new_state), new_plan, new_elapsed_time))

        return [], float('inf')

    def display_usage_stats(self):
        """
        Display usage of the planner. We can see the number of plan requested. We see how many
        nodes are developed. These nodes are considered nodes of interest that should be
        explored. Finally, action tested are all the action we updated the stated and added
        to the list of potential nodes.
        """
        print("Plan Requested: ", self.plan_requested)
        print("Node Developed: ", self.node_developed)
        print("Action Tested: ", self.action_tested)

    @staticmethod
    def _state_to_tuple(state: Dict[str, int]) -> Tuple[Tuple[str, int], ...]:
        """
        Converts a state dictionary into a sorted tuple, ensuring consistent and hashable representation.

        Args:
            state (Dict[str, int]): The state dictionary to convert.

        Returns:
            Tuple[Tuple[str, int], ...]: A sorted tuple representation of the state.
        """
        return tuple(sorted(state.items()))
