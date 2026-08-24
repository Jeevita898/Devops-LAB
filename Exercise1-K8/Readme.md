# Exercise 1 – Kubernetes Getting Started

## Objective

Deploy an Nginx web application as a Kubernetes Pod
and expose it using a NodePort Service.

## Technologies

- Docker
- Kubernetes
- Minikube
- kubectl
- Nginx

## Steps

### 1. Start Minikube

minikube start

### 2. Deploy the Pod

kubectl apply -f pod.yaml

### 3. Verify

kubectl get pods

### 4. Create the Service

kubectl apply -f service.yaml

### 5. Verify the Service

kubectl get services

### 6. Access the application

minikube service hello-k8s

## Result

The Nginx welcome page was successfully accessed through
the Kubernetes NodePort service.