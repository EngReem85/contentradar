#!/usr/bin/env python
"""
ContentRadar - Main Entry Point
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.utils.config import Config
import streamlit.web.cli as stcli
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    print(f"🚀 Starting {Config.APP_NAME} v{Config.VERSION}")
    
    # Ensure directories exist
    Config.ensure_dirs()
    
    # Validate configuration
    if not Config.validate():
        logger.warning("Configuration validation failed. Some features may not work.")
    
    # Launch Streamlit
    sys.argv = ["streamlit", "run", "ui/app.py", "--server.port=8501"]
    stcli.main()

if __name__ == "__main__":
    main()