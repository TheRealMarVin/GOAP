"""
This script sets up and runs a cooking experiment using the GOAP (Goal-Oriented Action Planning) system.
It allows the user to run the experiment in two modes: 'plan' (generates and displays the plan)
and 'execute' (executes the plan with dynamic updates via an event thread).

This script demonstrates a multi-goal planning scenario using GOAP, with goals of varying difficulty levels.
The planner is tested in both global and sequential modes to observe which goals are selected.
"""

import argparse
import threading
import time
from action import Action
from agent import Agent
from event_manager import EventManager
from goal import Goal
from goap_planner import GOAPPlanner

actions = [
    Action(name="ActionA", preconditions={}, effects={"condition_x": 1}, cost=100, duration=10),
    Action(name="ActionB", preconditions={}, effects={"condition_y": 1}, cost=300, duration=100),
    Action(name="ActionC", preconditions={}, effects={"condition_z": 1}, cost=30, duration=5)
]


def main(mode):
    """
    Main function to handle the multi goals experiments based on the selected mode.

    Args:
        mode (str): The mode to run ('plan' to generate and display the plan, 'execute' to run the plan with dynamic events).
    """
    initial_state = {}

    goals = [
        Goal(goal_state={"impossible_condition": 1}, heuristic=None),
        Goal(goal_state={"condition_y": 1}, heuristic=None),
        Goal(goal_state={"condition_z": 1}, heuristic=None)
    ]

    planner = GOAPPlanner(actions)
    plan, total_cost = planner.plan(initial_state, goals, {})

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

    agent.execute_plan(initial_state, plan, {"goals": goal})
    planner.display_usage_stats()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi Goals Experiment")
    parser.add_argument("--mode", choices=["plan", "execute"], default="plan",
                        help="Choose whether to plan or execute the experiment")
    args = parser.parse_args()

    main(args.mode)
