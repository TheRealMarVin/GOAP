from typing import List, Dict, Tuple
import heapq  # We'll use heapq for an efficient priority queue

from action import Action


class GOAPPlanner:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def plan(self, start_state: Dict[str, bool], goal_state: Dict[str, bool]) -> Tuple[List[str], int]:
        # Priority queue for frontier with (priority, current_cost, current_state, actions_taken, elapsed_time)
        frontier = []
        heapq.heappush(frontier, (0, 0, self._state_to_tuple(start_state), [], 0))  # (priority, cost, state_tuple, plan, elapsed_time)

        explored = set()  # To avoid revisiting states

        while frontier:
            _, current_cost, current_state_tuple, plan, elapsed_time = heapq.heappop(frontier)
            current_state = dict(current_state_tuple)  # Convert tuple back to dictionary

            # Check if the goal is met
            if all(current_state.get(k, False) == v for k, v in goal_state.items()):
                return plan, current_cost

            # Mark this state as explored
            if current_state_tuple in explored:
                continue
            explored.add(current_state_tuple)

            # Explore applicable actions
            for action in self.actions:
                if action.is_applicable(current_state):
                    new_state = current_state.copy()
                    new_state.update(action.effects)
                    new_plan = plan + [action.name]
                    new_cost = current_cost + action.cost
                    new_elapsed_time = elapsed_time + action.duration

                    # Calculate heuristic
                    h = self._heuristic(new_state, goal_state)
                    priority = new_cost + h

                    heapq.heappush(frontier, (priority, new_cost, self._state_to_tuple(new_state), new_plan, new_elapsed_time))

        return [], float('inf')  # No valid plan found

    @staticmethod
    def _heuristic(state: Dict[str, bool], goal: Dict[str, bool]) -> int:
        # Heuristic: count the number of unsatisfied goals
        return sum(1 for k, v in goal.items() if state.get(k) != v)

    @staticmethod
    def _state_to_tuple(state: Dict[str, bool]) -> Tuple[Tuple[str, bool], ...]:
        # Convert the state dictionary to a tuple of sorted key-value pairs
        return tuple(sorted(state.items()))
