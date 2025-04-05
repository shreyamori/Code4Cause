import os
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import openai

load_dotenv()

# Set up the OpenAI client (new 1.x way)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    return redirect(url_for('interests'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('login_page'))
    return render_template('signup.html')

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/interests")
def interests():
    return render_template("interests.html")

@app.route("/concepts")
def concepts():
    return render_template("concepts.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    print("API Key:", os.getenv("OPENAI_API_KEY"))

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
