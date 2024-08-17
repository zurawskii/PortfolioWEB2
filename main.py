import os

from flask import Flask, render_template, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from flask_ckeditor import CKEditor, CKEditorField
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from bs4 import BeautifulSoup
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY',  '8BYkEfBA6O6donzWlSihBXox7C0sKR6b')
ckeditor = CKEditor(app)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", "sqlite:///messages.db")
# Create the extension
db = SQLAlchemy(model_class=Base)
# Initialise the app with the extension
db.init_app(app)


class Email(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    sender: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(2000), nullable=False)


with app.app_context():
    db.create_all()


class PostForm(FlaskForm):
    title = StringField('Message Title', name="title")
    email = EmailField('Email To Respond', name="email")
    content = CKEditorField('Message', name="content")


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if request.method == "POST":
        clean_content = BeautifulSoup(request.form["content"], "html.parser").get_text()
        # CREATE RECORD
        new_message = Email(
            title=request.form["title"],
            sender=request.form["email"],
            content=clean_content
        )
        db.session.add(new_message)
        db.session.commit()

        return render_template("add.html")
    return render_template('index.html', form=form)


@app.route("/add", methods=["GET"])
def add():
    return render_template("add.html")


if __name__ == '__main__':
    app.run(debug=False)
