"""Agent constants.

    Includes: Agent Capabilities
"""

from enum import Enum


class AgentCapability(Enum):
    DISPLAY_ONLY = "DisplayOnly"  # or DisplayYesNo
    KEYBOARD_ONLY = "KeyboardOnly"  # or KeyboardDisplay
    NO_INPUT_NO_OUTPUT = "NoInputNoOutput"


AGENT_PATH = '/test/agent'
