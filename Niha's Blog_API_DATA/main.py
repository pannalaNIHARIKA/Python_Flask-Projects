from flask import Flask, render_template
import requests

URL = "https://api.npoint.io/cd492fa865e931928849"
app = Flask(__name__)

response = requests.get(URL)
blog_data = response.json()

@app.route('/')
def home():
    return render_template("index.html", blog_posts=blog_data)

@app.route('/post/<int:blog_id>')
def blog_page(blog_id):
    return render_template("post.html", b_id=blog_id, posts=blog_data)

if __name__ == "__main__":
    app.run(debug=True)
