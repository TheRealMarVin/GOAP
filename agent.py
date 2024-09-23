from typing import List, Dict, Tuple

from action import Action
from event_manager import EventManager
from goap_planner import GOAPPlanner


class Agent:
    def __init__(self, actions: List[Action], planner: GOAPPlanner, event_manager: EventManager):
        self.actions = actions
        self.planner = planner
        self.event_manager = event_manager
        self.should_replan = False
        self.event_manager.subscribe(self.on_event)  # Listen for events

    def on_event(self):
        print("Event detected! Replanning required.")
        self.should_replan = True

    def execute_plan(self, initial_state: Dict[str, bool], goal_state: Dict[str, bool]):
        current_state = initial_state.copy()

        while True:
            plan, total_cost = self.planner.plan(current_state, goal_state)

            if not plan:
                print("No valid plan could be found!")
                break

            print(f"Current State: {current_state}")
            print(f"Plan: {plan}")

            for action_name in plan:
                action = next(a for a in self.actions if a.name == action_name)

                if not action.is_applicable(current_state):
                    print(f"Action {action_name} is no longer applicable. Re-planning...")
                    break

                if not action.execute(current_state, on_interrupt=lambda: self.should_replan):
                    self.should_replan = False
                    break

            if all(current_state.get(k, False) == v for k, v in goal_state.items()):
                print("Goal achieved!")
                break

        print(f"Final State: {current_state}")