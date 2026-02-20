# 🐍 Dockerizing a Python Application with pip Dependencies

## 🎯 Objective
To create a Dockerfile that runs a Python script inside a container while installing required pip dependencies automatically.

---

## 🛠️ Tools & Technologies Used
- 🐳 Docker  
- 🐍 Python 3.11 (Alpine Linux Base Image)  
- 📦 pip (Python Package Manager)  
- 🔢 NumPy (External Dependency)  

---

## 📘 Overview
This experiment demonstrates how to containerize a Python application using Docker.  
The Dockerfile defines the runtime environment, installs required dependencies, copies the application file, and executes the script automatically when the container starts.

Using an Alpine-based image ensures a lightweight and efficient container.

---

## 📄 Dockerfile Configuration

```Dockerfile
FROM python:3.11.14-alpine3.23

WORKDIR /home

RUN pip install numpy

COPY app.py .

CMD ["python", "./app.py"]
```

### 🔎 Dockerfile Explanation
- `FROM` → Uses official lightweight Python base image  
- `WORKDIR` → Sets working directory inside container  
- `RUN` → Installs NumPy dependency  
- `COPY` → Copies application file into container  
- `CMD` → Executes Python script when container starts  

---

## 🧠 Application Code (app.py)

```python
import numpy as np  # dependency for learning purpose

stored_sapid = "500119597"

while True:
    user_sapid = input("Enter your SAP ID: ")
    if user_sapid == stored_sapid:
        print("Matched")
    else:
        print("Not Matched")
```

---

## ⚙️ Build and Run the Container

### 🏗️ Step 1: Build the Docker Image
```bash
docker build -t python-app:1.0 .
```

### ▶️ Step 2: Run the Docker Container
```bash
docker run --rm -it --name python-test python-app:1.0
```

### 🔎 Command Explanation
- `--rm` → Automatically removes container after exit  
- `-it` → Enables interactive terminal mode  
- `--name` → Assigns a custom name to the container  

---

## 📸 Workflow Screenshots

### 🔹 Docker Image Build Process  
![Docker Build](python_build.png)

### 🔹 Python Application Running Inside Container  
![Container Running](python_run1.png)  
![Container Running](python_run2.png)

---

## 📊 Result
- Successfully created Dockerfile for Python application  
- Installed NumPy dependency using pip  
- Built Docker image successfully  
- Executed Python script interactively inside container  
- Container removed automatically after stopping  

---

## 🏁 Conclusion
This experiment demonstrates how Docker can efficiently package Python applications along with their dependencies. Containerization ensures portability, consistency, and simplified deployment across different environments without manual configuration.
