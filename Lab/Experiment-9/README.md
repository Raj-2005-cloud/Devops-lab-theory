
  
# 🚀 Experiment 9 – Ansible Automation with Docker

**Course:** DevOps / Cloud Computing Lab  
**Objective:** Learn Ansible for automated server configuration management using Docker containers as managed nodes on **Windows**

</div>



## 🧠 Theory

### What is Ansible?

<div align="center">
  
```
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🔧 ANSIBLE – The Automation Engine                         ║
║                                                               ║
║   • Configuration Management   • Application Deployment      ║
║   • Orchestration              • Multi-server Workflows      ║
║                                                               ║
║   "Agentless • YAML-based • Idempotent • Push-based"         ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
  
</div>

### How Ansible Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                      CONTROL NODE (Your Windows PC)                         │
│                    ┌─────────────────────────┐                             │
│                    │   Ansible Installation   │                             │
│                    │   (WSL2 or Git Bash)     │                             │
│                    │   SSH Private Key        │                             │
│                    │   inventory.ini          │                             │
│                    │   playbooks/*.yml        │                             │
│                    └───────────┬─────────────┘                             │
│                                │                                            │
│                                │ SSH (Port 22)                              │
│                    ┌───────────┴────────────┐                              │
│                    │                        │                              │
│                    ▼                        ▼                              │
│         ┌──────────────────┐      ┌──────────────────┐                     │
│         │   MANAGED NODES   │      │   MANAGED NODES   │                     │
│         │                   │      │                   │                     │
│         │  ┌─────────────┐  │      │  ┌─────────────┐  │                     │
│         │  │  server1    │  │      │  │  server2    │  │                     │
│         │  │  ubuntu     │  │      │  │  ubuntu     │  │                     │
│         │  │  Docker     │  │      │  │  Docker     │  │                     │
│         │  └─────────────┘  │      │  └─────────────┘  │                     │
│         │                   │      │                   │                     │
│         │  ┌─────────────┐  │      │  ┌─────────────┐  │                     │
│         │  │  server3    │  │      │  │  server4    │  │                     │
│         │  │  ubuntu     │  │      │  │  ubuntu     │  │                     │
│         │  │  Docker     │  │      │  │  Docker     │  │                     │
│         │  └─────────────┘  │      │  └─────────────┘  │                     │
│         └──────────────────┘      └──────────────────┘                     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Key Components at a Glance

| 🧩 Component | 📝 Description | 🎯 Analogy |
|:------------|:---------------|:-----------|
| **Control Node** | Machine with Ansible installed (your Windows PC via WSL2) | 🎮 The Commander |
| **Managed Nodes** | Target servers — no agent needed | 🎯 The Targets |
| **Inventory** | `inventory.ini` — lists all nodes | 📋 Guest List |
| **Playbook** | YAML file with automation steps | 📜 Recipe Book |
| **Task** | Individual action in a playbook | 🥄 Single Step |
| **Module** | Built-in functions (`apt`, `copy`, etc.) | 🔧 Toolbox |
| **Role** | Reusable automation scripts | 📦 Pre-packaged Kit |

### Why Ansible Stands Out

<div align="center">

| ✨ Feature | 💡 Benefit |
|:----------|:-----------|
| **Agentless** | Uses SSH — no software needed on servers |
| **Idempotent** | Run playbooks multiple times safely |
| **Declarative** | Describe desired state, not the steps |
| **Push-based** | Control node initiates all changes |
| **YAML Syntax** | Human-readable, easy to learn |

</div>

---

## 🏛️ Architecture Overview

```
                         ┌─────────────────────────────────────────────────┐
                         │      🖥️  WINDOWS PC (Control Node)              │
                         │                                                 │
                         │  ┌─────────┐  ┌─────────┐  ┌─────────┐         │
                         │  │ Ansible │  │  SSH    │  │ Play-   │         │
                         │  │ (WSL2)  │  │  Key    │  │ books   │         │
                         │  └────┬────┘  └────┬────┘  └────┬────┘         │
                         │       │            │            │              │
                         │       └────────────┼────────────┘              │
                         │                    │                           │
                         └────────────────────┼───────────────────────────┘
                                              │
                            SSH (Port 22) 🔐   │
                                              │
              ┌───────────────────────────────┼───────────────────────────────┐
              │                               │                               │
              ▼                               ▼                               ▼
      ┌───────────────┐               ┌───────────────┐               ┌───────────────┐
      │   📦 server1   │               │   📦 server2   │               │   📦 server3   │
      │               │               │               │               │               │
      │  ┌─────────┐  │               │  ┌─────────┐  │               │  ┌─────────┐  │
      │  │ubuntu   │  │               │  │ubuntu   │  │               │  │ubuntu   │  │
      │  │22.04    │  │               │  │22.04    │  │               │  │22.04    │  │
      │  └─────────┘  │               │  └─────────┘  │               │  └─────────┘  │
      │  IP: x.x.x.3  │               │  IP: x.x.x.4  │               │  IP: x.x.x.5  │
      └───────────────┘               └───────────────┘               └───────────────┘
                                              │
                                              ▼
                                      ┌───────────────┐
                                      │   📦 server4   │
                                      │               │
                                      │  ┌─────────┐  │
                                      │  │ubuntu   │  │
                                      │  │22.04    │  │
                                      │  └─────────┘  │
                                      │  IP: x.x.x.6  │
                                      └───────────────┘
```

---

## 📋 Prerequisites (Windows)

<div align="center">

| ✅ Requirement | 🔍 How to Install | 💻 Check Command |
|:---------------|:------------------|:-----------------|
| **WSL2** (Windows Subsystem for Linux) | `wsl --install` in PowerShell (Admin) | `wsl -l -v` |
| **Ubuntu** on WSL2 | Install from Microsoft Store | `wsl -d Ubuntu` |
| **Docker Desktop** with WSL2 backend | [docker.com](https://docker.com) | `docker --version` |
| **Git for Windows** (includes Git Bash) | [git-scm.com](https://git-scm.com) | `git --version` |
| **VS Code** (recommended) | [code.visualstudio.com](https://code.visualstudio.com) | `code --version` |

</div>

### 🎯 Recommended Setup Approach

```
┌─────────────────────────────────────────────────────────────────┐
│                      WINDOWS 11 SETUP                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   🪟 Windows Host                                               │
│       │                                                         │
│       ├── 🐧 WSL2 - Ubuntu (Control Node)                       │
│       │       └── Ansible installed here                        │
│       │                                                         │
│       └── 🐳 Docker Desktop (with WSL2 backend)                 │
│               └── Ubuntu containers run here                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Part A – Setup & SSH Configuration

### Step 1: Launch WSL2 Ubuntu

```powershell
# In PowerShell (as Administrator)
wsl --update
wsl --set-default-version 2

# Launch Ubuntu
wsl -d Ubuntu
```

### Step 2: Install Ansible in WSL2

```bash
# Update package list
sudo apt update

# Install Ansible
sudo apt install ansible -y

# Verify installation
ansible --version
```

**Expected output:**
```
ansible [core 2.x.x]
  config file = /etc/ansible/ansible.cfg
  python version = 3.x.x
```

### Step 3: Generate SSH Key Pair

```bash
# 🔑 Generate RSA 4096-bit key pair
ssh-keygen -t rsa -b 4096
# Press Enter for all prompts (use default path, no passphrase)

# Create working directory
mkdir -p ~/ansible-exp9 && cd ~/ansible-exp9

# Copy keys to project directory
cp ~/.ssh/id_rsa.pub .
cp ~/.ssh/id_rsa .

# Verify
ls -la
```

**Key placement guide:**

| File | Location | Purpose |
|:-----|:---------|:--------|
| `id_rsa` (Private) | WSL2 (`~/.ssh/id_rsa`) | Used by Ansible/SSH to authenticate |
| `id_rsa.pub` (Public) | Docker container (`~/.ssh/authorized_keys`) | Grants access to matching private key |

---

### Step 4: Create the Dockerfile

```bash
cd ~/ansible-exp9
```

Create `Dockerfile`:

```dockerfile
FROM ubuntu:22.04

# Install required packages
RUN apt update -y && \
    apt install -y python3 python3-pip openssh-server && \
    apt clean

# Create SSH runtime directory
RUN mkdir -p /var/run/sshd

# Configure SSH for key-based authentication
RUN mkdir -p /run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config && \
    sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config

# Setup SSH directory and permissions
RUN mkdir -p /root/.ssh && \
    chmod 700 /root/.ssh

# Copy SSH keys
COPY id_rsa /root/.ssh/id_rsa
COPY id_rsa.pub /root/.ssh/authorized_keys

# Set proper permissions
RUN chmod 600 /root/.ssh/id_rsa && \
    chmod 644 /root/.ssh/authorized_keys

# Fix PAM for SSH login
RUN sed -i 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' /etc/pam.d/sshd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
```

---

### Step 5: Build Docker Image

```bash
# Build the custom ubuntu-server image
docker build -t ubuntu-server .

# Verify image was created
docker images | grep ubuntu-server
```

---

### Step 6: Test SSH with Single Container

```bash
# Start a test container
docker run -d --rm -p 2222:22 --name ssh-test-server ubuntu-server

# Get container IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-test-server

# Test SSH login with key (no password should be prompted)
ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no -p 2222 root@localhost

# Once logged in, verify
whoami
hostname

# Exit and stop
exit
docker stop ssh-test-server
```

---

## 🐳 Part B – Ansible with Docker Servers

### Step 7: Launch 4 Server Containers

```bash
for i in {1..4}; do
  echo -e "\n📦 Creating server${i}\n"
  docker run -d --rm -p 220${i}:22 --name server${i} ubuntu-server
  echo -e "📍 IP of server${i} is $(docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i})"
done

# Verify all 4 are running
docker ps
```

**Expected output:**
```
CONTAINER ID   IMAGE            NAMES      STATUS          PORTS
abc123...      ubuntu-server    server1    Up 5 seconds    0.0.0.0:2201->22/tcp
def456...      ubuntu-server    server2    Up 5 seconds    0.0.0.0:2202->22/tcp
ghi789...      ubuntu-server    server3    Up 5 seconds    0.0.0.0:2203->22/tcp
jkl012...      ubuntu-server    server4    Up 5 seconds    0.0.0.0:2204->22/tcp
```

---

### Step 8: Create Ansible Inventory

```bash
# Auto-generate inventory.ini with container IPs
echo "[servers]" > inventory.ini
for i in {1..4}; do
  docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' server${i} >> inventory.ini
done

# Add Ansible connection variables
cat << EOF >> inventory.ini

[servers:vars]
ansible_user=root
ansible_ssh_private_key_file=/home/$(whoami)/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
EOF

# Review the inventory
cat inventory.ini
```

**Expected `inventory.ini`:**
```ini
[servers]
172.17.0.3
172.17.0.4
172.17.0.5
172.17.0.6

[servers:vars]
ansible_user=root
ansible_ssh_private_key_file=/home/username/.ssh/id_rsa
ansible_python_interpreter=/usr/bin/python3
ansible_ssh_common_args='-o StrictHostKeyChecking=no'
```

---

### Step 9: Test Ansible Connectivity (Ping All)

```bash
# Disable host key checking
export ANSIBLE_HOST_KEY_CHECKING=False

# Ping all servers
ansible all -i inventory.ini -m ping
```

**Expected output:**
```json
172.17.0.3 | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3"
    },
    "changed": false,
    "ping": "pong"
}
172.17.0.4 | SUCCESS => { ... }
172.17.0.5 | SUCCESS => { ... }
172.17.0.6 | SUCCESS => { ... }
```

For verbose output (useful for debugging):
```bash
ansible all -i inventory.ini -m ping -vvv
```

---

## 📜 Playbooks

### Playbook 1: Update + Install Packages + Create File

Create `update.yml`:

```yaml
---
- name: 📦 Update and configure servers
  hosts: all
  become: yes

  tasks:
    - name: 🔄 Update apt packages
      apt:
        update_cache: yes
        upgrade: dist

    - name: 📥 Install required packages
      apt:
        name: ["vim", "htop", "wget", "curl"]
        state: present

    - name: 📝 Create test file
      copy:
        dest: /root/ansible_test.txt
        content: |
          ✅ Configured by Ansible
          📍 Server: {{ inventory_hostname }}
          🕐 Time: {{ ansible_date_time.time }}
          📅 Date: {{ ansible_date_time.date }}
```

### Playbook 2: Full Configuration with System Info

Create `playbook1.yml`:

```yaml
---
- name: ⚙️ Configure multiple servers
  hosts: servers
  become: yes

  tasks:
    - name: 🔄 Update apt package index
      apt:
        update_cache: yes

    - name: 🐍 Install Python 3 (latest)
      apt:
        name: python3
        state: latest

    - name: 📄 Create test file with content
      copy:
        dest: /root/test_file.txt
        content: |
          ═══════════════════════════════════════
          📋 SERVER CONFIGURATION REPORT
          ═══════════════════════════════════════
          
          🖥️  Server: {{ inventory_hostname }}
          📅 Date: {{ ansible_date_time.date }}
          🕐 Time: {{ ansible_date_time.time }}
          🐧 OS: {{ ansible_distribution }} {{ ansible_distribution_version }}
          
          ═══════════════════════════════════════

    - name: 🖥️ Display system information
      command: uname -a
      register: uname_output

    - name: 💾 Show disk space
      command: df -h
      register: disk_space

    - name: 📊 Print results
      debug:
        msg:
          - "🚀 System info: {{ uname_output.stdout }}"
          - "💿 Disk space: {{ disk_space.stdout_lines[0] }}"
          - "💿 Disk space: {{ disk_space.stdout_lines[1] }}"
```

---

### Step 10: Run the Playbooks

```bash
# Run update.yml
echo "🚀 Running update playbook..."
ansible-playbook -i inventory.ini update.yml

# Run playbook1.yml
echo "🚀 Running configuration playbook..."
ansible-playbook -i inventory.ini playbook1.yml
```

**Sample PLAY RECAP:**
```
PLAY RECAP *********************************************************************
172.17.0.3    : ok=6  changed=4  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
172.17.0.4    : ok=6  changed=4  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
172.17.0.5    : ok=6  changed=4  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
172.17.0.6    : ok=6  changed=4  unreachable=0  failed=0  skipped=0  rescued=0  ignored=0
```

---

## ✅ Verification

### Step 11: Verify Changes on All Servers

```bash
# Check test file via Ansible
echo "📋 Verifying test files on all servers..."
ansible all -i inventory.ini -m command -a "cat /root/test_file.txt"

# Manually verify via Docker exec
echo "🔍 Manual verification via Docker exec:"
for i in {1..4}; do
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "  📦 server${i}"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  docker exec server${i} cat /root/test_file.txt
done

# Verify installed packages
echo "✅ Verifying installed packages..."
ansible all -i inventory.ini -m command -a "which vim htop wget curl"
```

---

### 🎯 Bonus: Ad-hoc Ansible Commands

```bash
# Check uptime on all servers
ansible all -i inventory.ini -m command -a "uptime"

# Check OS info
ansible all -i inventory.ini -m command -a "uname -a"

# Check memory usage
ansible all -i inventory.ini -m command -a "free -h"

# Create a user on all servers
ansible all -i inventory.ini -m user -a "name=devops state=present"

# List available modules
ansible-doc -l | head -20

# View specific module docs
ansible-doc apt
ansible-doc copy
```

---

## 🔧 Optional Part C – Local nginx Install (WSL2 Ubuntu)

### Create local inventory and playbook

```bash
# Create local inventory for WSL2
cat << EOF > local_inventory.ini
[local]
localhost ansible_connection=local
EOF

# Create nginx playbook
cat << EOF > install_nginx.yml
---
- name: 🌐 Install Nginx on localhost (WSL2)
  hosts: local
  become: yes
  tasks:
    - name: 📥 Install nginx package
      apt:
        name: nginx
        state: present
    - name: ▶️ Start nginx service
      service:
        name: nginx
        state: started
        enabled: yes
    - name: ℹ️ Get nginx status
      command: systemctl status nginx
      register: nginx_status
    - name: 📊 Display nginx status
      debug:
        msg: "{{ nginx_status.stdout_lines[0:3] }}"
EOF

# Run it 
ansible-playbook -i local_inventory.ini install_nginx.yml
```

---

### 🔐 Using Ansible Vault (for secrets)

```bash
# Create an encrypted secrets file
ansible-vault create secrets.yml

# View encrypted file
ansible-vault view secrets.yml

# Edit encrypted file
ansible-vault edit secrets.yml

# Use with playbook
ansible-playbook -i inventory.ini playbook1.yml --ask-vault-pass
```

---

### 📦 Install Ansible Collections

```bash
# Install a collection from Ansible Galaxy
ansible-galaxy collection install community.general

# List installed collections
ansible-galaxy collection list
```

---

## 🧹 Cleanup

```bash
# Stop and remove all server containers
for i in {1..4}; do
  echo "🧹 Stopping server${i}..."
  docker stop server${i}
done

# Remove project keys (optional)
rm ~/ansible-exp9/id_rsa ~/ansible-exp9/id_rsa.pub

# Remove docker image (optional)
docker rmi ubuntu-server

# Exit WSL2 (if done)
exit
```

---

## 🪟 Windows + WSL2 – Common Issues & Fixes

| ⚠️ Issue | 🐛 Cause | 🔧 Fix |
|:---------|:---------|:-------|
| SSH fingerprint prompt blocks Ansible | First-time SSH | `export ANSIBLE_HOST_KEY_CHECKING=False` |
| Docker not found in WSL2 | Docker Desktop not integrated | Enable WSL2 integration in Docker Desktop settings |
| Permission denied on `id_rsa` | Wrong file permissions | `chmod 600 ~/.ssh/id_rsa` |
| Ansible can't find Python on nodes | Wrong interpreter path | Set `ansible_python_interpreter=/usr/bin/python3` in inventory |
| WSL2 can't ping Windows localhost | Network isolation | Use container IPs instead of localhost |
| Docker daemon not running | Docker Desktop not started | Start Docker Desktop from Windows Start menu |
| `ansible` command not found | Ansible not installed in WSL2 | Run `sudo apt install ansible -y` |
| SSH connection refused | Container not running | Check `docker ps` and restart containers |

---

## 🎯 Key Concepts Summary

### Ansible Workflow

```
Step 1: 🔑 SSH Keys      →  Generate and copy keys to containers
Step 2: 🏗️ Build Image    →  Create ubuntu-server with SSH
Step 3: 🚀 Launch         →  4 containers as managed nodes
Step 4: 📋 Inventory      →  List all server IPs
Step 5: 🧪 Test Ping      →  Verify connectivity
Step 6: ✍️ Write Playbook  →  Define automation tasks
Step 7: ▶️ Run Playbook    →  Execute across all servers
Step 8: ✅ Verify         →  Check results
Step 9: 🧹 Cleanup        →  Remove containers
```

### Idempotency Demo

Running the same playbook twice:

| Run | Changed Count | Explanation |
|:---:|:-------------:|:------------|
| **First run** | `changed=4` | Packages installed, files created |
| **Second run** | `changed=0` | Already in desired state — no changes made |

> ✨ **Idempotency:** Safe to run multiple times without unintended side effects!

---

## 📚 References

| Resource | Link |
|:---------|:-----|
| Official Ansible Website | [ansible.com](https://www.ansible.com) |
| Ansible Documentation | [docs.ansible.com](https://docs.ansible.com) |
| Ansible for Windows | [docs.ansible.com/ansible/latest/os_guide/windows_faq.html](https://docs.ansible.com/ansible/latest/os_guide/windows_faq.html) |
| WSL2 Documentation | [learn.microsoft.com/en-us/windows/wsl/](https://learn.microsoft.com/en-us/windows/wsl/) |
| Docker WSL2 Backend | [docs.docker.com/desktop/wsl/](https://docs.docker.com/desktop/wsl/) |
| Ansible Galaxy | [galaxy.ansible.com](https://galaxy.ansible.com) |

---

## 📸 Screenshots Checklist


---

## 📊 Result

<div align="center">

| ✅ | Outcome |
|:--:|:--------|
| 🎯 | **SUCCESS** - The experiment was completed successfully |

</div>

Using Ansible as a configuration management and automation tool, a control node (Windows PC with WSL2/Ubuntu) was configured to manage 4 Docker containers acting as remote servers. SSH key-based authentication was established between the control node and all managed nodes. An Ansible inventory file was created listing all target servers, and connectivity was verified using the `ansible ping` module — **all 4 servers returned SUCCESS**. 

Two YAML-based playbooks were written and executed, which:
- Automatically updated apt packages
- Installed software packages (`vim`, `htop`, `wget`, `curl`)
- Created configuration files with dynamic content using Ansible variables
- Collected system information across all servers simultaneously

**All without logging into any server manually!** 🚀

---

## 🎓 Learning Outcomes

After completing this experiment, students are able to:

| # | Learning Outcome |
|:-:|:-----------------|
| 1 | 🧠 **Understand** the architecture of Ansible — including the roles of the control node, managed nodes, inventory, modules, tasks, and playbooks, and how they work together in an agentless, SSH-based automation model |
| 2 | 🔐 **Set up** SSH key-based authentication between a control machine and multiple remote servers, and understand why this is essential for automated, passwordless server management |
| 3 | 📝 **Write and interpret** Ansible inventory files (`inventory.ini`) to define and group managed nodes with connection variables |
| 4 | ✍️ **Write YAML-based Ansible playbooks** to automate real-world tasks such as package installation, file creation, and system information gathering across multiple servers |
| 5 | 🔧 **Use Ansible modules** such as `apt`, `copy`, `command`, and `debug` to perform common system administration tasks declaratively |
| 6 | 🔄 **Demonstrate idempotency** — understanding that running the same playbook multiple times produces the same result without unintended side effects |
| 7 | ⚡ **Execute ad-hoc Ansible commands** for quick, one-off tasks without writing a full playbook |
| 8 | 🐳 **Use Docker containers** as simulated servers to practice multi-node infrastructure management in a local environment without requiring real cloud VMs |
| 9 | 💾 **Recognize the practical value** of Infrastructure as Code (IaC) — how version-controlled, declarative configuration files eliminate configuration drift and enable consistent, repeatable deployments at scale |
| 10 | 🪟 **Configure Ansible on Windows** using WSL2, bridging the gap between Windows development environments and Linux-based automation |

---

<div align="center">
  
---
  
*🔧 Experiment 9 | Ansible Automation | DevOps Lab*  
*🐧 Windows + WSL2 + Docker Setup*

</div>
