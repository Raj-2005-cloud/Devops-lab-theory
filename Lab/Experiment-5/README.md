
## Volumes, Environment Variables, Monitoring & Networks


---

## Part 1: Docker Volumes - Persistent Data Storage

### Lab 1: Understanding Data Persistence

#### The Problem: Container Data is Ephemeral

```bash
# Create a container and add data
docker run -it --name test-container ubuntu /bin/bash
echo "Hello World" > message.txt
cat message.txt
exit

# Remove the container
docker stop test-container
docker rm test-container

# Data is lost when container is removed
docker run -it --name test-container ubuntu /bin/bash
cat message.txt
# cat: message.txt: No such file or directory
```

#### Anonymous Volumes

```bash
# Create container with anonymous volume
docker run -d -v /app/data --name web1 nginx

# List all volumes
docker volume ls

# Inspect volume mounts
docker inspect web1 | grep -A 5 Mounts
```

### Lab 2: Volume Types

#### 1. Named Volumes

```bash
# Create a named volume
docker volume create mydata

# Use named volume in container
docker run -d -v mydata:/app/data --name web2 nginx

# Inspect volume
docker volume ls
docker volume inspect mydata

# Mount host directory as volume
docker run -d -v ~/myapp-data:/app/data --name web3 nginx
```

#### 2. Bind Mounts (Host Directory)

```bash
# Create host directory
mkdir myapp-data

# Bind mount to container
docker run -d -v $(pwd)/myapp-data:/app/data --name web3 nginx

# Create file on host
echo "From Host" > myapp-data/host-file.txt

# Verify in container
docker exec -it web3 bash
ls /app/data
cat /app/data/host-file.txt
# From Host
exit

# Database with named volume
docker run -d \
  --name mysql-db \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0
```

### Lab 3: Practical Volume Examples

#### Example 1: Database with Persistent Storage

```bash
# Clean up existing container
docker stop mysql-db
docker rm mysql-db

# Create new MySQL with persistent volume
docker run -d \
  --name new-mysql \
  -v mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  mysql:8.0

# Create custom nginx config directory
mkdir ~/nginx-config

# Create custom nginx configuration
echo 'server {
    listen 80;
    server_name localhost;
    location / {
        return 200 "Hello from mounted config!";
    }
}' > ~/nginx-config/nginx.conf

# Run nginx with mounted config
docker run -d \
  --name nginx-custom \
  -p 8080:80 \
  -v ~/nginx-config/nginx.conf:/etc/nginx/conf.d/default.conf \
  nginx
```

#### Example 2: Web App with Configuration Files

```bash
# Test the configuration
curl http://localhost:8080
# Hello from mounted config!

# Create app volume
docker volume create app-volume
docker volume inspect app-volume

# Prune unused volumes
docker volume prune
# Deleted Volumes listed
# Total reclaimed space: 246.1MB
```

---

## Part 2: Environment Variables

### Lab 1: Setting Environment Variables

#### Method 1: Using `-e` flag

```bash
# Remove existing container if needed
docker rm -f app11

# Run container with environment variables
docker run -d \
  --name app11 \
  -e DATABASE_URL="postgres://user:pass@db:5432/mydb" \
  -e DEBUG="true" \
  -p 3005:3000 \
  nginx

# Verify environment variables
docker exec -it app11 bash
env | grep DATABASE
# DATABASE_URL=postgres://user:pass@db:5432/mydb
env | grep DEBUG
# DEBUG=true
exit

# Clean up
docker rm -f app11
```

#### Method 2: Using `--env-file`

```bash
# Create environment file directory
mkdir env-lab
cd env-lab

# Create .env file
echo "DATABASE_HOST=localhost" > .env
echo "DATABASE_PORT=5432" >> .env
echo "API_KEY=secret123" >> .env

# View the file
cat .env
# DATABASE_HOST=localhost
# DATABASE_PORT=5432
# API_KEY=secret123

# Run container with env file
docker run -d --name app22 --env-file .env nginx

# Verify environment variables
docker exec -it app22 bash
echo $DATABASE_HOST
# localhost
echo $DATABASE_PORT
# 5432
echo $API_KEY
# secret123
exit

# Clean up
docker rm -f app22
cd ..
```

### Lab 2: Flask App with Environment Variables

#### Create Flask Application

```bash
# Create project directory
mkdir flask-env-app
cd flask-env-app

# Create requirements.txt
echo "flask" > requirements.txt
```

#### `app.py` - Flask Application

```python
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/config')
def config():
    return jsonify({
        'db_host': os.environ.get('DATABASE_HOST', 'localhost'),
        'debug': os.environ.get('DEBUG', 'false').lower() == 'true',
        'has_api_key': bool(os.environ.get('API_KEY'))
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .

CMD ["python", "app.py"]
```

#### Build and Run

```bash
# Build the image
docker build -t flask-env-app .

# Run with environment variables
docker run -d \
  --name flask1 \
  -p 5001:5000 \
  -e DATABASE_HOST=mydb \
  -e DEBUG=true \
  -e API_KEY=supersecret \
  flask-env-app
```

### Lab 3: Test Environment Variables

```bash
# Test in browser or with curl
curl http://localhost:5001/config

# Expected output:
# {
#   "db_host": "mydb",
#   "debug": true,
#   "has_api_key": true
# }
```

---

## Part 3: Docker Monitoring

### Lab 1: `docker stats` - Real-time Container Metrics

```bash
# Real-time stats (press Ctrl+C to exit)
docker stats

# Single snapshot
docker stats --no-stream

# JSON format output
docker stats --format json --no-stream

# No truncation of IDs
docker stats --no-stream --no-trunc
```

**Sample Output:**
```
CONTAINER ID  NAME             CPU%   MEM USAGE/LIMIT      MEM%   NET I/O          BLOCK I/O        PIDs
e3d6ecfd0537  nginx-custom     0.00%  13.26MiB / 7.61GiB  0.17%  2.8kB / 1.21kB   0B / 4.1kB       17
400c92a389aa  new-mysql        1.28%  349.6MiB / 7.61GiB  4.49%  1.84kB / 126B    65.5kB / 15.1MB  37
```

### Lab 2: `docker top` - Process Monitoring

```bash
# Create test container
docker rm -f monitor-test
docker run -d --name monitor-test -p 8090:80 nginx

# View processes in container
docker top monitor-test

# View with extended details
docker top monitor-test -ef

# Sample output:
# UID   PID   PPID  C  STIME  TTY  TIME      CMD
# root  3944  3920  0  14:30  ?    00:00:00  nginx: master process nginx -g daemon off;
# statd 3989  3944  0  14:30  ?    00:00:00  nginx: worker process
```

### Lab 3: `docker logs` - Application Logs

```bash
# View all logs
docker logs monitor-test

# View last 100 lines
docker logs --tail 100 monitor-test

# Show timestamps
docker logs -t monitor-test

# Logs from last 5 minutes
docker logs --since 5m monitor-test

# Follow logs (real-time)
docker logs -f monitor-test

# Combine options
docker logs -f --tail 50 -t monitor-test
```

### Lab 4: Container Inspection

```bash
# Full container inspection
docker inspect monitor-test

# Get specific configuration
docker inspect --format='{{.Config.Env}}' monitor-test

# Get memory limit
docker inspect --format='{{.HostConfig.Memory}}' monitor-test

# Get CPU limit
docker inspect --format='{{.HostConfig.NanoCpus}}' monitor-test

# Monitor Docker events
docker events

# Filter events by type
docker events --filter 'type=container'
```

### Lab 5: Practical Monitoring Script

#### `monitor.sh`

```bash
#!/bin/bash

echo "=== Docker Monitoring Dashboard ==="
echo "Time: $(date)"
echo
echo "1. Running Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo
echo "2. Resource Usage:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
echo
echo "3. Recent Events:"
docker events --since 1m --until 0s 2>/dev/null || echo "No recent events"
echo
echo "4. System Info:"
docker system df
```

```bash
# Make script executable
chmod +x monitor.sh

# Run monitoring script
./monitor.sh
```

**Sample Output:**
```
=== Docker Monitoring Dashboard ===
Time: Mon Mar 2 20:11:57 IST 2026

1. Running Containers:
NAMES            STATUS            PORTS
nginx-custom     Up 40 minutes     0.0.0.0:8080->80/tcp
new-mysql        Up 41 minutes     3306/tcp, 33060/tcp
web3             Up 45 minutes     80/tcp

2. Resource Usage:
NAME            CPU%   MEM USAGE/LIMIT      NET I/O           BLOCK I/O
nginx-custom    0.00%  13.26MiB/7.61GiB     3.01kB/1.21kB    0B/4.1kB
new-mysql       0.86%  349.6MiB/7.61GiB     2.05kB/126B      65.5kB/15.1MB

4. System Info:
TYPE          TOTAL  ACTIVE  SIZE      RECLAIMABLE
Images          24      15   6.887GB   3.065GB (44%)
Containers      36      7    1.872MB   1.311MB (70%)
Local Volumes   12      9    863.2MB   234.2MB (27%)
Build Cache     95      0    51.3MB    51.3MB
```

---

## Part 4: Docker Networks

### Lab 1: Bridge Network

```bash
# Clean up existing containers
docker rm -f web1 web2

# Create custom bridge network
docker network create my-network

# Run containers on custom network
docker run -d --name web1 --network my-network nginx
docker run -d --name web2 --network my-network nginx

# Test connectivity
docker exec web1 ping web2

# Inspect network
docker network inspect my-network
```

### Lab 2: Host Network

```bash
# Run container with host network
docker run -d --name host-app --network host nginx

# Access directly on host ports
curl http://localhost
# Note: May conflict with existing services
```

### Lab 3: None Network

```bash
# Run container with no network
docker run -d --name isolated-app --network none alpine sleep 3600

# Verify only loopback interface
docker exec isolated-app ifconfig
# Only lo interface present
```

### Lab 4: Network Management

```bash
# Connect container to network
docker network connect app-network web1

# Disconnect container from network
docker network disconnect app-network web1

# Remove network
docker network rm app-network

# Prune unused networks
docker network prune
```

### Lab 5: Multi-Container App - Web + Database

```bash
# Create application network
docker network create app-network

# Run PostgreSQL database
docker run -d \
  --name postgres-db \
  --network app-network \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15

# Run web application (example)
docker run -d \
  --name web-app \
  --network app-network \
  -p 8080:3000 \
  -e DATABASE_URL="postgres://postgres:secret@postgres-db:5432/mydb" \
  -e DATABASE_HOST="postgres-db" \
  node-app

# Inspect bridge network
docker network inspect bridge
```

### Lab 6: Port Publishing

```bash
# Publish specific port
docker run -d -p 80:8080 --name app1 nginx

# Publish random port
docker run -d -p 8080 --name app2 nginx

# Publish multiple ports
docker run -d -p 8082:80 -p 8443:443 --name app3 nginx

# Bind to specific host IP
docker run -d -p 127.0.0.1:8085:80 --name app4 nginx

# List networks
docker network ls
```

**Sample Network List:**
```
NETWORK ID    NAME           DRIVER   SCOPE
app-network   bridge         local
bridge        bridge         local
docker_gwbridge bridge       local
host          host           local
ingress       overlay        swarm
my-network    bridge         local
myapp-network bridge         local
```

---

## Part 5: Complete Real-World Example

### Flask + PostgreSQL + Redis Setup

#### Step 1: Create Network

```bash
# Create dedicated network
docker network create myapp-network
```

#### Step 2: Run Redis

```bash
docker run -d \
  --name redis \
  --network myapp-network \
  -v redis-data:/data \
  redis:7-alpine
```

#### Step 3: Run PostgreSQL

```bash
docker run -d \
  --name postgres \
  --network myapp-network \
  -e POSTGRES_DB=myapp \
  -e POSTGRES_USER=appuser \
  -e POSTGRES_PASSWORD=secret \
  -v pgdata:/var/lib/postgresql/data \
  postgres:15
```

#### Step 4: Create Flask Application

```bash
# Create project structure
mkdir flask-app
cd flask-app
```

#### `app.py`

```python
import os
import redis
import psycopg2
from flask import Flask, jsonify
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Redis connection
redis_client = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'localhost'),
    port=6379,
    decode_responses=True
)

# PostgreSQL connection
def get_db_connection():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'myapp'),
        user=os.environ.get('DB_USER', 'appuser'),
        password=os.environ.get('DB_PASSWORD', 'secret')
    )

@app.route('/')
def home():
    return jsonify({
        'message': 'Hello from Flask!',
        'environment': os.environ.get('APP_ENV', 'development')
    })

@app.route('/visits')
def visits():
    # Increment visit count in Redis
    visits = redis_client.incr('visits')
    return jsonify({'visits': visits})

@app.route('/health')
def health():
    # Check database connection
    try:
        conn = get_db_connection()
        conn.close()
        db_status = 'healthy'
    except:
        db_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy',
        'database': db_status,
        'redis': 'healthy'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### `requirements.txt`

```
flask==2.3.0
redis==5.0.0
psycopg2-binary==2.9.6
```

#### `Dockerfile`

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
```

#### `.env.production`

```
SECRET_KEY=supersecretkey
APP_ENV=production
DB_HOST=postgres
DB_NAME=myapp
DB_USER=appuser
DB_PASSWORD=secret
REDIS_HOST=redis
```

#### Step 5: Build and Run Flask App

```bash
# Build the image
docker build -t flask-app:latest .

# Run Flask container
docker run -d \
  --name flask-app \
  --network myapp-network \
  -p 5001:5000 \
  --env-file .env.production \
  flask-app:latest
```

#### Step 6: Monitor All Services

```bash
# View running containers
docker ps

# Monitor resource usage
docker stats

# View logs for specific service
docker logs -f flask-app

# Inspect network connectivity
docker network inspect myapp-network

# Test the application
curl http://localhost:5001/
curl http://localhost:5001/visits
curl http://localhost:5001/health
```

**Final Running Containers:**
```
CONTAINER ID  IMAGE             STATUS            PORTS
82d8f44ec481  flask-app:latest  Up About a minute 0.0.0.0:5001->5000/tcp
c0e7a059f3da  redis:7-alpine    Up 5 minutes      6379/tcp
3f89c6e81ba8  postgres:15       Up 5 minutes      5432/tcp
```

---

## Key Takeaways

### Volumes
- **Persist data** beyond container lifecycle
- **Named volumes** are preferred for production
- **Bind mounts** are good for development
- Always use `docker volume prune` to clean up unused volumes

### Environment Variables
- Use `-e` flag for single variables
- Use `--env-file` for multiple variables
- Never hardcode secrets in Dockerfiles
- Environment variables can override application config

### Monitoring
- `docker stats` for real-time resource usage
- `docker top` for process monitoring
- `docker logs` for application output
- `docker inspect` for detailed configuration
- `docker events` for system monitoring

### Networks
- **Bridge networks** for container-to-container communication
- **Host networks** for performance (no isolation)
- **None networks** for isolated containers
- **Custom networks** provide automatic DNS resolution
- Use `--network` flag to connect containers

### Best Practices

1. **Production Data**
   - Always use named volumes for production data
   - Regular volume backups
   - Monitor disk usage

2. **Configuration**
   - Use `.env` files for sensitive configuration
   - Don't commit `.env` files to version control
   - Use different env files per environment

3. **Monitoring**
   - Set up log rotation
   - Monitor resource limits
   - Use monitoring scripts for alerts

4. **Networking**
   - Create custom networks for each application
   - Use network isolation for security
   - Document network dependencies

---

## Quick Reference Commands

### Volumes
```bash
docker volume create <name>
docker volume ls
docker volume inspect <name>
docker volume rm <name>
docker volume prune
```

### Environment Variables
```bash
docker run -e KEY=value
docker run --env-file <file>
docker exec <container> env
```

### Monitoring
```bash
docker stats [container]
docker top <container>
docker logs [options] <container>
docker inspect <container>
docker events
docker system df
```

### Networks
```bash
docker network create <name>
docker network ls
docker network inspect <name>
docker network connect <network> <container>
docker network disconnect <network> <container>
docker network rm <name>
docker network prune
```

### Cleanup Commands
```bash
# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all unused resources
docker system prune -a

# Remove volumes
docker volume prune

# Remove networks
docker network prune
```

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| Port already allocated | Use different host port or remove conflicting container |
| Volume permission denied | Check volume mount permissions or use `:Z` flag on SELinux |
| Network not found | Create network before using it or check spelling |
| Container can't resolve hostname | Ensure containers are on same custom network |
| High memory usage | Set memory limits with `-m` flag |
| Logs too large | Implement log rotation in Docker daemon config |

---

## Summary

This experiment covered the four essential Docker concepts for production deployments:

1. **Volumes** → Persistent data storage
2. **Environment Variables** → Dynamic configuration
3. **Monitoring** → Observability and debugging
4. **Networks** → Secure container communication

Combined, these concepts enable building scalable, maintainable containerized applications ready for production deployment.
