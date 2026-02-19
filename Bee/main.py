"""
Main Application Starter for AI Assistant
Author: Your Name
Description: Handles UI initialization, face authentication,
and assistant startup sequence.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

import eel

# Internal Modules
from engine.features import playAssistantSound, speak
from engine.command import *
from engine.auth import recoganize


# ===============================
# Configuration
# ===============================

APP_NAME = "GenAI Assistant"
USER_NAME = os.getenv("ASSISTANT_USER", "User")
WEB_FOLDER = "www"
START_PAGE = "index.html"
HOST = "localhost"
PORT = 8000


# ===============================
# Logging Setup
# ===============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# ===============================
# Core Application
# ===============================

def start():
    """
    Initialize Eel application and authentication flow.
    """

    try:
        eel.init(WEB_FOLDER)
        logger.info("Eel initialized successfully.")

        @eel.expose
        def init():
            """
            Frontend initialization function exposed to JS.
            """

            try:
                logger.info("Starting device initialization...")
                subprocess.call(["device.bat"], shell=True)

                eel.hideLoader()
                speak("Ready for Face Authentication")

                logger.info("Starting Face Authentication...")
                flag = recoganize.AuthenticateFace()

                if flag == 1:
                    logger.info("Face Authentication Successful.")
                    eel.hideFaceAuth()
                    speak("Face Authentication Successful")
                    eel.hideFaceAuthSuccess()

                    welcome_message = f"Hello {USER_NAME}, How can I help you?"
                    speak(welcome_message)

                    eel.hideStart()
                    playAssistantSound()

                else:
                    logger.warning("Face Authentication Failed.")
                    speak("Face Authentication Failed. Please try again.")

            except Exception as e:
                logger.error(f"Error during initialization: {e}")
                speak("An error occurred during initialization.")

        # Open browser in app mode (Windows Edge)
        open_browser()

        eel.start(
            START_PAGE,
            mode=None,
            host=HOST,
            port=PORT,
            block=True
        )

    except Exception as e:
        logger.critical(f"Application failed to start: {e}")
        sys.exit(1)


# ===============================
# Utility Functions
# ===============================

def open_browser():
    """
    Open the web interface in app mode.
    Supports Windows (Edge).
    """
    try:
        if os.name == "nt":
            subprocess.Popen(
                ['msedge.exe', f'--app=http://{HOST}:{PORT}/{START_PAGE}'],
                shell=True
            )
            logger.info("Browser launched successfully.")
        else:
            logger.info("Non-Windows OS detected. Open manually in browser.")

    except Exception as e:
        logger.error(f"Failed to open browser: {e}")


# ===============================
# Entry Point
# ===============================

if __name__ == "__main__":
    start()
