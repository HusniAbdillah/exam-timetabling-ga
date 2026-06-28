import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Launch the Streamlit app.

    Resolves the application path and invokes streamlit run via subprocess.
    """
    project_root = Path(__file__).parent.resolve()
    app_path = project_root / "app" / "app.py"

    print("Launching Streamlit dashboard... (Press Ctrl+C to stop)")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", str(app_path)])
    except KeyboardInterrupt:
        print("\nStreamlit dashboard stopped. Exiting gracefully...")
        sys.exit(0)


if __name__ == "__main__":
    main()
