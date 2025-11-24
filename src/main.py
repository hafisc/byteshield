"""
ByteShield Entry Point
Main entry point untuk aplikasi ByteShield
"""

from src.app import ByteShieldApp


def main():
    """Run aplikasi ByteShield"""
    app = ByteShieldApp()
    app.mainloop()


if __name__ == "__main__":
    main()
