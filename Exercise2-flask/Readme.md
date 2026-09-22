Exercise 2: Deploy Flask App on Minikube

Objective

Deploy a simple Flask application on Kubernetes using Minikube, Docker,
and kubectl.

Project Structure

Exercise2-flask/
├── app.py
├── Dockerfile
└── flask-deployment.yaml

1. Start Minikube

minikube start

2. Create Flask Application

app.py

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello from Flask on Kubernetes!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=15000)

3. Create Dockerfile

FROM python:3.8-slim
WORKDIR /app
COPY . /app
RUN pip install flask
CMD ["python", "app.py"]

4. Build Docker Image

For Windows CMD:

@FOR /f "tokens=*" %i IN ('minikube -p minikube docker-env --shell cmd') DO @%i
docker build -t flask-app .

5. Create Kubernetes Deployment

flask-deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-app
          image: flask-app:latest
          imagePullPolicy: Never
          ports:
            - containerPort: 15000

---
apiVersion: v1
kind: Service
metadata:
  name: flask-app-service
spec:
  selector:
    app: flask-app
  ports:
    - port: 15000
      targetPort: 15000
  type: NodePort

6. Deploy Application

kubectl apply -f flask-deployment.yaml

7. Check Deployment

kubectl get deployments

8. Check Pods

kubectl get pods -l app=flask-app

9. Check Logs

kubectl logs <pod-name>

10. Check Services

kubectl get services

11. Access the Application

minikube service flask-app-service --url

Use the URL displayed by Minikube to access the Flask application.

Useful Commands

minikube status
kubectl get deployments
kubectl get pods
kubectl get services
kubectl describe deployment flask-app
kubectl apply -f flask-deployment.yaml
minikube service flask-app-service --url