"""
This script sets up and runs a cooking experiment using the GOAP (Goal-Oriented Action Planning) system.
It allows the user to run the experiment in two modes: 'plan' (generates and displays the plan)
and 'execute' (executes the plan with dynamic updates via an event thread).
"""

import argparse
import threading
import time
from action import Action
from agent import Agent
from event_manager import EventManager
from goap_planner import GOAPPlanner

actions = [
    Action("Gather Wood", {"wood": 0}, {"wood": 5}, duration=1, cost=1),
    Action("Light Fire", {"wood": 3}, {"fire": 1}, duration=1, cost=1),
    Action("Cook Food", {"fire": 1}, {"cooked_food": 1}, duration=2, cost=2),
]


def main(mode, use_heuristic):
    """
    Main function to handle the cooking experiment based on the selected mode.

    Args:
        mode (str): The mode to run ('plan' to generate and display the plan, 'execute' to run the plan with dynamic events).
        use_heuristic (str): 'enabled' to enable the use of heuristic to generate the plan, 'disabled' to not use it.
    """
    initial_state = {"wood": 0, "fire": 0, "cooked_food": 0}
    goal_state = {"cooked_food": 1}

    heuristic = None
    if use_heuristic == "enabled":
        heuristic = lambda state, goal, context: sum(abs(state.get(k, 0) - v) for k, v in goal.items())
    planner = GOAPPlanner(actions, heuristic=heuristic)

    plan, total_cost = planner.plan(initial_state, goal_state, {})

    if mode == "plan":
        print(f"Generated Plan: {plan} with total cost: {total_cost}")
        return

    event_manager = EventManager()

    def event_thread():
        """
        Simulates dynamic events by periodically publishing events through the event manager.
        """
        while True:
            time.sleep(5)
            event_manager.publish_event()

    agent = Agent(actions, planner, event_manager, verbose=True)

    event_thread_obj = threading.Thread(target=event_thread, daemon=True)
    event_thread_obj.start()

    agent.execute_plan(initial_state, plan, {"goal_state": goal_state})
    planner.display_usage_stats()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cooking Experiment")
    parser.add_argument("--mode", choices=["plan", "execute"], default="plan",
                        help="Choose whether to plan or execute the experiment")
    parser.add_argument("--heuristic", choices=["enabled", "disabled"], default="enabled",
                        help="Choose whether to enable heuristic or not.")
    args = parser.parse_args()

    main(args.mode, args.heuristic)
