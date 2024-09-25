from typing import List, Dict, Tuple
import heapq

from action import Action


class GOAPPlanner:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def plan(self, start_state: Dict[str, int], goal_state: Dict[str, int]) -> Tuple[List[str], int]:
        frontier = []
        heapq.heappush(frontier, (0, 0, self._state_to_tuple(start_state), [], 0))

        explored = set()

        while frontier:
            _, current_cost, current_state_tuple, plan, elapsed_time = heapq.heappop(frontier)
            current_state = dict(current_state_tuple)

            if all(current_state.get(k, 0) >= v for k, v in goal_state.items()):
                return plan, current_cost

            if current_state_tuple in explored:
                continue
            explored.add(current_state_tuple)

            for action in self.actions:
                if action.is_applicable(current_state):
                    new_state = current_state.copy()
                    for k, v in action.effects.items():
                        new_state[k] = new_state.get(k, 0) + v

                    new_plan = plan + [action.name]
                    new_cost = current_cost + action.cost
                    new_elapsed_time = elapsed_time + action.duration

                    h = self._heuristic(new_state, goal_state)
                    priority = new_cost + h

                    heapq.heappush(frontier, (priority, new_cost, self._state_to_tuple(new_state), new_plan, new_elapsed_time))

        return [], float('inf')

    @staticmethod
    def _heuristic(state: Dict[str, int], goal: Dict[str, int]) -> int:
        return sum(max(0, v - state.get(k, 0)) for k, v in goal.items())

    @staticmethod
    def _state_to_tuple(state: Dict[str, int]) -> Tuple[Tuple[str, int], ...]:
        return tuple(sorted(state.items()))
