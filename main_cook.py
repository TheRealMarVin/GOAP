import threading
import time

from action import Action
from agent import Agent
from event_manager import EventManager
from goap_planner import GOAPPlanner
from typing import Dict


actions = [
    Action("Gather Wood1", preconditions={}, effects={"wood": 10}, duration=5, cost=5),
    Action("Gather Wood2", preconditions={}, effects={"wood": 3}, duration=1, cost=2),
    Action("Light Fire", preconditions={"wood": 15}, effects={"fire": 1}, duration=2, cost=2),
    Action("Cook Food", preconditions={"fire": 1}, effects={"cooked_food": 1}, duration=5, cost=5),
]

event_manager = EventManager()


def simulate_event():
    time.sleep(4)
    event_manager.notify()


event_thread = threading.Thread(target=simulate_event)
event_thread.start()

initial_state = {
    "wood": 0,
    "fire": 0,
    "cooked_food": 0
}
goal_state = {
    "cooked_food": 1
}


def cooking_heuristic(state: Dict[str, int], goal_state: Dict[str, int], context: Dict) -> int:
    return sum(1 for k, v in goal_state.items() if state.get(k, 0) < v)


planner = GOAPPlanner(actions, heuristic=cooking_heuristic)

cooking_context = {}

plan, total_cost = planner.plan(initial_state, goal_state, cooking_context)
chef = Agent(actions, planner, event_manager, verbose=True)
chef.execute_plan(initial_state, plan, cooking_context)
