from flask import Flask, render_template_string
from datetime import datetime
import logging
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

NEWS_LIST = [
    "🚀 DevOps adoption is accelerating across global tech companies.",
    "☁️ Kubernetes remains the leading container orchestration platform.",
    "🤖 AI-powered automation is transforming CI/CD pipelines.",
    "⚡ Serverless computing is reducing infrastructure complexity.",
    "🔐 DevSecOps is becoming a standard for secure software delivery."
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Smart News Portal</title>
<style>
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(120deg,#1f4037,#99f2c8);
    margin:0;
    padding:0;
}

.header {
    text-align:center;
    padding:30px;
    color:white;
}

.container {
    width:80%;
    margin:auto;
}

.card {
    background:white;
    padding:20px;
    margin:20px 0;
    border-radius:12px;
    box-shadow:0 6px 15px rgba(0,0,0,0.2);
    transition:transform 0.2s;
}

.card:hover {
    transform:scale(1.03);
}

.time {
    font-size:12px;
    color:gray;
}

.footer {
    text-align:center;
    padding:20px;
    color:white;
    font-size:14px;
}
</style>
</head>

<body>

<div class="header">
<h1>📰 Smart DevOps News Portal</h1>
<p>Live Technology Updates</p>
</div>

<div class="container">

{% for news in news_list %}
<div class="card">
<h3>{{ news }}</h3>
<p class="time">Published: {{ time }}</p>
</div>
{% endfor %}

</div>

<div class="footer">
Built with Flask | DevOps Demo Project
</div>

</body>
</html>
"""

@app.route("/")
def home():
    """
    Render the news homepage.
    """
    try:
        current_time = datetime.now().strftime("%d %b %Y %H:%M")

        return render_template_string(
            HTML_TEMPLATE,
            news_list=NEWS_LIST,
            time=current_time
        )

    except Exception as error:
        logging.error("Error rendering homepage: %s", error)
        return "Internal Server Error", 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
