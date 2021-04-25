# Importing Libraries
from flask import Flask, render_template, request
import boto3
from flask_sqlalchemy import SQLAlchemy

# Connecting to S3 Bucket
s3 = boto3.resource(service_name='s3', region_name='us-east-1',
                    aws_access_key_id='YOUR ACCESS KEY',
                    aws_secret_access_key='YOUR SECRET ACCESS KEY')

# Downloading csv with filename downloaded.csv
s3.Bucket('iotlab2021').download_file(Filename='manual.db',Key='manual.db')
s3.Bucket('iotlab2021').download_file(Filename='sensor.db',Key='sensor.db')

app = Flask(__name__)

# Databases
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///manual.db'
app.config['SQLALCHEMY_BINDS'] = {'sensor': 'sqlite:///sensor.db'}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Data(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer)
    inhibitor_level = db.Column(db.Integer)
    temp_change = db.Column(db.Integer)
    diss_oxygen = db.Column(db.Integer)
    styrene_level = db.Column(db.Integer)


class Sensor_data(db.Model):

    __bind_key__ = 'sensor'

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer)
    inhibitor_level = db.Column(db.Integer)
    temp_change = db.Column(db.Integer)
    diss_oxygen = db.Column(db.Integer)
    styrene_level = db.Column(db.Integer)

    # Returns temperature data from last 30 days
    def temp_last30(self):
        a = [['DAYS', 'TEMPERATURE']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).temperature])
            count = count + 1
        return a

    # Returns inhibitor proportion data from last 30 days
    def inhibitor_last30(self):
        a = [['DAYS', 'INHIBITOR LEVEL']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).inhibitor_level])
            count = count + 1
        return a

    # Returns temperature change data from last 30 days
    def temp_change_last30(self):
        a = [['DAYS', 'TEMPERATURE CHANGE']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).temp_change])
            count = count + 1
        return a

    # Returns dissolved oxygen percentage from last 30 days
    def diss_oxygen_last30(self):
        a = [['DAYS', 'DISSOLVED OXYGEN']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).diss_oxygen])
            count = count + 1
        return a

    # Returns styrene level data from last 30 days
    def styrene_last30(self):
        a = [['DAYS', 'STYRENE LEVEL']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).styrene_level])
            count = count + 1
        return a


@app.route('/')
def home():
    return render_template('index.html')

# For manually predicting the conditions
@app.route('/predict', methods=['POST'])
def predict():

    # Taking Inputs from form
    temperature = int(request.form['Temperature'])
    inhibitor_level = int(request.form['Inhibitor_level'])
    temp_change = int(request.form['Temp_change'])
    diss_oxygen = int(request.form['Diss_oxygen'])
    styrene_level = int(request.form['Styrene_level'])

    data = Data(temperature=temperature, inhibitor_level=inhibitor_level,
                temp_change=temp_change, diss_oxygen=diss_oxygen,
                styrene_level=styrene_level)

    # Adding data to manual.db database

    db.session.add(data)
    db.session.commit()

    # Initializing a variable
    a = ' '

    if temperature > 65:
        a = a + "Temperature greater than usual."
    if inhibitor_level < 10:
        a = a + ' ' + "Low Inhibitor Level."
    if temp_change > 3:
        a = a + ' ' + "High Temperature Change."
    if diss_oxygen < 3:
        a = a + ' ' + "Low Oxygen Level."
    if styrene_level < 100:
        a = a + ' ' + "Low Styrene Level."

    a = a + ' ' + "Evacuate !!"

    if data.query.count() % 30 == 0:
        s3.Bucket('iotlab2021').upload_file(Filename='manual.db', Key='manual.db')

    return render_template('predict.html', value=a)

# For Visualizing the sensor data
@app.route('/visualization', methods=['GET'])
def visualization():
    a = Sensor_data()
    temperature = a.temp_last30()
    inhibitor_level = a.inhibitor_last30()
    temp_change = a.temp_change_last30()
    diss_oxygen = a.diss_oxygen_last30()
    styrene_level = a.styrene_last30()

    return render_template('visualization.html', temperature=temperature, inhibitor_level=inhibitor_level,
                           temp_change=temp_change, diss_oxygen=diss_oxygen,
                           styrene_level=styrene_level)


if __name__ == '__main__':
    app.run(debug=True)
