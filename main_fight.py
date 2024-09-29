"""
This script sets up and runs a fighting experiment using the GOAP (Goal-Oriented Action Planning) system.
It allows the user to run the experiment in two modes: 'plan' (generates and displays the plan) 
and 'execute' (executes the plan with dynamic updates via opponent actions).
"""

import argparse
import threading
import time

from action import Action
from agent import Agent
from event_manager import EventManager
from goap_planner import GOAPPlanner
from typing import Dict


class Opponent:
    def __init__(self, name: str, x: int, y: int, health: int, move_type: str):
        """
        Initializes an opponent with a name, position, health, and movement type.

        Args:
            name (str): The name of the opponent.
            x (int): The initial x-coordinate of the opponent.
            y (int): The initial y-coordinate of the opponent.
            health (int): The health of the opponent.
            move_type (str): The type of movement ("vertical" or "horizontal").
        """
        self.name = name
        self.x = x
        self.y = y
        self.health = health
        self.move_type = move_type
        self.actions = [("Wait", 2)] 
        self.current_action_index = 0
        self.move_direction = 1

    def perform_action(self):
        """
        Executes the current action of the opponent, which could be waiting or moving.
        """
        if self.health > 0:
            if self.current_action_index < len(self.actions):
                action, duration = self.actions[self.current_action_index]
                if action == "Wait":
                    print(f"{self.name} is waiting for {duration} turn(s).")
                    time.sleep(duration)
                    self.current_action_index += 1
                elif action == "Move":
                    self.move()
                    self.current_action_index += 1

        if self.current_action_index >= len(self.actions):
            self.current_action_index = 0
            self.prepare_next_move()

    def move(self):
        """
        Moves the opponent in the specified direction (either vertical or horizontal), 
        adjusting direction when hitting the grid boundaries.
        """
        if self.move_type == "vertical":
            self.y += self.move_direction

            if self.y > 9 or self.y < 0:
                self.move_direction *= -1
                self.y += self.move_direction
            print(f"{self.name} moved vertically to position ({self.x}, {self.y})")

        elif self.move_type == "horizontal":
            self.x += self.move_direction
            if self.x > 9 or self.x < 0:
                self.move_direction *= -1
                self.x += self.move_direction
            print(f"{self.name} moved horizontally to position ({self.x}, {self.y})")

    def prepare_next_move(self):
        """
        Prepares the next set of actions for the opponent based on their movement type.
        """
        if self.move_type == "vertical":
            self.actions = [("Move", 1), ("Wait", 2)]
        elif self.move_type == "horizontal":
            self.actions = [("Move", 1), ("Wait", 2)]
        self.current_action_index = 0


opponents = [
    Opponent("Opponent1", 2, 0, 50, move_type="vertical"),
    Opponent("Opponent2", 4, 1, 100, move_type="horizontal")
]


actions = [
    Action("Move Up", {"stamina": 1}, {"y": +1, "stamina": -1}, duration=1, cost=1),
    Action("Move Down", {"stamina": 1}, {"y": -1, "stamina": -1}, duration=1, cost=1),
    Action("Move Left", {"stamina": 1}, {"x": -1, "stamina": -1}, duration=1, cost=1),
    Action("Move Right", {"stamina": 1}, {"x": +1, "stamina": -1}, duration=1, cost=1),
    Action("Simple Attack", {"stamina": 2, "in_range": 1}, {"damage_dealt": 10, "stamina": -2}, duration=1, cost=2),
    Action("Combo Attack", {"stamina": 4, "in_range": 1}, {"damage_dealt": 30, "stamina": -4}, duration=2, cost=4),
    Action("Block", {"stamina": 1, "in_range": 1}, {"blocking": 1, "stamina": -1}, duration=1, cost=1),
    Action("Counter Attack", {"blocking": 1, "stamina": 2, "in_range": 1},
           {"damage_dealt": 20, "blocking": 0, "stamina": -2}, duration=1, cost=2),
    Action("Wait", {}, {"stamina": 10}, duration=1, cost=1)
]


def fight_heuristic(state: Dict[str, int], goal_state: Dict[str, int], context: Dict) -> int:
    """
    Heuristic function that calculates the cost of the current state relative to the goal state 
    for the fight scenario based on the distance and health of enemies.

    Args:
        state (Dict[str, int]): The current state of the agent.
        goal_state (Dict[str, int]): The desired goal state.
        context (Dict): Additional context, including information about enemies.

    Returns:
        int: The calculated heuristic cost.
    """
    enemies = context.get("enemies", [])
    fighter_x, fighter_y = state['x'], state['y']
    total_cost = 0

    for i, enemy in enumerate(enemies):
        perceived_health = state.get(f"enemy_health_{i}", float('inf'))
        distance = abs(fighter_x - enemy.x) + abs(fighter_y - enemy.y)

        if perceived_health == 0:
            distance = 0

        total_cost += (distance * 1) + (perceived_health * 1)

    return total_cost


def update_fight_state(state: Dict[str, int], context: Dict):
    """
    Updates the agent's state to reflect the current fight scenario, including health and 
    whether the agent is in range of enemies.

    Args:
        state (Dict[str, int]): The agent's current state.
        context (Dict): Additional context, including information about enemies.
    """
    enemies = context.get("enemies", [])
    fighter_x, fighter_y = state['x'], state['y']

    in_range = any(abs(fighter_x - enemy.x) == 0 and abs(fighter_y - enemy.y) == 0 for enemy in enemies)
    state['in_range'] = 1 if in_range else 0

    for i, enemy in enumerate(enemies):
        perceived_health_key = f"enemy_health_{i}"

        if perceived_health_key not in state:
            state[perceived_health_key] = enemy.health

        if (fighter_x - enemy.x) == 0 and (fighter_y - enemy.y) == 0 and "damage_dealt" in state:
            damage = state["damage_dealt"]
            state[perceived_health_key] = max(0, state[perceived_health_key] - damage)

    state["damage_dealt"] = 0


def update_enemy_health(action: Action, state: Dict[str, int], context: Dict):
    """
    Updates the health of enemies based on the agent's action effects.

    Args:
        action (Action): The action executed by the agent.
        state (Dict[str, int]): The agent's current state.
        context (Dict): Additional context, including information about enemies.
    """
    if action.name in ["Simple Attack", "Combo Attack", "Counter Attack"]:
        enemies = context.get("enemies", [])
        fighter_x, fighter_y = state['x'], state['y']

        for enemy in enemies:
            if abs(fighter_x - enemy.x) == 0 and abs(fighter_y - enemy.y) == 0 and enemy.health > 0:
                damage = action.effects.get("damage_dealt", 0)

                enemy.health = max(0, enemy.health - damage)

                if state.get("verbose", False):
                    if enemy.health > 0:
                        print(f"{enemy.name} took {damage} damage! Remaining health: {enemy.health}")
                    else:
                        print(f"{enemy.name} is dead!")


def opponent_thread():
    """
    Continuously iterates over all opponents and performs their actions in a separate thread.
    """
    while True:
        for opponent in opponents:
            opponent.perform_action()
            time.sleep(1)


def main(mode):
    """
    Main function to handle the fighting experiment based on the selected mode.

    Args:
        mode (str): The mode to run ('plan' to generate and display the plan, 'execute' to run the plan with opponent actions).
    """
    goal_state = {f"enemy_health_{i}": 0 for i in range(len(opponents))}
    fight_context = {
        "enemies": opponents,
        "update_state_callback": update_fight_state,
        "post_action_callback": update_enemy_health,
        "goal_state": goal_state
    }

    fighter_initial_state = {"x": 0, "y": 0, "stamina": 20, "health": 100, "blocking": 0, "in_range": 0, "damage_dealt": 0}

    planner = GOAPPlanner(actions, heuristic=fight_heuristic)
    plan, total_cost = planner.plan(fighter_initial_state, goal_state, fight_context)

    if mode == "plan":
        print(f"Generated Plan: {plan} with total cost: {total_cost}")
        return

    opponent_thread_obj = threading.Thread(target=opponent_thread, daemon=True)
    opponent_thread_obj.start()

    event_manager = EventManager()
    fighter = Agent(actions, planner, event_manager, verbose=True)
    fighter.execute_plan(fighter_initial_state, plan, fight_context)
    planner.display_usage_stats()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fighting Experiment")
    parser.add_argument("--mode", choices=["plan", "execute"], default="plan",
                        help="Choose whether to plan or execute the experiment")
    args = parser.parse_args()

    main(args.mode)
