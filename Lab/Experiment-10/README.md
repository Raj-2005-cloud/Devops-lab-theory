Here's your Lab 10 report reformatted with clear section hierarchy and improved visual structure:

---

# Lab 10 — SonarQube: Continuous Code Quality Inspection

---

## 📌 Objective

To set up SonarQube for continuous code quality inspection, analyze a Java application for bugs, vulnerabilities, and code smells, integrate it into a CI/CD pipeline using Jenkins, and understand how Quality Gates enforce code standards before deployment.

---

## 📖 Theory

### 1.1 What is SonarQube?

SonarQube is an open-source platform for **continuous inspection of code quality**. It performs automatic static analysis to detect:

| Issue Type | Description |
|------------|-------------|
| **Bugs** | Code that will break or behave unexpectedly |
| **Vulnerabilities** | Security-related issues (e.g., SQL injection) |
| **Code Smells** | Maintainability issues that slow development |
| **Duplications** | Repeated code blocks |
| **Coverage** | % of code covered by unit tests |
| **Technical Debt** | Estimated time required to fix all issues |

### 1.2 Architecture

```
[ Your Code ]
      ↓
[ Sonar Scanner ]  →  Analyzes code locally
      ↓
[ SonarQube Server ]  →  Stores results + shows dashboard
      ↓
[ PostgreSQL DB ]  →  Persists all analysis data
```

### 1.3 Key Components

| Component | Role | Analogy |
|-----------|------|---------|
| SonarQube Server | Stores & displays results | Teacher / Examiner |
| Sonar Scanner | Analyzes and sends results | Student writing exam |
| Source Code | What gets analyzed | Answer sheet |

### 1.4 Quality Gate

A **Quality Gate** is a set of conditions that code must satisfy before it can be deployed. If the gate fails, the CI/CD pipeline is blocked — ensuring bad code never reaches production.

---

## 🏗️ Lab Architecture

```
┌─────────────────┐     HTTP      ┌──────────────────┐
│  Developer      │──────────────▶│  SonarQube       │
│  Machine        │               │  Server          │
│  (Maven)        │               │  (Port 9000)     │
└─────────────────┘               └──────────────────┘
        │                                │
        │ source code                    │ JDBC
        ▼                                ▼
┌─────────────────┐               ┌──────────────────┐
│  Calculator.java│               │  PostgreSQL      │
│  (with issues)  │               │  Database        │
└─────────────────┘               └──────────────────┘
```

---

## 📁 Project Structure

```
Lab-10/
├── docker-compose.yml                          # SonarQube + PostgreSQL setup
└── sample-java-app/
    ├── pom.xml                                 # Maven build + Sonar plugin
    ├── Jenkinsfile                             # CI/CD pipeline definition
    ├── sonar-project.properties                # Scanner configuration
    └── src/
        └── main/
            └── java/
                └── com/
                    └── example/
                        └── Calculator.java     # Sample app with intentional issues
```

---

## 🛠️ Setup & Commands

### Step 1 — Start SonarQube Environment

```bash
docker compose up -d
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  sonar-db:
    image: postgres:13
    container_name: sonar-db
    environment:
      POSTGRES_USER: sonar
      POSTGRES_PASSWORD: sonar
      POSTGRES_DB: sonarqube
    volumes:
      - sonar-db-data:/var/lib/postgresql/data
    networks:
      - sonarqube-lab

  sonarqube:
    image: sonarqube:lts-community
    container_name: sonarqube
    ports:
      - "9000:9000"
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://sonar-db:5432/sonarqube
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: sonar
    volumes:
      - sonar-data:/opt/sonarqube/data
      - sonar-extensions:/opt/sonarqube/extensions
    depends_on:
      - sonar-db
    networks:
      - sonarqube-lab

volumes:
  sonar-db-data:
  sonar-data:
  sonar-extensions:

networks:
  sonarqube-lab:
    driver: bridge
```

> **Access SonarQube at:** http://localhost:9000  
> **Default login:** `admin / admin`

---

### Step 2 — Sample Java Application (with Intentional Issues)

**Calculator.java — contains bugs, vulnerabilities, and code smells for analysis:**

```java
package com.example;

public class Calculator {

    // BUG: Division by zero not handled
    public int divide(int a, int b) {
        return a / b;
    }

    // CODE SMELL: Unused variable
    public int add(int a, int b) {
        int result = a + b;
        int unused = 100;   // unused variable
        return result;
    }

    // VULNERABILITY: SQL Injection risk
    public String getUser(String userId) {
        String query = "SELECT * FROM users WHERE id = " + userId;
        return query;
    }

    // CODE SMELL: Duplicate code block
    public int multiply(int a, int b) {
        int result = 0;
        for (int i = 0; i < b; i++) { result = result + a; }
        return result;
    }

    public int multiplyAlt(int a, int b) {
        int result = 0;
        for (int i = 0; i < b; i++) { result = result + a; }
        return result;
    }

    // CODE SMELL: Too many parameters
    public void processUser(String name, String email, String phone,
                            String address, String city, String state,
                            String zip, String country) {
        System.out.println("Processing: " + name);
    }

    // BUG: NullPointerException if name is null
    public String getName(String name) {
        return name.toUpperCase();
    }

    // CODE SMELL: Empty catch block (swallowing exception)
    public void riskyOperation() {
        try {
            int x = 10 / 0;
        } catch (Exception e) {
            // swallowed — bad practice
        }
    }
}
```

---

### Step 3 — Maven Configuration

**pom.xml:**

```xml
<properties>
    <maven.compiler.source>11</maven.compiler.source>
    <maven.compiler.target>11</maven.compiler.target>
    <sonar.projectKey>sample-java-app</sonar.projectKey>
    <sonar.projectName>Sample Java Application</sonar.projectName>
    <sonar.host.url>http://localhost:9000</sonar.host.url>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>3.9.1.2184</version>
    </plugin>
  </plugins>
</build>
```

---

### Step 4 — Run SonarQube Analysis

```bash
# Compile the project
mvn clean compile

# Run the scan (replace with your generated token)
mvn sonar:sonar -Dsonar.login=YOUR_SONAR_TOKEN
```

> **Generate a token:** SonarQube → My Account → Security → Generate Token

---

### Step 5 — Jenkins CI/CD Integration

**Jenkinsfile:**

```groovy
pipeline {
    agent any

    environment {
        SONAR_HOST_URL = 'http://sonarqube:9000'
        SONAR_TOKEN = credentials('sonar-token')
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {
                    sh 'mvn clean verify sonar:sonar'
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 1, unit: 'HOURS') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build') {
            steps { sh 'mvn package' }
        }

        stage('Deploy') {
            steps {
                sh 'docker build -t sample-app .'
                sh 'docker run -d -p 8080:8080 sample-app'
            }
        }
    }
}
```

---

### Step 6 — API Verification

```bash
# Fetch all bugs
curl -u admin:admin123 \
  "http://localhost:9000/api/issues/search?projectKeys=sample-java-app&types=BUG"

# Fetch vulnerabilities
curl -u admin:admin123 \
  "http://localhost:9000/api/issues/search?projectKeys=sample-java-app&types=VULNERABILITY"

# Full metrics summary (pretty printed)
curl -u admin:admin123 \
  "http://localhost:9000/api/measures/component?component=sample-java-app&metricKeys=bugs,vulnerabilities,code_smells,coverage,duplicated_lines_density,sqale_debt_ratio,reliability_rating,security_rating" \
  | python3 -m json.tool
```

---

## 📊 Analysis Results

### Before Fix

| Metric | Count |
|--------|-------|
| Bugs | 2 |
| Vulnerabilities | 1 |
| Code Smells | 5+ |
| Duplications | 2 blocks |
| Test Coverage | 0% |
| Technical Debt | ~2 hours |

### After Fixing Divide-by-Zero Bug

**Fixed code:**
```java
// Fixed: Division by zero now handled
public int divide(int a, int b) {
    if (b == 0) {
        throw new IllegalArgumentException("Cannot divide by zero");
    }
    return a / b;
}
```

**Re-run scan:**
```bash
mvn clean compile
mvn sonar:sonar -Dsonar.login=YOUR_SONAR_TOKEN
```

| Metric | Before | After Fix |
|--------|--------|-----------|
| Bugs | 2 | 1 ✅ |
| Vulnerabilities | 1 | 1 |
| Code Smells | 5+ | 5+ |

> The dashboard reflects the reduced bug count after re-scan — demonstrating SonarQube's continuous feedback loop.

---

## 🔄 CI/CD Flow with Quality Gate

```
Developer commits code
        ↓
Jenkins triggers pipeline
        ↓
mvn clean verify sonar:sonar
        ↓
SonarQube analyzes code
        ↓
Quality Gate evaluated
    ↙           ↘
PASS              FAIL
  ↓                 ↓
Build continues   Pipeline blocked 
Deploy to server  Fix issues first
```

---

## 📸 Screenshots

<img width="1440" height="900" alt="SonarQube Dashboard" src="https://github.com/user-attachments/assets/dd79c6e0-6f26-498c-bba3-3f329c5d9ba9" />

<img width="1440" height="268" alt="Issues Overview" src="https://github.com/user-attachments/assets/b9e97c0c-c8bd-4427-9e73-13c435b7e72e" />

<img width="1440" height="40" alt="Quality Gate Status" src="https://github.com/user-attachments/assets/97072b88-fc68-4754-8558-b1d217c12426" />

<img width="1440" height="490" alt="Bug Details" src="https://github.com/user-attachments/assets/3652a288-ad92-47d6-84f7-0f4904009dce" />

<img width="1440" height="900" alt="Code Smells" src="https://github.com/user-attachments/assets/a7489b93-3aa6-475f-9815-891781f6e526" />

<img width="1440" height="900" alt="Vulnerabilities" src="https://github.com/user-attachments/assets/7d0ca3d3-a95f-4402-9452-9747f1d7d8e3" />

<img width="1440" height="900" alt="Measures Screen" src="https://github.com/user-attachments/assets/a8b815ab-5c7d-45a0-bb35-ea5b47e9baad" />

<img width="1440" height="819" alt="Technical Debt" src="https://github.com/user-attachments/assets/2052c04d-6a34-4b3c-b459-7962ff13472e" />

<img width="1439" height="816" alt="Coverage Report" src="https://github.com/user-attachments/assets/a530388b-2e8e-4c48-80f6-74619e9dfad2" />

<img width="1094" height="739" alt="Duplications" src="https://github.com/user-attachments/assets/0ed29301-97b4-49a4-9352-c698bfa4c91d" />

<img width="1440" height="811" alt="Project Activity" src="https://github.com/user-attachments/assets/54279280-7b13-4345-8bff-d629f61705e1" />

<img width="1440" height="900" alt="New Code Period" src="https://github.com/user-attachments/assets/703be70b-aa37-42c3-813f-8119d0f0346c" />

<img width="1440" height="900" alt="Issue Details View" src="https://github.com/user-attachments/assets/51d195f7-6b0a-4eee-9b48-c3c6dc85dd8e" />

<img width="1440" height="900" alt="Rule Description" src="https://github.com/user-attachments/assets/f5a7ab14-e27c-4684-9183-2ee0eadb2020" />

<img width="1432" height="799" alt="Jenkins Pipeline" src="https://github.com/user-attachments/assets/c5d2fed9-ba3d-40a7-9309-dc9bdc0ce820" />

<img width="1440" height="777" alt="Docker Containers" src="https://github.com/user-attachments/assets/779f09e1-1807-42fb-868a-ab87b50dd7d1" />

<img width="1440" height="900" alt="Terminal Analysis" src="https://github.com/user-attachments/assets/66724edd-7c61-4018-9177-9429bd0f5ebe" />

<img width="1440" height="900" alt="Maven Build" src="https://github.com/user-attachments/assets/1ab1f6ea-fe46-4c0f-9f1a-8f270aa29b6a" />

<img width="1440" height="900" alt="Scanner Output" src="https://github.com/user-attachments/assets/92f2d9b9-1786-45ea-b1ad-b63b43a75903" />

<img width="1440" height="900" alt="API Response" src="https://github.com/user-attachments/assets/e1c3d35c-992b-41db-8346-0efe6b680625" />

<img width="1440" height="809" alt="Token Generation" src="https://github.com/user-attachments/assets/77d5b326-3d48-4dce-80ef-4a8a05bb3a45" />

<img width="1435" height="197" alt="Quality Gate Pass" src="https://github.com/user-attachments/assets/3ec8b915-8fc5-4d1f-840d-26252ac948a3" />

<img width="1440" height="212" alt="After Fix Dashboard" src="https://github.com/user-attachments/assets/17ad8a86-b4bb-418c-9731-3d7981770f80" />

<img width="1427" height="793" alt="Jenkins Console Output" src="https://github.com/user-attachments/assets/95f95069-85fe-43aa-810c-9b58e355577a" />

<img width="1436" height="319" alt="Successful Deployment" src="https://github.com/user-attachments/assets/2a1e59bc-03ba-4d59-b9ea-7a580dc26961" />

---

## 📚 Key Concepts Covered

| Concept | What Was Demonstrated |
|---------|----------------------|
| **Quality Gate** | Default "Sonar way" gate applied to project |
| **Technical Debt** | ~2 hours estimated fix time shown in dashboard |
| **Static Analysis** | Maven plugin scanned code without running it |
| **CI/CD Integration** | Jenkinsfile blocks deployment on gate failure |
| **Multi-issue Detection** | Bugs, vulnerabilities, code smells all detected |
| **Feedback Loop** | Fixed bug → re-scanned → dashboard updated |

---

## 🔍 Tool Comparison

| Feature | Jenkins | Ansible | Chef | SonarQube |
|---------|---------|---------|------|-----------|
| Primary Purpose | CI/CD Automation | Config Management | Config Management | Code Quality |
| Architecture | Master-Agent | Agentless | Client-Server | Client-Server |
| Language | Groovy | YAML | Ruby | Java |
| Learning Curve | Moderate | Low | High | Low |
| Idempotency | No | Yes | Yes | N/A |

---

## 🧹 Cleanup

```bash
docker compose down -v
```

*This removes all containers and volumes.*

---

## 🔗 References

- [SonarQube Official Documentation](https://docs.sonarqube.org/)
- [SonarQube Docker Hub](https://hub.docker.com/_/sonarqube)
- [Maven Sonar Plugin](https://docs.sonarqube.org/latest/analyzing-source-code/scanners/sonarscanner-for-maven/)
- [SonarQube Quality Gates](https://docs.sonarqube.org/latest/user-guide/quality-gates/)

---

**End of Lab Report**
