import logging
from typing import Optional

import sounddevice as sd

from src.application.event_bus import EventBus
from src.config import DEFAULT_MIC_INPUT_NAME
from src.domain.service.speech_listener_providers.whisper_speech_listener_provider import \
    WhisperSpeechListenerProvider
from src.shared.helpers.constants import EventType


class SpeechListenerFactory:
    @staticmethod
    def create_speech_listener(
        listener_type: str,
        event_bus: EventBus,
        model_name: str = "base",
        temp_directory: str = "/tmp",
    ):

        devices = sd.query_devices()
        input_device_index = None

        if DEFAULT_MIC_INPUT_NAME:
            for device in devices:
                if DEFAULT_MIC_INPUT_NAME in device['name']:
                    input_device_index = device['index']
                    break


        if DEFAULT_MIC_INPUT_NAME and not input_device_index:
            print(f"Default mic input device not found: {DEFAULT_MIC_INPUT_NAME}")
            print("Available device names:")
            for index, device in enumerate(devices):
                if device["max_input_channels"] > 0:
                    print(f"{device['name']}")
            return


        if not input_device_index:
            print(f"Using device index: {input_device_index}")
            # Prompt for device selection if input_device_index is not provided
            print("Available audio input devices:")
            for index, device in enumerate(devices):
                if device["max_input_channels"] > 0:
                    print(
                        f"{index}: {device['name']} - Max Input Channels: {device['max_input_channels']}"
                    )

            input_device_index = int(input("Select an input device index: "))

        # Ensure the input device index is within the range of available devices
        if input_device_index >= len(sd.query_devices()) or input_device_index < 0:
            raise ValueError("Invalid device index selected.")

        if listener_type == "whisper":
            return WhisperSpeechListenerProvider(
                event_bus, input_device_index, model_name, temp_directory
            )
        else:
            raise ValueError(f"Unsupported speech listener type: {listener_type}")
