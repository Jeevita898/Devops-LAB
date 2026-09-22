Multi-Node Kubernetes Cluster with Multiple Applications

Objective

Deploy two Flask applications on a 3-node Minikube cluster:

Product Catalog --- 2 replicas

Shopping Cart --- 3 replicas

The replicas are distributed across different nodes using pod
anti-affinity.

Project Structure

Exercise10-MultiNode/
├── product_catalog.py
├── shopping_cart.py
├── Dockerfile.product
├── Dockerfile.shopping
├── product_catalog_deployment.yaml
├── shopping_cart_deployment.yaml
├── product_catalog_service.yaml
└── shopping_cart_service.yaml

Step 1: Clean Existing Minikube

minikube stop
minikube delete

Step 2: Create Multi-Node Minikube Cluster

minikube start --nodes 3 -p devops-multinode --force

Enable the registry addon:

minikube -p devops-multinode addons enable registry

Step 3: Product Catalog Application

product_catalog.py

from flask import Flask, jsonify

app = Flask(__name__)

products = [
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Headphones", "price": 150},
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

Step 4: Shopping Cart Application

shopping_cart.py

from flask import Flask, jsonify, request

app = Flask(__name__)

cart = []

@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)

@app.route("/cart", methods=["POST"])
def add_to_cart():
    item = request.json
    cart.append(item)
    return jsonify(cart), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)

Step 5: Dockerize Applications

Dockerfile.product

FROM python:3.9-slim
WORKDIR /app
COPY product_catalog.py /app/
RUN pip install flask
CMD ["python", "product_catalog.py"]

Dockerfile.shopping

FROM python:3.9-slim
WORKDIR /app
COPY shopping_cart.py /app/
RUN pip install flask
CMD ["python", "shopping_cart.py"]

Build the images:

docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .

Step 6: Load Images into Minikube

minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest

Verify:

minikube -p devops-multinode ssh -- docker images

Step 7: Product Catalog Deployment

product_catalog_deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: product-catalog
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      app: product-catalog
  template:
    metadata:
      labels:
        app: product-catalog
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: product-catalog
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: product-catalog-container
        image: product-catalog:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 80

Step 8: Shopping Cart Deployment

shopping_cart_deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: shopping-cart
  namespace: default
spec:
  replicas: 3
  selector:
    matchLabels:
      app: shopping-cart
  template:
    metadata:
      labels:
        app: shopping-cart
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchLabels:
                app: shopping-cart
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: shopping-cart-container
        image: shopping-cart:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 80

Apply both deployments:

kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml

Step 9: Create Services

product_catalog_service.yaml

apiVersion: v1
kind: Service
metadata:
  name: product-catalog-service
  namespace: default
spec:
  selector:
    app: product-catalog
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort

shopping_cart_service.yaml

apiVersion: v1
kind: Service
metadata:
  name: shopping-cart-service
  namespace: default
spec:
  selector:
    app: shopping-cart
  ports:
    - protocol: TCP
      port: 80
      targetPort: 80
  type: NodePort

Apply the services:

kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml

Step 10: Verify Pods

kubectl get pods -o wide

The Product Catalog should have 2 pods and Shopping Cart should have 3
pods distributed across the nodes.

Step 11: Access Product Catalog

minikube -p devops-multinode service product-catalog-service

Test:

curl http://127.0.0.1:<port>/products

Expected response:

[
    {"id": 1, "name": "Laptop", "price": 1200},
    {"id": 2, "name": "Phone", "price": 800},
    {"id": 3, "name": "Headphones", "price": 150}
]

Step 12: Access Shopping Cart

minikube -p devops-multinode service shopping-cart-service

Get the cart:

curl http://127.0.0.1:<port>/cart

Expected:

[]

Add an item:

curl -X POST http://127.0.0.1:<port>/cart -H "Content-Type: application/json" -d '{"id": 1, "name": "Laptop", "quantity": 1}'

Expected:

[
    {"id": 1, "name": "Laptop", "quantity": 1}
]

Useful Commands

minikube status
kubectl get nodes
kubectl get deployments
kubectl get pods -o wide
kubectl get services
kubectl apply -f <file.yaml>
minikube -p devops-multinode service <service-name>

Result

Two Flask applications are deployed on a 3-node Minikube cluster with:

Product Catalog: 2 replicas

Shopping Cart: 3 replicas

Pod anti-affinity for distribution across nodes

NodePort services for accessing both applications