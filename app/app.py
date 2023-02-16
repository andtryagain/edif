import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    send_from_directory,
    url_for
)
from werkzeug.utils import secure_filename

from film_developer import FilmDeveloper, FilmDeveloperBW, FilmDeveloperColor

UPLOAD_FOLDER                       = 'upload'
RESULT_FOLDER                       = 'result'

HOME_PAGE                           = 'index.html'
UPLOAD_PAGE                         = 'upload.html'

ALLOWED_EXTENSIONS                  = {'png', 'jpg', 'jpeg'}

app                                 = Flask(__name__)

app.debug                           = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY']            = 'some_secret_key'

app.config['UPLOAD_FOLDER']         = UPLOAD_FOLDER
app.config['RESULT_FOLDER']         = RESULT_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_developer(filename, developer_class: FilmDeveloper) -> FilmDeveloper:
    developer = developer_class(
        filename,
        'png',
        UPLOAD_FOLDER,
        RESULT_FOLDER
    )

    return developer


def home_page():
    return render_template(HOME_PAGE)


def developer_page(page, developer_class):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('no file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('no selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            developer = get_developer(filename, developer_class)
            developer.execute()
            path = f'./{RESULT_FOLDER}/{developer.result_filename}'
            # return send_file(path_or_file=path, as_attachment=True)
            return redirect(url_for('get_result_file', filename=developer.result_filename))
    return render_template(page)


@app.route('/')
def index():
    return home_page()


@app.route('/black_and_white', methods=['GET', 'POST'])
def upload_black_and_white_film():
    return developer_page(UPLOAD_PAGE, FilmDeveloperBW)


@app.route('/color', methods=['GET', 'POST'])
def upload_color_film():
    return developer_page(UPLOAD_PAGE, FilmDeveloperColor)


@app.route('/result/<filename>')
def get_result_file(filename):
    result = os.path.join(app.root_path, app.config['RESULT_FOLDER'])
    return send_from_directory(directory=result, path=filename)




if __name__ == '__main__':
    app.run()
