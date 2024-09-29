"""
This module implements the EventManager class, which manages event subscriptions
and notifies listeners when an event occurs.
"""

class EventManager:
    def __init__(self):
        """
        Initializes the EventManager with an empty list of listeners.
        """
        self.listeners = []

    def subscribe(self, callback):
        """
        Subscribes a callback function to be notified when an event occurs.

        Args:
            callback (Callable): The function to be called when an event is triggered.
        """
        self.listeners.append(callback)

    def notify(self):
        """
        Notifies all subscribed listeners by calling their respective callback functions.
        """
        for listener in self.listeners:
            listener()
