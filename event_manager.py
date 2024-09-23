class EventManager:
    def __init__(self):
        self.listeners = []

    def subscribe(self, callback):
        self.listeners.append(callback)

    def notify(self):
        for listener in self.listeners:
            listener()
