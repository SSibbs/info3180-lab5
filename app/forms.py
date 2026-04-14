# Add any form classes for Flask-WTF here
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


class MovieForm(FlaskForm):
    title = StringField(
        "Movie Title",
        validators=[DataRequired(), Length(max=100)]
    )

    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(max=500)]
    )

    poster = FileField(
        "Movie Poster",
        validators=[
            FileRequired(),
            FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')
        ]
    )

    submit = SubmitField("Add Movie")