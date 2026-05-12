from flask import Flask, render_template, request, redirect
from config import Config
from models import db, URL

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original_url = request.form["url"]

        url = URL(original_url=original_url)
        url.short_code = url.generate_short_code()

        db.session.add(url)
        db.session.commit()

        short_url = request.host_url + url.short_code
        return render_template("index.html", short_url=short_url)

    return render_template("index.html")


@app.route("/<short_code>")
def redirect_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()

    if url:
        url.clicks += 1
        db.session.commit()
        return redirect(url.original_url)

    return "URL not found"


if __name__ == "__main__":
    app.run(debug=True)