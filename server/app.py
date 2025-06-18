# app.py
from flask import Flask, request
from extensions import db
from models import Author, Post
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    try:
        author = Author(name=data["name"], phone_number=data["phone_number"])
        db.session.add(author)
        db.session.commit()
        return {"message": "Author created successfully!"}, 201
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return {"error": str(e.orig) if isinstance(e, IntegrityError) else str(e)}, 400


@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    try:
        post = Post(
            title=data["title"],
            content=data["content"],
            summary=data["summary"],
            category=data["category"],
            author_id=data["author_id"],
        )
        db.session.add(post)
        db.session.commit()
        return {"message": "Post created successfully!"}, 201
    except ValueError as e:
        db.session.rollback()
        return {"error": str(e)}, 400
