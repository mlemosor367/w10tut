import os
import sys
import click

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from os.path import join, dirname, realpath

ALLOWED_EXTENSIONS = {'.csv'}
WIN = sys.platform.startswith('win')
if WIN:
    prefixdb = 'sqlite:///'
else:
    prefixdb = 'sqlite:////'

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# init Db
app.config["SQLALCHEMY_DATABASE_URI"] = prefixdb + os.path.join(app.root_path, 'Weather.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# enable debugging mode
app.config["DEBUG"] = True

# Upload folder
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/user/<name>')
def user(name):
    # return '<h1>hello ! {}</h1>'.format(name)
    return render_template('user.html', name=name)


# upload
@app.route('/upload')
def upload():
    return render_template('upload.html')


# display
@app.route('/display')
def display():
    print("Total number of records in Weather table is", Weather.query.count())
    count = Weather.query.count()
    rs_weather = Weather.query.all()
    return render_template('display.html', count=count, rset=rs_weather)


# Root URL
@app.route('/')
def index():
    # Set The upload HTML template '\templates\index.html'
    return render_template('index.html')


# allow only .csv files
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Get the uploaded files
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SensorID = db.Column(db.String(100), nullable=False)
    Temperature = db.Column(db.Integer, nullable=False)
    Humidity = db.Column(db.Integer, nullable=False)
    Preassure = db.Column(db.Integer, nullable=False)
    MessageTimeStamp = db.Column(db.String(100), nullable=False)
    GatewayID = db.Column(db.String(100), nullable=False)
    GatewayTimeStamp = db.Column(db.Float, nullable=False)


@app.route("/upload", methods=['POST'])
def uploadFiles():
    # get the uploaded file
    uploaded_file = request.files['file']
    print(uploaded_file)
    # if not allowed_file(uploaded_file):
    #    print("not valid extension on {}".format(uploaded_file))
    #    return redirect(request.url)
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        # set the file path
        uploaded_file.save(file_path)
        # save the file
        # read a file and upload the info to db
        with open(file_path) as f:
            contents = f.readlines()
            count = 0
            for line in contents:
                if count == 0:
                    count += 1
                else:
                    count += 1
                    print("Line{}: {}".format(count, line.strip()))
                    l = line.split(",")
                    w = Weather(SensorID=l[0], Temperature=l[1], Humidity=l[2], Preassure=l[3], MessageTimeStamp=l[4],
                                GatewayID=l[5], GatewayTimeStamp=l[6])
                    db.session.add(w)
                    print("l is:", l)
        db.session.commit()
        f.close()
    return redirect(url_for('index'))


@app.cli.command('display_counter')
def display_counter():
    print("Total number of records in Weather table is", Weather.query.count())
    


if __name__ == "__main__":
    app.run(port=5000)
