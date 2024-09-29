"""
This module defines the Action class, which represents an individual action that an agent can perform
in the GOAP (Goal-Oriented Action Planning) system. Each action has preconditions, effects,
a duration, and a cost associated with its execution.
"""

import time
from typing import Dict


class Action:
    def __init__(self, name: str, preconditions: Dict[str, int], effects: Dict[str, int], duration: int, cost: int = 1):
        """
        Initializes an Action with its name, preconditions, effects, duration, and cost.

        Args:
            name (str): The name of the action.
            preconditions (Dict[str, int]): The preconditions required for the action to be executed.
            effects (Dict[str, int]): The effects the action has on the state after execution.
            duration (int): The time (in seconds) it takes to complete the action.
            cost (int): The cost associated with performing the action.
        """
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.duration = duration
        self.cost = cost

    def is_applicable(self, state: Dict[str, int]) -> bool:
        """
        Checks if the action can be applied in the given state based on its preconditions.

        Args:
            state (Dict[str, int]): The current state of the agent.

        Returns:
            bool: True if all preconditions are met, False otherwise.
        """
        return all(state.get(k, 0) >= v for k, v in self.preconditions.items())

    def execute(self, state: Dict[str, int], on_interrupt=None, verbose=True):
        """
        Executes the action, updating the state based on the action's effects after the specified duration.
        The action can be interrupted if the provided callback returns True.

        Args:
            state (Dict[str, int]): The current state of the agent.
            on_interrupt (Callable, optional): A callback function to check if the action should be interrupted.
            verbose (bool): If True, enables detailed logging of the action execution.

        Returns:
            bool: True if the action completes successfully, False if it was interrupted.
        """
        if not self.is_applicable(state):
            print(f"Preconditions for action {self.name} are not met.")
            return False

        if verbose:
            print(f"Starting action: {self.name} (duration: {self.duration}s)")

        for i in range(self.duration):
            if on_interrupt and on_interrupt():
                if verbose:
                    print(f"Action {self.name} interrupted!")
                return False
            time.sleep(1)

        if verbose:
            print(f"Action {self.name} completed!")

        for k, v in self.effects.items():
            state[k] = state.get(k, 0) + v

        return True
