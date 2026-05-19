from flask import Flask, render_template, redirect, url_for
import datetime
import random
import subprocess
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
logs = [
    "[INFO] Jenkins pipeline initialized",
    "[INFO] Docker engine connected",
    "[INFO] Kubernetes cluster active",
    "[INFO] Minikube running successfully"
]

deployments = [
    {
        "project": "Frontend Service",
        "status": "Success",
        "time": "10:15 AM"
    }
]

def get_kubernetes_pods():

    try:
        output = subprocess.check_output(
            "kubectl get pods --no-headers",
            shell=True
        ).decode("utf-8")

        pod_lines = output.strip().split("\n")

        pods = []

        for line in pod_lines:
            if line:
                pods.append(line.split()[0])

        return pods

    except:
        return ["Kubernetes not running"]

def get_docker_containers():

    try:
        output = subprocess.check_output(
            "docker ps --format \"{{.Names}}\"",
            shell=True
        ).decode("utf-8")

        containers = output.strip().split("\n")

        if containers == ['']:
            return ["No running containers"]

        return containers

    except:
        return ["Docker not running"]

def get_minikube_status():

    try:
        output = subprocess.check_output(
            "minikube status",
            shell=True
        ).decode("utf-8")

        if "Running" in output:
            return "Running"

        return "Stopped"

    except:
        return "Not Available"

@app.route('/')
def dashboard():

    pods = get_kubernetes_pods()

    containers = get_docker_containers()

    minikube_status = get_minikube_status()

    return render_template(
        'index.html',
        deployments=deployments,
        pods=pods,
        containers=containers,
        minikube_status=minikube_status,
	logs=logs
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
    logs.insert(0, "[INFO] New deployment triggered successfully")

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)