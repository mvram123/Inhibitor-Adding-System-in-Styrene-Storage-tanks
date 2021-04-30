from flask import Flask
import boto3
from flask_sqlalchemy import SQLAlchemy

# Connecting to S3 Bucket
s3 = boto3.resource(service_name='s3',region_name='us-east-1',
                    aws_access_key_id='AKIAXMJLKRLJ6UNUYJKP',
                    aws_secret_access_key='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')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensor.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Sensor_data(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Integer)
    inhibitor_level = db.Column(db.Integer)
    temp_change = db.Column(db.Integer)
    diss_oxygen = db.Column(db.Integer)
    styrene_level = db.Column(db.Integer)

    # def __repr__(self):
    # return f'temperature {self.id}: ' + str(self.temperature)

    def temp_last30(self):
        a = [['DAYS', 'TEMPERATURE']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).temperature])
            count = count + 1
        return a

    def inhibitor_last30(self):
        a = [['DAYS', 'INHIBITOR LEVEL']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).inhibitor_level])
            count = count + 1

        return a

    def temp_change_last30(self):
        a = [['DAYS', 'TEMPERATURE CHANGE']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).temp_change])
            count = count + 1
        return a

    def diss_oxygen_last30(self):
        a = [['DAYS', 'DISSOLVED OXYGEN']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).diss_oxygen])
            count = count + 1
        return a

    def styrene_last30(self):
        a = [['DAYS', 'STYRENE LEVEL']]
        count = 1
        for i in range(self.query.count()-29, self.query.count()+1):
            a.append([count, self.query.get(i).styrene_level])
            count = count + 1
        return a


a = Sensor_data()
b = a.inhibitor_last30()
print(b)
print(type(b))
