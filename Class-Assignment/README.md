# Hands-on Task: Run and Manage a "Hello Web App" (httpd)

## Objective

Deploy and manage a simple Apache-based web server on Kubernetes and:

- Verify it is running
- Modify it
- Scale it
- Debug it
- Observe self-healing

---

## Prerequisites

- A running Kubernetes cluster (e.g., Minikube, kind, or any cloud cluster)
- `kubectl` installed and configured
- Basic familiarity with the terminal

---

##  Task 1: Deploy a Simple Web Application (Apache httpd)

> You will run an Apache server instead of nginx.

---

### Step 1: Run a Pod

```bash
kubectl run apache-pod --image=httpd
```

**Check that the pod is running:**

```bash
kubectl get pods
```

Expected output:

```
NAME         READY   STATUS    RESTARTS   AGE
apache-pod   1/1     Running   0          10s
```

---

### Step 2: Inspect Pod

```bash
kubectl describe pod apache-pod
```

**Focus on:**

- `container image` = `httpd`
- `ports` (default 80)
- `events` (for any errors or pull issues)

---

### Step 3: Access the App

Forward the pod's port to your local machine:

```bash
kubectl port-forward pod/apache-pod 8081:80
```

Open in your browser:

```
http://localhost:8081
```

> ✅ You should see: → Apache default page **("It works!")**

---

### Step 4: Delete Pod

```bash
kubectl delete pod apache-pod
```

> 💡 **Insight:** Same as before — the pod **disappears permanently**. There is **no self-healing** because a bare pod has no controller managing it.

---

## 🔄 Task 2: Convert to Deployment

---

### Step 5: Create Deployment

```bash
kubectl create deployment apache --image=httpd
```

**Check:**

```bash
kubectl get deployments
kubectl get pods
```

Expected output:

```
NAME     READY   UP-TO-DATE   AVAILABLE   AGE
apache   1/1     1            1           15s
```

---

### Step 6: Expose Deployment

Create a NodePort service to expose the deployment:

```bash
kubectl expose deployment apache --port=80 --type=NodePort
```

**Access again via port-forward:**

```bash
kubectl port-forward service/apache 8082:80
```

**Open:**

```
http://localhost:8082
```

---

## Task 3: Modify Behavior

---

### Step 7: Scale Deployment

Scale the deployment to 2 replicas:

```bash
kubectl scale deployment apache --replicas=2
```

**Check:**

```bash
kubectl get pods
```

Expected output:

```
NAME                      READY   STATUS    RESTARTS   AGE
apache-xxxxxxxxx-aaaaa    1/1     Running   0          1m
apache-xxxxxxxxx-bbbbb    1/1     Running   0          10s
```

>  **Observe:** Multiple pods running the same app — this is horizontal scaling in action!

---

### Step 8: Test Load Distribution (Basic)

Run port-forward again and refresh your browser multiple times:

```bash
kubectl port-forward service/apache 8082:80
```

> *(Advanced later: check logs + serve different content per pod to see which pod handled the request)*

---

##  Task 4: Debugging Scenario

---

### Step 9: Break the App

Intentionally set a wrong container image to simulate a misconfiguration:

```bash
kubectl set image deployment/apache httpd=wrongimage
```

**Check pod status:**

```bash
kubectl get pods
```

You will see pods entering an error state (e.g., `ImagePullBackOff` or `ErrImagePull`).

---

### Step 10: Diagnose

Inspect the broken pod:

```bash
kubectl describe pod <pod-name>
```

**Look for:**

- `ImagePullBackOff` status
- Error messages under the `Events` section (e.g., `Failed to pull image "wrongimage"`)

---

### Step 11: Fix It

Restore the correct image:

```bash
kubectl set image deployment/apache httpd=httpd
```

Kubernetes will automatically roll out the fix and replace broken pods with healthy ones.

---

##  Task 5: Explore Inside Container (Important Skill)

---

### Step 12: Exec into Pod

Open an interactive shell inside a running pod:

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

**Once inside the container:**

```bash
ls /usr/local/apache2/htdocs
```

>  This is where web files are stored. You'll find `index.html` here.

**Exit the container shell:**

```bash
exit
```

---

## Task 6: Observe Self-Healing

---

### Step 13: Delete One Pod

```bash
kubectl delete pod <one-pod-name>
```

**Watch Kubernetes automatically recreate it:**

```bash
kubectl get pods -w
```

Expected behavior:

```
NAME                      READY   STATUS        RESTARTS   AGE
apache-xxxxxxxxx-aaaaa    1/1     Terminating   0          5m
apache-xxxxxxxxx-ccccc    0/1     Pending       0          2s
apache-xxxxxxxxx-ccccc    1/1     Running       0          5s
```

>  **Insight:** Unlike bare pods, **Deployments recreate pods automatically**. This is Kubernetes self-healing in action — the desired state (2 replicas) is always maintained.

---

## Task 7: Cleanup

Remove all resources created during this task:

```bash
kubectl delete deployment apache
kubectl delete service apache
```

---

## Optional Next Challenge: Modify Container at Runtime

Exec into a running pod and serve custom HTML content:

```bash
kubectl exec -it <pod-name> -- /bin/bash
```

Then run inside the container:

```bash
echo "Hello from Kubernetes" > /usr/local/apache2/htdocs/index.html
```

Exit and refresh your browser — you should now see:

```
Hello from Kubernetes
```

>  **Note:** Changes made this way are **not persistent**. If the pod restarts, the default page will return. To make changes permanent, use a `ConfigMap` or a custom Docker image.

---

## Summary of Commands

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `kubectl run apache-pod --image=httpd` | Run a bare pod |
| 2 | `kubectl get pods` | List pods |
| 3 | `kubectl describe pod apache-pod` | Inspect pod details |
| 4 | `kubectl port-forward pod/apache-pod 8081:80` | Access pod locally |
| 5 | `kubectl delete pod apache-pod` | Delete pod |
| 6 | `kubectl create deployment apache --image=httpd` | Create deployment |
| 7 | `kubectl expose deployment apache --port=80 --type=NodePort` | Expose as service |
| 8 | `kubectl port-forward service/apache 8082:80` | Access service locally |
| 9 | `kubectl scale deployment apache --replicas=2` | Scale to 2 pods |
| 10 | `kubectl set image deployment/apache httpd=wrongimage` | Break the app |
| 11 | `kubectl describe pod <pod-name>` | Diagnose errors |
| 12 | `kubectl set image deployment/apache httpd=httpd` | Fix the app |
| 13 | `kubectl exec -it <pod-name> -- /bin/bash` | Shell into container |
| 14 | `kubectl delete pod <pod-name>` | Trigger self-healing |
| 15 | `kubectl get pods -w` | Watch pods live |
| 16 | `kubectl delete deployment apache` | Cleanup deployment |
| 17 | `kubectl delete service apache` | Cleanup service |

---
