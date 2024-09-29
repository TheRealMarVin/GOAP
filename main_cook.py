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


def main(mode):
    initial_state = {"wood": 0, "fire": 0, "cooked_food": 0}
    goal_state = {"cooked_food": 1}

    planner = GOAPPlanner(actions,
                          heuristic=lambda state, goal, context: sum(abs(state.get(k, 0) - v) for k, v in goal.items()))

    plan, total_cost = planner.plan(initial_state, goal_state, {})

    if mode == "plan":
        print(f"Generated Plan: {plan} with total cost: {total_cost}")
        return

    event_manager = EventManager()

    def event_thread():
        while True:
            time.sleep(5)
            event_manager.publish_event()

    agent = Agent(actions, planner, event_manager, verbose=True)

    event_thread_obj = threading.Thread(target=event_thread, daemon=True)
    event_thread_obj.start()

    agent.execute_plan(initial_state, plan, {"goal_state": goal_state})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cooking Experiment")
    parser.add_argument("--mode", choices=["plan", "execute"], default="plan",
                        help="Choose whether to plan or execute the experiment")
    args = parser.parse_args()

    main(args.mode)
