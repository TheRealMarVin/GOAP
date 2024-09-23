import time
from typing import Dict


class Action:
    def __init__(self, name: str, preconditions: Dict[str, bool], effects: Dict[str, bool], duration: int,
                 cost: int = 1):
        self.name = name
        self.preconditions = preconditions
        self.effects = effects
        self.duration = duration
        self.cost = cost

    def is_applicable(self, state: Dict[str, bool]) -> bool:
        return all(state.get(k, False) == v for k, v in self.preconditions.items())

    def execute(self, state: Dict[str, bool], on_interrupt=None):
        print(f"Starting action: {self.name} (duration: {self.duration}s)")
        for i in range(self.duration):
            if on_interrupt and on_interrupt():
                print(f"Action {self.name} interrupted!")
                return False
            time.sleep(1)  # Simulate the action taking time
        print(f"Action {self.name} completed!")
        state.update(self.effects)
        return True
