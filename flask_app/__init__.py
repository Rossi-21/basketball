from flask import Flask


app = Flask(__name__)

app.secret_key = "Something Very Special"
app.config['UPLOAD_FOLDER'] = '/Users/richardlyons/sports/basketball/uploads/'