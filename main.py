from flask import Flask, render_template, request
from datetime import datetime
import json
app = Flask(__name__)


def load_messages():
    with open("db.json", "r") as file:
        data = json.load(file)
    return data.get("messages", [])

all_messages = load_messages()


def add_message(author, text):  # объявляем функцию добавления сообщений с параметрами
    message = {
        "author": author,
        "text": text,
        "time": datetime.now().strftime("%H:%M:%S")
    }
    all_messages.append(message)  # добавляем параметризированное сообщение в список всех сообщений
    save_message()

def save_message(): # сохраняем сообщения в файл
    all_messages_data = {
        "messages": all_messages
    }
    with open("db.json", "w") as file:
        json.dump(all_messages_data, file)

@app.route("/") # реализуем эндпоинт начальной страницы
def main_page():
    return "Hello"

@app.route("/chat")
def chat_page():
    return render_template("form.html")

@app.route("/get_messages")
def get_messages():
    print("Cообщения...")
    return {"messages": all_messages}

@app.route("/send_message")
def send_message():
    name = request.args.get("name") # получаем данные из query параметров запроса к серверу
    text = request.args.get("text")
    print(f"пользователь '{name}' пишет '{text}'")
    add_message(name, text)
    return "ok"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)