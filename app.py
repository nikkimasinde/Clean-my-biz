import os
from flask import Flask, render_template, request, session
from openai import OpenAI

app = Flask(__name__)
app.secret_key = "business_secret_123"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    error = ""
    
    if request.method == "POST":
        user_input = request.form.get("content", "")
        word_count = len(user_input.split())

        if word_count > 50:
            error = f"Sample limit reached! ({word_count}/50 words). Please shorten your text for the free tester."
        elif session.get('used_sample'):
            error = "Free sample limit reached. Upgrade to Professional to continue!"
        else:
            try:
                # This prompt tells the AI exactly what 'Pros' to show with the price
                response = client.chat.completions.create(
                    model="anthropic/claude-3-haiku",
                    messages=[
                        {"role": "system", "content": """You are a professional business organizer. 
                        Organize the input into a clean table. 
                        At the end, add this EXACT message:
                        ---
                        🚀 WANT THE FULL REPORT?
                        Hiring an accountant takes days and costs $500+. 
                        Doing this manually wastes 10+ hours of your life.
                        
                        GET IT DONE INSTANTLY: $172
                        Save time. Save money. Grow your business."""},
                        {"role": "user", "content": user_input}
                    ]
                )
                result = response.choices[0].message.content
                session['used_sample'] = True 
            except Exception as e:
                error = "Connection error. Make sure your OpenRouter credits are ready."

    return render_template("index.html", result=result, error=error)
    
