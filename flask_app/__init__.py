from flask import Flask


UPLOAD_FOLDER = '/Users/Ross/Documents/Python/flask_mysql/basketball/flask_app/uploads'


app = Flask(__name__)

app.secret_key = "Something Very Special"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER