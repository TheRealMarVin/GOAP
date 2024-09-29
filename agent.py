from typing import List, Dict
from action import Action
from event_manager import EventManager
from goap_planner import GOAPPlanner


class Agent:
    def __init__(self, actions: List[Action], planner: GOAPPlanner, event_manager: EventManager, verbose: bool = True):
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

    def execute_plan(self, initial_state: Dict[str, int], plan: List[str], context: Dict = None):
        if context is None:
            context = {}

        current_state = initial_state.copy()

        while plan:
            if self.verbose:
                print(f"Current State: {current_state}")
                print(f"Plan: {plan}")

            action_name = plan.pop(0)
            action = next((a for a in self.actions if a.name == action_name), None)

            if "update_state_callback" in context:
                context["update_state_callback"](current_state, context)

            if not action or not action.is_applicable(current_state):
                self.should_replan = True
                if self.verbose:
                    print(f"Preconditions for action {action_name} are not met. Replanning...")
                new_plan, _ = self.planner.plan(current_state, context.get("goal_state", {}), context)
                if not new_plan:
                    if self.verbose:
                        print("No valid plan could be found during replanning!")
                    return
                plan = new_plan
                continue

            if not action or not action.execute(current_state, on_interrupt=lambda: self.should_replan,
                                                verbose=self.verbose):
                self.should_replan = False

                if self.verbose:
                    print(f"Action {action_name} failed or interrupted. Replanning...")

                new_plan, _ = self.planner.plan(current_state, context.get("goal_state", {}), context)
                if not new_plan:
                    if self.verbose:
                        print("No valid plan could be found during replanning!")
                    return

                plan = new_plan
                continue

            if "post_action_callback" in context:
                context["post_action_callback"](action, current_state, context)

            if self.verbose:
                print(f"Updated state after action {action_name}: {current_state}")

            goal_state = context.get("goal_state", {})
            if all(current_state.get(k, 0) == v for k, v in goal_state.items()):
                if self.verbose:
                    print("Goal achieved!")
                break

        if self.verbose:
            print(f"Final State: {current_state}")
