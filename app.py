import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import openai

load_dotenv()

# Set up the OpenAI client (new 1.x way)
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecret")  # For session handling

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    session['user'] = username
    return redirect(url_for('interests'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return redirect(url_for('login_page'))
    return render_template('signup.html')

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        concept = request.form.get("concept")
        grade = request.form.get("grade")
        subject = request.form.get("subject")

        # Generate the prefilled message
        grade_text = grade.replace("grade", "Grade ").title()
        subject_text = subject.title()
        message = f"Explain '{concept}' to a {grade_text} student interested in {subject_text} in a fun and simple way."

        return render_template("index.html", prefill_message=message)

    # If GET
    return render_template("index.html", prefill_message="")


@app.route("/interests")
def interests():
    return render_template("interests.html")

@app.route("/concepts")
def concepts():
    return render_template("concepts.html")

@app.route('/concept-submit', methods=['POST'])
def concept_submit():
    concept = request.form.get("concept")
    grade = request.form.get("grade")
    subject = request.form.get("subject")
    interest = subject.capitalize()

    user_prompt = f"Explain '{concept}' to a {grade.replace('grade', 'Grade ')} student interested in {interest} in a fun and simple way."
    return render_template("index.html", concept_prompt=user_prompt)

@app.route('/chat', methods=['POST'])
def chat():
    messages = request.json.get("messages")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            temperature=0.8,
            messages=messages
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"reply": reply})

    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"error": "Something went wrong. Please try again."}), 500

@app.route('/image', methods=['POST'])
def generate_image():
    prompt = request.json.get("prompt")

    safe_prompt = f"Generate an educational and safe illustration: {prompt}"

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=safe_prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url
        print("✅ Generated image:", image_url)
        return jsonify({ "image": image_url })

    except openai.OpenAIError as e:
        print("❌ Image generation error:", e)
        return jsonify({ "error": str(e) }), 400

if __name__ == "__main__":
    app.run(debug=True)
