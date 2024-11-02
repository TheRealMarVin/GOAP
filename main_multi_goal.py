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
from goap_planner import GOAPPlanner, PlanningMode

actions = [
    Action(name="ActionA", preconditions={}, effects={"condition_x": 1}, cost=100, duration=10),
    Action(name="ActionB", preconditions={}, effects={"condition_y": 1}, cost=300, duration=100),
    Action(name="ActionC", preconditions={}, effects={"condition_z": 1}, cost=30, duration=5)
]


def main():
    """
    Main function to handle the multi goals experiments based on the selected mode.
    """
    initial_state = {}

    goals = [
        Goal(goal_state={"impossible_condition": 1}, heuristic=None),
        Goal(goal_state={"condition_y": 1}, heuristic=None),
        Goal(goal_state={"condition_z": 1}, heuristic=None)
    ]

    planner = GOAPPlanner(actions)

    plan, total_cost = planner.plan(initial_state, goals, {}, mode=PlanningMode.GLOBAL)
    print(f"Generated Plan (Global): {plan} with total cost: {total_cost}")
    planner.display_usage_stats()

    plan, total_cost = planner.plan(initial_state, goals, {}, mode=PlanningMode.SEQUENTIAL)
    print(f"Generated Plan (Sequential): {plan} with total cost: {total_cost}")
    planner.display_usage_stats()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi Goals Experiment")
    args = parser.parse_args()

    main()
