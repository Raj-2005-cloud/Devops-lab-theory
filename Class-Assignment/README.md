# Apache Web Server Deployment on Kubernetes

## Objective
Deploy and manage a simple Apache-based web server using Kubernetes. The goal is to practice key DevOps tasks including:
- Verifying application status
- Modifying and scaling deployments
- Debugging container errors
- Exploring the container filesystem
- Observing self-healing capabilities

## Prerequisites
- Kubernetes cluster (Minikube, Docker Desktop, or cloud-based)
- kubectl installed and configured

## Steps Performed with Screenshots

### 1. Run a Pod
```bash
kubectl run apache-pod --image=httpd
kubectl get pods
