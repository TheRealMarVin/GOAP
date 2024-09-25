import time
from typing import Dict


class Action:
    def __init__(self, name: str, preconditions: Dict[str, int], effects: Dict[str, int], duration: int, cost: int = 1):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.duration = duration
        self.cost = cost

    def is_applicable(self, state: Dict[str, int]) -> bool:
        return all(state.get(k, 0) >= v for k, v in self.preconditions.items())

    def execute(self, state: Dict[str, int], on_interrupt=None, verbose=True):
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
