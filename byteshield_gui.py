"""
ByteShield - System Cleaner & Virus Scanner
Backward compatibility wrapper

This file provides backward compatibility for users running:
    python byteshield_gui.py

It imports and runs the modular version from src/
"""

from src.main import main

if __name__ == "__main__":
    main()
