from flask import Flask, render_template, redirect, url_for
import datetime
import random

app = Flask(__name__)

deployments = [
    {
        "project": "Frontend Service",
        "status": "Success",
        "time": "10:15 AM"
    },
    {
        "project": "Auth Service",
        "status": "Running",
        "time": "11:00 AM"
    },
    {
        "project": "Payment Service",
        "status": "Failed",
        "time": "11:30 AM"
    }
]

pods = [
    "frontend-pod",
    "backend-pod",
    "database-pod"
]

@app.route('/')
def dashboard():
    return render_template(
        'index.html',
        deployments=deployments,
        pods=pods
    )

@app.route('/deploy')
def deploy():

    services = [
        "Frontend Service",
        "Backend API",
        "Auth Service",
        "Notification Service",
        "Payment Service"
    ]

    statuses = [
        "Success",
        "Running",
        "Failed"
    ]

    new_deployment = {
        "project": random.choice(services),
        "status": random.choice(statuses),
        "time": datetime.datetime.now().strftime("%I:%M %p")
    }

    deployments.insert(0, new_deployment)

    return redirect(url_for('dashboard'))

@app.route('/pipelines')
def pipelines():
    return render_template(
        'pipelines.html',
        deployments=deployments
    )

@app.route('/containers')
def containers():
    return render_template(
        'containers.html',
        pods=pods
    )

@app.route('/kubernetes')
def kubernetes():
    return render_template(
        'kubernetes.html',
        pods=pods
    )

@app.route('/infrastructure')
def infrastructure():
    return render_template('infrastructure.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)