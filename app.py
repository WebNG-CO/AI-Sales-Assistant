from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# سیستم پرامپت پایه برای دستیار فروش
SYSTEM_PROMPT = """
شما یک دستیار فروش هستید برای خدمات طراحی سایت WebNG. با مشتری مودب، ساده و مفید صحبت کن.
"""

# کلید API و URL مربوط به OpenRouter (باید جایگزین شود)
API_KEY = "your-openrouter-api-key"
API_URL = "https://openrouter.ai/api/v1/chat"

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
  <title>WebNG Chatbot</title>
</head>
<body>
  <h2>دستیار فروش WebNG</h2>
  <form method="POST">
    <textarea name="user_input" rows="4" cols="50" placeholder="سوال خود را بنویسید..."></textarea><br>
    <input type="submit" value="ارسال">
  </form>
  {% if response %}
    <div style="margin-top:20px;">
      <strong>پاسخ:</strong>
      <p>{{ response }}</p>
    </div>
  {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def chat():
    response_text = None
    if request.method == 'POST':
        user_input = request.form['user_input']

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ]
        }

        r = requests.post(API_URL, headers=headers, json=data)
        if r.status_code == 200:
            response_text = r.json()['choices'][0]['message']['content']
        else:
            response_text = f"خطا در دریافت پاسخ: {r.status_code}"

    return render_template_string(HTML_PAGE, response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
