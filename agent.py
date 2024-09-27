from typing import List, Dict
from action import Action
from event_manager import EventManager
from goap_planner import GOAPPlanner


class Agent:
    def __init__(self, actions: List[Action], planner: GOAPPlanner, event_manager: EventManager, verbose: bool):
        self.actions = actions
        self.planner = planner
        self.event_manager = event_manager
        self.should_replan = False
        self.verbose = verbose
        self.event_manager.subscribe(self.on_event)

    def on_event(self):
        if self.verbose:
            print("Event detected! Replanning required.")
        self.should_replan = True

    def execute_plan(self, initial_state: Dict[str, int], goal_state: Dict[str, int], context: Dict = None):
        if context is None:
            context = {}

        current_state = initial_state.copy()

        while True:
            if "update_state_callback" in context:
                context["update_state_callback"](current_state, context)

            plan, total_cost = self.planner.plan(current_state, goal_state, context)

            if not plan:
                if self.verbose:
                    print("No valid plan could be found!")
                break

            if self.verbose:
                print(f"Current State: {current_state}")
                print(f"Plan: {plan}")

            for action_name in plan:
                action = next(a for a in self.actions if a.name == action_name)

                if not action.execute(current_state, on_interrupt=lambda: self.should_replan, verbose=self.verbose):
                    self.should_replan = False
                    break

                if "post_action_callback" in context:
                    context["post_action_callback"](action, current_state, context)

                if self.verbose:
                    print(f"Updated state after action {action_name}: {current_state}")

            if all(current_state.get(k, 0) >= v for k, v in goal_state.items()):
                if self.verbose:
                    print("Goal achieved!")
                break

        if self.verbose:
            print(f"Final State: {current_state}")
