import logging
from typing import Callable, List

from pynput import keyboard
from pynput.keyboard import Key, Listener


class KeyboardManager:
    """
    Manages global keyboard events, dispatching them to registered callbacks.
    """
    def __init__(self):
        """
        Sets up the keyboard listener with an empty callback list.
        """
        self.listener: Listener = keyboard.Listener(on_press=self.on_press)
        self.callbacks: List[Callable[[Key], None]] = []

    def on_press(self, key: Key):
        """
        Executes all registered callbacks when a key is pressed.
        """
        for callback in self.callbacks:
            try:
                callback(key)
            except Exception as e:
                logging.error("Error in callback %s: %s", callback, e)

    def register_callback(self, callback: Callable[[Key], None]):
        """
        Registers a callback to receive key press events.
        """
        if callback not in self.callbacks:
            self.callbacks.append(callback)

    def unregister_callback(self, callback: Callable[[Key], None]):
        """
        Unregisters a callback, preventing it from receiving further key press events.
        """
        if callback in self.callbacks:
            self.callbacks.remove(callback)

    def start_listener(self):
        """
        Starts the listener if it's not already active, allowing it to begin handling events.
        """
        if not self.listener.running:
            self.listener.start()

    def stop_listener(self):
        """
        Stops the listener, ceasing event handling and freeing up resources.
        """
        if self.listener.running:
            self.listener.stop()
