# DevOps Hands-On Exercises

A collection of ten hands-on DevOps exercises covering containers, Kubernetes, Docker security and networking, CI/CD with Jenkins, and monitoring with Prometheus and Grafana. Each exercise lives in its own folder with the code, manifests and (where available) screenshots of the result.

## Exercises at a Glance

| # | Folder | Topic | Key Tools |
|---|--------|-------|-----------|
| 1 | [`Exercise1-K8`](./Exercise1-K8) | Run Nginx as a Pod and expose it with a NodePort Service | Kubernetes, Minikube, kubectl, Nginx |
| 2 | [`Exercise2-flask`](./Exercise2-flask) | Containerize a Flask app and deploy it on Minikube | Docker, Flask, Kubernetes Deployment |
| 3 | [`Exercise3-ScaleFlask`](./Exercise3-ScaleFlask) | Scale a flash-sale Flask app with a ReplicaSet, health probes and resource limits | Gunicorn, ReplicaSet, probes |
| 4 | [`Exercise4-DockerNetwork`](./Exercise4-DockerNetwork) | A REST API container for Docker networking practice | Docker, Flask |
| 5 | [`Exercise5-DockerSecurity`](./Exercise5-DockerSecurity) | Restrict a container with a custom AppArmor profile | Docker, AppArmor, Docker SDK for Python |
| 6 | [`Exercise6-RealTime`](./Exercise6-RealTime) | Real-time delivery monitoring and alerting | Prometheus, Grafana, Jenkins, prometheus-client |
| 7 | [`Exercise7-Jenkin`](./Exercise7-Jenkin) | Install Jenkins LTS in Docker and complete first-time setup | Docker, Jenkins |
| 8 | [`Exercise8-ShellScript`](./Exercise8-ShellScript) | Run a shell script as a Jenkins job | Bash, Jenkins |
| 9 | [`Exercise9-Pipeline`](./Exercise9-Pipeline) | Multi-stage Jenkins pipeline (Build, Test, Deploy) for a Flask app | Jenkins Pipeline, unittest |
| 10 | [`Exercise10-MultiNode`](./Exercise10-MultiNode) | Two microservices on a 3-node Minikube cluster with pod anti-affinity | Minikube multi-node, Deployments, Services |

## Repository Structure

```text
Devops/
├── README.md
├── Exercise1-K8/                 # Pod + NodePort Service (Nginx)
│   ├── pod.yaml
│   ├── service.yaml
│   └── Readme.md
├── Exercise2-flask/              # Flask app on Minikube
│   ├── app.py
│   ├── Dockerfile
│   ├── flask-deployment.yaml
│   └── Readme.md
├── Exercise3-ScaleFlask/         # ReplicaSet with probes and limits
│   ├── app.py
│   ├── Dockerfile
│   └── flashsale-replicaset.yaml
├── Exercise4-DockerNetwork/      # REST API for Docker networking
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── Exercise5-DockerSecurity/     # AppArmor-confined container
│   ├── app.py
│   ├── Dockerfile
│   ├── my-apparmor-profile
│   ├── apply_apparmor.py
│   └── test_restricted_actions.py
├── Exercise6-RealTime/           # Prometheus + Grafana monitoring
│   └── delivery_monitoring/
│       ├── delivery_metrics.py
│       ├── Dockerfile
│       ├── prometheus.yml
│       ├── alert_rules.yml
│       ├── Jenkinsfile
│       └── jenkins-docker/Dockerfile
├── Exercise7-Jenkin/             # Jenkins in Docker
│   └── Readme.md
├── Exercise8-ShellScript/        # Shell script for Jenkins
│   └── hello-world.sh
├── Exercise9-Pipeline/           # Multi-stage Jenkins pipeline
│   ├── app.py
│   ├── test_app.py
│   ├── requirements.txt
│   └── Jenkinsfile
└── Exercise10-MultiNode/         # Multi-node cluster, two services
    ├── product_catalog.py
    ├── shopping_cart.py
    ├── Dockerfile.product
    ├── Dockerfile.shopping
    ├── *_deployment.yaml
    ├── *_service.yaml
    └── Readme.md
```

## Prerequisites

| Tool | Needed for |
|------|-----------|
| [Docker](https://docs.docker.com/get-docker/) | All exercises |
| [Minikube](https://minikube.sigs.k8s.io/docs/start/) | Exercises 1, 2, 3, 10 |
| [kubectl](https://kubernetes.io/docs/tasks/tools/) | Exercises 1, 2, 3, 10 |
| Python 3.8+ | Running and testing the apps locally (Exercises 2, 4, 5, 9) |
| Linux host with AppArmor | Exercise 5 |
| A web browser | Jenkins, Prometheus and Grafana UIs |

## Exercise Details

### Exercise 1: Kubernetes Getting Started
Deploys an Nginx Pod (`pod.yaml`) and exposes it via a NodePort Service (`service.yaml`).

```bash
minikube start
kubectl apply -f pod.yaml
kubectl apply -f service.yaml
minikube service hello-k8s
```

### Exercise 2: Deploy a Flask App on Minikube
A Flask app listening on port `15000`, packaged in a Docker image and deployed with a Deployment plus a NodePort Service. The image is built inside Minikube's Docker daemon, so the manifest uses `imagePullPolicy: Never`.

```bash
minikube start
eval $(minikube docker-env)        # Windows CMD: see the exercise Readme
docker build -t flask-app .
kubectl apply -f flask-deployment.yaml
minikube service flask-app-service --url
```

### Exercise 3: Scaling a Flask App with a ReplicaSet
A "flash sale" Flask API served by Gunicorn with three endpoints: `/` (welcome), `/buy` (simulated checkout) and `/health`. Every response includes the pod hostname so you can see load being spread across replicas. The ReplicaSet runs 3 replicas with readiness and liveness probes on `/health` and CPU and memory requests and limits.

```bash
eval $(minikube docker-env)
docker build -t flashsale:1.0 .
kubectl apply -f flashsale-replicaset.yaml
kubectl get pods -l app=flashsale
```

### Exercise 4: Docker Networking
A minimal Flask REST API (`GET /about` on port `5001`) with pinned dependencies (`Flask==2.0.1`, `Werkzeug==2.0.3`). Use it as the workload when practicing user-defined bridge networks and container-to-container communication.

```bash
docker build -t rest-api .
docker network create my-network
docker run -d --name api --network my-network -p 5001:5001 rest-api
curl http://localhost:5001/about
```

### Exercise 5: Docker Security with AppArmor
Runs a Flask container under a custom AppArmor profile (`my-apparmor-profile`) that denies reads of `/etc/passwd` and `/etc/shadow`, denies `sys_admin`, and attempts to block `bash`.

- `apply_apparmor.py` starts the container with the profile and prints the applied security options.
- `test_restricted_actions.py` runs three checks: read `/etc/passwd`, read `/etc/shadow`, execute bash.

```bash
sudo apparmor_parser -r -W my-apparmor-profile
docker build -t flask-apparmor .
pip install docker
python apply_apparmor.py
python test_restricted_actions.py
```

> **Known limitation:** the test script notes that blocking bash execution is not yet fully effective with the current profile.

### Exercise 6: Real-Time Delivery Monitoring
A Python service (`delivery_metrics.py`) simulates deliveries and exposes Prometheus metrics on port `8000`: `total_deliveries`, `pending_deliveries`, `on_the_way_deliveries` and `average_delivery_time`. Prometheus scrapes it and evaluates two alert rules:

| Alert | Condition | Severity |
|-------|-----------|----------|
| `HighPendingDeliveries` | `pending_deliveries > 10` for 15s | warning |
| `HighAverageDeliveryTime` | average delivery time `> 30` | critical |

A Jenkins pipeline checks Docker, builds the image, runs the metrics app, then starts Prometheus (`:9090`) and Grafana (`:3000`). `jenkins-docker/Dockerfile` builds a Jenkins image with the Docker CLI installed so pipelines can run Docker commands.

```bash
cd delivery_monitoring
docker build -t delivery_metrics .
docker run -d -p 8000:8000 --name delivery_metrics delivery_metrics
docker run -d --name prometheus -p 9090:9090 \
  -v $(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/alert_rules.yml:/etc/prometheus/alert_rules.yml \
  prom/prometheus
docker run -d --name grafana -p 3000:3000 grafana/grafana
```

Then open Prometheus at http://localhost:9090 and Grafana at http://localhost:3000 and add Prometheus as a data source. Screenshots are in `Exercise6-RealTime/` (`metric.png`, `prometheus1.png`, `prometheus2.png`, `grafana.png`, `JenkinBuild.png`).

> The `Jenkinsfile` copies files from `/delivery_monitoring/`, and `prometheus.yml` targets `host.docker.internal:8000`. Adjust these paths and hostnames for your environment.

### Exercise 7: Installing Jenkins with Docker
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
docker exec -it jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
Open http://localhost:8080, unlock with the password, install the suggested plugins and create the admin user.

### Exercise 8: Shell Script for Jenkins
`hello-world.sh` prints `Hello, Jenkins!`. Used as the build step of a Jenkins Freestyle job (Execute shell). See `image.png` for the result.

### Exercise 9: Multi-Stage Jenkins Pipeline
A declarative pipeline for a Flask app:

1. **Build**: install dependencies from `requirements.txt`
2. **Test**: run `unittest` (`test_app.py` checks the `/` route)
3. **Deploy**: copy `app.py` and `requirements.txt` into `python-app-deploy/` in the workspace

Run the tests locally:
```bash
pip install -r requirements.txt
python -m unittest discover -s .
```

### Exercise 10: Multi-Node Kubernetes Cluster
Two Flask services on a 3-node Minikube profile (`devops-multinode`):

| Service | Replicas | Endpoint |
|---------|----------|----------|
| Product Catalog | 2 | `GET /products` |
| Shopping Cart | 3 | `GET /cart`, `POST /cart` |

Pod anti-affinity (`topologyKey: kubernetes.io/hostname`) forces each replica onto a different node.

```bash
minikube start --nodes 3 -p devops-multinode
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
kubectl apply -f product_catalog_deployment.yaml -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_service.yaml -f shopping_cart_service.yaml
kubectl get pods -o wide
```

## Cleanup

```bash
kubectl delete -f <manifest>.yaml     # remove Kubernetes resources
minikube delete --all                 # remove all Minikube clusters
docker rm -f $(docker ps -aq)         # remove all containers (use with care)
```

## Skills Demonstrated

- Containerization with Docker and Dockerfile best practices
- Kubernetes workloads: Pods, Deployments, ReplicaSets, Services
- Health probes, resource requests and limits, and pod anti-affinity
- Container security with AppArmor profiles
- CI/CD with Jenkins (Freestyle jobs and declarative pipelines)
- Metrics, alerting and dashboards with Prometheus and Grafana