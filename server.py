from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trustpoint.db'
db = SQLAlchemy(app)

class UserActivity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    activity_type = db.Column(db.String(50))
    activity_data = db.Column(db.Text)

class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    info_type = db.Column(db.String(50))
    info_data = db.Column(db.Text)

@app.route('/api/activity', methods=['POST'])
def log_activity():
    data = request.json
    activity = UserActivity(activity_type=data['type'], activity_data=data['data'])
    db.session.add(activity)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

@app.route('/api/system_info', methods=['POST'])
def log_system_info():
    data = request.json
    info = SystemInfo(info_type=data['type'], info_data=data['data'])
    db.session.add(info)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

@app.route('/')
def dashboard():
    activities = UserActivity.query.order_by(UserActivity.timestamp.desc()).all()
    system_infos = SystemInfo.query.order_by(SystemInfo.timestamp.desc()).all()
    return render_template('dashboard.html', activities=activities, system_infos=system_infos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)