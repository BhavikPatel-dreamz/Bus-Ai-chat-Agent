from routes.chat import chat_bp
from flask import Flask

app = Flask(__name__)
app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(port=5050)
