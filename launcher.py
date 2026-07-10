import os
import threading
import time
import webbrowser

from web import create_app


HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))
OPEN_HOST = os.getenv("OPEN_HOST", "127.0.0.1")


def _open_browser():
    time.sleep(1.5)
    webbrowser.open(f"http://{OPEN_HOST}:{PORT}/")


def main():
    app = create_app()
    threading.Thread(target=_open_browser, daemon=True).start()
    app.run(debug=False, use_reloader=False, host=HOST, port=PORT)


if __name__ == "__main__":
    main()
