# models.py
from extensions import db
from sqlalchemy.orm import validates


class Author(db.Model):
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    phone_number = db.Column(db.String)
    posts = db.relationship("Post", backref="author")

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author name cannot be blank.")
        return value

    @validates("phone_number")
    def validate_phone(self, key, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return value


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    summary = db.Column(db.String)
    category = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey("authors.id"))

    @validates("content")
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Post content must be at least 250 characters.")
        return value

    @validates("summary")
    def validate_summary(self, key, value):
        if len(value) > 250:
            raise ValueError("Post summary must be 250 characters or less.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if value not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Post category must be either 'Fiction' or 'Non-Fiction'.")
        return value

    @validates("title")
    def validate_title(self, key, value):
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(keyword in value for keyword in clickbait_keywords):
            raise ValueError("Title must be clickbait-y.")
        return value
