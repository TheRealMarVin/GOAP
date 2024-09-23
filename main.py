import time

from action import Action
from agent import Agent
from event_manager import EventManager
from goap_planner import GOAPPlanner

actions = [
    Action("Gather Wood", preconditions={}, effects={"has_wood": True}, duration=3),
    Action("Light Fire", preconditions={"has_wood": True}, effects={"has_fire": True}, duration=2),
    Action("Cook Food", preconditions={"has_fire": True}, effects={"has_cooked_food": True}, duration=5),
]

event_manager = EventManager()
planner = GOAPPlanner(actions)
agent = Agent(actions, planner, event_manager)


def simulate_event():
    time.sleep(4)
    event_manager.notify()


# Run the agent in parallel with an event being triggered
import threading

event_thread = threading.Thread(target=simulate_event)
event_thread.start()

initial_state = {
    "has_wood": False,
    "has_fire": False,
    "has_cooked_food": False
}
goal_state = {
    "has_cooked_food": True
}

agent.execute_plan(initial_state, goal_state)
