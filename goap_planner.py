"""
This module implements the GOAPPlanner class, which is responsible for generating plans
using the Goal-Oriented Action Planning (GOAP) approach. It calculates the optimal sequence
of actions to reach a specified goal state from a start state.
"""

import heapq
from enum import Enum
from typing import List, Dict, Tuple, Union
from action import Action
from goal import Goal
from helpers import is_goal_satisfied


class PlanningMode(Enum):
    SEQUENTIAL = 1
    GLOBAL = 2

class PlanProgress:
    def __init__(self, current_cost: float, current_state_tuple: Dict, plan: List, elapsed_time: float):
        """
        Initializes the PlanProgress instance, representing the progress of a plan.

        Args:
            current_cost (float): The accumulated cost of actions in the plan.
            current_state_tuple (Dict): A hashable representation of the current state.
            plan (List): A list of actions taken so far.
            elapsed_time (float): The total time elapsed during the execution of the plan.
        """
        self.current_cost = current_cost
        self.current_state_tuple = current_state_tuple
        self.plan = plan
        self.elapsed_time = elapsed_time

    def __lt__(self, other):
        """
        Compares two PlanProgress instances for sorting, prioritizing lower cost,
        then lower elapsed time, and finally shorter plans.

        Args:
            other (PlanProgress): Another PlanProgress instance to compare.

        Returns:
            bool: True if this instance should come before the other in sorting order.
        """
        if self.current_cost != other.current_cost:
            return self.current_cost < other.current_cost

        if self.elapsed_time != other.elapsed_time:
            return self.elapsed_time < other.elapsed_time

        return len(self.plan) < len(other.plan)


class GOAPPlanner:
    def __init__(self, actions: List[Action], max_depth: int=20):
        """
        Initializes the GOAPPlanner with a list of possible actions.

        Args:
            actions (List[Action]): A list of possible actions the agent can perform.
            max_depth (int): Max possible depth for the planner to reach
        """
        self.actions = actions
        self.max_depth = max_depth
        self.plan_requested = 0
        self.node_developed = 0
        self.action_tested = 0

    def plan(self, start_state: Dict[str, int], goals: Union[List[Goal], Goal],
             context: Dict, mode: PlanningMode =PlanningMode.GLOBAL) -> Tuple[List[str], float]:
        """
        Generates a plan to reach one of the goal states from the start state using the GOAP approach.

        Args:
            start_state (Dict[str, int]): The initial state of the agent.
            goals (Union[List[Goal], Goal]): A list of goals, each containing a goal state and an associated heuristic function.
            context (Dict): Additional context, including callbacks for state updates and environment information.
            mode (PlanningMode): Type of planning mode to handle multi goals. Default Global mode.

        Returns:
            Tuple[List[str], float]: A tuple containing the list of actions in the plan and the total cost of the plan.
        """
        if goals is None:
            return [], float('inf')
        elif isinstance(goals, Goal):
            goals = [goals]

        self.plan_requested += 1
        if mode == PlanningMode.SEQUENTIAL:
            return self._plan_sequential(goals, start_state, context)

        return self._plan_global(goals, start_state, context)

    @staticmethod
    def _update_initial_state(initial_state, context):
        """
        Updates the initial state using a callback from the context, if provided.

        Args:
            initial_state (Dict): The initial state dictionary to update.
            context (Dict): Context dictionary containing callbacks for updates.

        Returns:
            Dict: The updated start state.
        """
        updated_start_state = initial_state.copy()
        if "update_state_callback" in context:
            context["update_state_callback"](updated_start_state, context)
        return updated_start_state

    def _plan_sequential(self, goals, initial_state, context):
        """
        Generates a plan by sequentially attempting to satisfy each goal in order. This
        is a special case where we want to process one goal after the other.

        Args:
            goals (List[Goal]): A list of goals with associated goal states and heuristics.
            initial_state (Dict): The starting state for the planner.
            context (Dict): Context dictionary for callbacks and additional information.

        Returns:
           Tuple[List[str], float]: A tuple containing the plan and its total cost.
        """
        for goal_info in goals:
            plan, cost = self._plan_global([goal_info], initial_state, context)
            if len(plan) > 0:
                return plan, cost

        return [], float('inf')

    def _plan_global(self, goals, initial_state, context):
        """
        Generates a global plan for the provided goals from the initial state.
        This will try to expand all the plans at the same time and return as
        soon as one plan is satisfied.

        Args:
            goals (List[Goal]): A list of goals with associated goal states and heuristics.
            initial_state (Dict): The starting state for the planner.
            context (Dict): Context dictionary for callbacks and additional information.

        Returns:
            Tuple[List[str], float]: A tuple containing the list of actions in the plan and the total cost.
        """
        updated_start_state = self._update_initial_state(initial_state, context)

        explored = set()
        frontier = []
        initial_progress = PlanProgress(0, self._state_to_tuple(updated_start_state), [], 0)
        heapq.heappush(frontier, (0, initial_progress))

        while frontier:
            self.node_developed += 1
            _, progress = heapq.heappop(frontier)
            if len(progress.plan) >= self.max_depth:
                continue

            current_state = dict(progress.current_state_tuple)

            if is_goal_satisfied(goals, current_state):
                return progress.plan, progress.current_cost

            if progress.current_state_tuple in explored:
                continue
            explored.add(progress.current_state_tuple)

            for action in self.actions:
                if action.is_applicable(current_state):
                    new_state = current_state.copy()
                    self.action_tested += 1
                    for k, v in action.effects.items():
                        new_state[k] = new_state.get(k, 0) + v

                    if "update_state_callback" in context:
                        context["update_state_callback"](new_state, context)

                    new_plan = progress.plan + [action.name]
                    new_cost = progress.current_cost + action.cost
                    new_elapsed_time = progress.elapsed_time + action.duration

                    for goal_info in goals:
                        h = 0
                        if goal_info.heuristic is not None:
                            h = goal_info.heuristic(new_state, goal_info.goal_state, context)

                        priority = new_cost + h
                        if priority == float('inf'):
                            raise Exception("infinite weight. Something is wrong")

                        new_progress = PlanProgress(new_cost, self._state_to_tuple(new_state), new_plan, new_elapsed_time)
                        heapq.heappush(frontier, (priority, new_progress))

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
