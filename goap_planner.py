import heapq

from typing import List, Dict, Tuple, Callable
from action import Action


class GOAPPlanner:
    def __init__(self, actions: List[Action], heuristic: Callable[[Dict[str, int], Dict[str, int], Dict], int]):
        self.actions = actions
        self.heuristic = heuristic

    def plan(self, start_state: Dict[str, int], goal_state: Dict[str, int], context: Dict) -> Tuple[List[str], int]:
        frontier = []
        heapq.heappush(frontier, (0, 0, self._state_to_tuple(start_state), [], 0))

        explored = set()

        while frontier:
            _, current_cost, current_state_tuple, plan, elapsed_time = heapq.heappop(frontier)
            # print(plan, current_state_tuple)
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

                    # Apply the state update callback if provided in the context
                    if "update_state_callback" in context:
                        context["update_state_callback"](new_state, context)

                    new_plan = plan + [action.name]
                    new_cost = current_cost + action.cost
                    new_elapsed_time = elapsed_time + action.duration

                    h = self.heuristic(new_state, goal_state, context)
                    priority = new_cost + h

                    heapq.heappush(frontier, (priority, new_cost, self._state_to_tuple(new_state), new_plan, new_elapsed_time))

        return [], float('inf')

    @staticmethod
    def _state_to_tuple(state: Dict[str, int]) -> Tuple[Tuple[str, int], ...]:
        return tuple(sorted(state.items()))
