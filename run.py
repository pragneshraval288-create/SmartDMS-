import threading
import webbrowser
from backend.app import create_app
from backend.extensions import db

def open_browser():
    try:
        webbrowser.open_new("http://127.0.0.1:5000/")
    except:
        pass

def main():
    app = create_app()

    threading.Timer(1.0, open_browser).start()

    with app.app_context():
        db.create_all()

    app.run(debug=True)

if __name__ == "__main__":
    main()
