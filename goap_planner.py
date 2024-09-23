from typing import List, Dict, Tuple

from action import Action


class GOAPPlanner:
    def __init__(self, actions: List[Action]):
        self.actions = actions

    def plan(self, start_state: Dict[str, bool], goal_state: Dict[str, bool]) -> Tuple[List[str], int]:
        frontier = [(start_state, [], 0)]  # (current_state, actions_taken, current_cost)

        while frontier:
            frontier.sort(key=lambda x: x[2])
            current_state, plan, cost = frontier.pop(0)

            if all(current_state.get(k, False) == v for k, v in goal_state.items()):
                return plan, cost

            for action in self.actions:
                if action.is_applicable(current_state):
                    new_state = current_state.copy()
                    new_state.update(action.effects)
                    new_plan = plan + [action.name]
                    new_cost = cost + action.cost
                    frontier.append((new_state, new_plan, new_cost))

        return [], float('inf')
