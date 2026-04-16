"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file
import os


from app.forms import MovieForm
from app.models import Movie
from werkzeug.utils import secure_filename
from app import db

from flask_wtf.csrf import generate_csrf
from flask import jsonify

from flask import send_file
from flask import send_from_directory



###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    #return render_template('404.html'), 404
    return jsonify({"error": "Not Found"}), 404


@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()

    if form.validate_on_submit():

        # 1. Get form data
        title = form.title.data
        description = form.description.data
        poster_file = form.poster.data

        # 2. Secure filename
        filename = secure_filename(poster_file.filename)

        # 3. Save file to uploads folder
        #upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        #upload_path = os.path.join("app", "static", "uploads", filename)
        upload_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "static", "uploads", filename)
)
        #print("UPLOAD FOLDER:", app.config['UPLOAD_FOLDER'])
        poster_file.save(upload_path)

        # 4. Save to database
        movie = Movie(
            title=title,
            description=description,
            poster=filename
        )

        db.session.add(movie)
        db.session.commit()

        # 5. Return JSON response
        return jsonify({
            "message": "File Upload Successful",
            "title": title,
            "poster": filename,
            "description": description
        }), 201
    else:
        print(form.errors)

        return jsonify({
            "errors": form_errors(form)
        }), 400

#def form_errors(form):
 #   error_list = []
  #  for field, errors in form.errors.items():
   #     for error in errors:
    #        error_list.append({field: error})
    #return error_list

def form_errors(form):
    error_list = []

    for field, errors in form.errors.items():
        for error in errors:
            message = f"Error in {field} field - {error}"
            error_list.append(message)

    return error_list


@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()

    data = []

    for movie in movies:
        data.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "poster": movie.poster
        })

    return jsonify({"movies": data})

@app.route("/api/v1/posters/<filename>")
def get_poster(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "static", "uploads"),
        filename
    )
