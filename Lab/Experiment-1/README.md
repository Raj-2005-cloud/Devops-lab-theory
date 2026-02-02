# Experiment 1: Comparison of VMs and Containers

**Student Name:** RAJ VARDHAN SINGH  
**Date:** 24 JAN,2026

**SAP ID:** 500123753 

**Course:** Containerization and DevOps Lab

## 🎯 Objective
To understand the conceptual and practical differences between Virtual Machines and Containers by deploying Nginx in both environments.

## 📋 Part A: Virtual Machine Setup

### Step 1: Vagrant VM Creation
![Vagrant Init and Up](vagrant-up.png)
![Vagrant Init and Up](vagrant_2.png)
*Command: `vagrant up` creating Ubuntu VM*

### Step 2: Nginx Installation in VM
![Nginx in VM](nginx_1.png)
![Nginx in VM](nginx_2.png)
![Nginx in VM](nginx_3.png)
![Nginx in VM](nginx_4.png)
![Nginx in VM](nginx_5.png)
*Command: `sudo apt install nginx` and verification with `curl localhost`*

### Step 3: VM Resource Usage
![VM Resources](resource_2.png)
*Command: `free -h` showing memory usage in VM*

## 🐳 Part B: Container Setup

### Step 1: Docker Nginx Container
![Docker Run](container.png)
*Command: `docker run -d -p 8080:80 nginx`*

### Step 2: Container Verification
![Container Check](container.png)
*Command: `curl localhost:8080` verifying Nginx in container*

### Step 3: Container Resource Usage
![Docker Stats](resource_1.png)
*Command: `docker stats` showing container resource usage*

## ⚖️ Comparison Results

### Resource Utilization Table
| Parameter | Virtual Machine | Container |
|-----------|----------------|-----------|
| **Boot Time** | ~45 seconds | ~2 seconds |
| **RAM Usage** | 1.2 GB | 120 MB |
| **Disk Space** | 2.5 GB | 142 MB |
| **Isolation** | Full OS-level | Process-level |

### Screenshot Comparison
![Side-by-Side Comparison](resource_2.png)
![Side-by-Side Comparison](resource_1.png)

*Left: VM resources | Right: Container resources*

## 📊 Key Findings
1. Containers start **20x faster** than VMs
2. Containers use **90% less memory** than VMs
3. VMs provide stronger isolation but higher overhead
4. Containers are more efficient for microservices

## 🧪 Commands Used
```bash
# VM Commands
vagrant init ubuntu/jammy64
vagrant up
vagrant ssh
sudo apt install nginx

# Container Commands
docker pull nginx
docker run -d -p 8080:80 nginx
docker stats
