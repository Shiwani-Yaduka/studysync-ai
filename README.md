# 📚 StudySync AI

> AI-Powered Smart Study Assistant with Kubernetes, CI/CD, Monitoring, and Automation

---

## 🚀 Project Overview

StudySync AI is a cloud-native AI-powered study automation platform that helps students prepare smarter for exams and assessments.

The system automatically:

* Detects upcoming exams/events from Google Calendar
* Extracts important topics using keyword detection
* Generates detailed AI-powered study guides
* Sends automated email-based preparation material
* Monitors the entire infrastructure using Prometheus and Grafana
* Deploys automatically using Jenkins CI/CD pipelines

---

[📸 Add Project Hero Screenshot Here
(Frontend Dashboard UI Screenshot)]

---

# 🧠 Key Features

✅ AI-generated detailed study guides
✅ Google Calendar event integration
✅ Automated scheduler-based workflow
✅ Smart keyword/topic extraction
✅ Email delivery automation
✅ Kubernetes deployment using K3s
✅ Jenkins-based CI/CD pipeline
✅ Dockerized frontend and backend
✅ Prometheus metrics monitoring
✅ Grafana visualization dashboards
✅ Multi-EC2 cloud architecture on AWS

---

# 🏗️ System Architecture

[📸 Add Architecture Diagram Here
(Frontend → Backend → AI Pipeline → Monitoring → Jenkins Workflow)]

---

# ☁️ Infrastructure Architecture

```text
EC2-1 → K3s Cluster
          ├── Streamlit Frontend
          ├── Flask Backend
          └── Kubernetes Services

EC2-2 → Jenkins Server
          ├── CI/CD Pipeline
          ├── Docker Builds
          └── Auto Deployment

EC2-3 → Monitoring Server
          ├── Prometheus
          └── Grafana
```

---

# ⚙️ Tech Stack

## Frontend

* Streamlit

## Backend

* Flask
* APScheduler

## AI & APIs

* Gemini API
* Tavily Search API
* Google Calendar API
* SendGrid API

## DevOps & Cloud

* Docker
* Kubernetes (K3s)
* Jenkins
* AWS EC2

## Monitoring

* Prometheus
* Grafana

---

# 🔄 Workflow

## 📅 Exam Detection Workflow

```text
Google Calendar Event
        ↓
Scheduler Checks Events
        ↓
Keyword Detection
        ↓
Topic Extraction
        ↓
AI Study Guide Generation
        ↓
Automated Email Delivery
```

---

[📸 Add Workflow Screenshot Here
(Google Calendar → Backend Logs → Email Workflow)]

---

# 📦 Kubernetes Deployment

The application is deployed using Kubernetes (K3s) with:

* Separate frontend and backend deployments
* Kubernetes Services
* Secrets Management
* Automated rollout updates

---

[📸 Add Kubernetes Pods Screenshot Here
(kubectl get pods output)]

---

# 🔁 CI/CD Pipeline

The project uses Jenkins for Continuous Integration and Continuous Deployment.

## CI/CD Flow

```text
GitHub Push
      ↓
Jenkins Trigger
      ↓
Docker Image Build
      ↓
DockerHub Push
      ↓
Kubernetes Rollout Restart
```

---

[📸 Add Jenkins Pipeline Screenshot Here
(Successful Jenkins Build)]

---

# 📊 Monitoring & Observability

Prometheus scrapes backend metrics from the Flask application, while Grafana visualizes:

* Request metrics
* Backend response time
* Scheduler activity
* AI workflow metrics
* Infrastructure monitoring

---

[📸 Add Grafana Dashboard Screenshot Here
(Main Monitoring Dashboard)]

---

[📸 Add Prometheus Targets Screenshot Here
(Target Status Showing UP)]

---

# 📡 Important URLs

## Frontend Application

```text
http://<K3S_PUBLIC_IP>:8501
```

## Backend Health Endpoint

```text
http://<K3S_PUBLIC_IP>:30050/health
```

## Metrics Endpoint

```text
http://<K3S_PUBLIC_IP>:30050/metrics
```

## Grafana Dashboard

```text
http://<MONITORING_EC2_IP>:3000
```

## Prometheus UI

```text
http://<MONITORING_EC2_IP>:9090
```

## Jenkins Dashboard

```text
http://<JENKINS_EC2_IP>:8080
```

---

# 🐳 Dockerization

Both frontend and backend services are containerized using Docker.

## Docker Components

* Frontend Dockerfile
* Backend Dockerfile
* DockerHub image registry
* Automated image deployment via Jenkins

---

[📸 Add DockerHub Repository Screenshot Here]

---

# 🔐 Security Features

* Kubernetes Secrets for API key management
* Isolated monitoring infrastructure
* Separate CI/CD server
* Containerized services
* Cloud-based deployment architecture

---

# 📁 Project Structure

```text
studysync-ai/
│
├── frontend/
├── backend/
├── docker/
├── k8s/
├── app/
├── Jenkinsfile
├── run.py
└── README.md
```

---

# 🧪 Example Use Case

## Scenario

1. Student adds:

```text
Docker Exam
```

to Google Calendar.

2. Scheduler detects event 7 days before exam.

3. AI generates:

* Docker concepts
* commands
* architecture explanations
* revision notes
* interview questions

4. Email automatically sent to student.

---

[📸 Add Email Screenshot Here
(Generated Study Guide Email)]

---

# 📈 Future Enhancements

* HTTPS + Domain Setup
* Multi-user authentication
* AI personalization levels
* Redis task queues
* Terraform Infrastructure-as-Code
* Kubernetes Ingress
* Loki centralized logging
* Alertmanager integration

---

# 👩‍💻 Author

## Shiwani Yaduka

BTech CSA Student | DevOps & Cloud Enthusiast | AI + Kubernetes Projects

GitHub: https://github.com/Shiwani-Yaduka

---

# ⭐ Conclusion

StudySync AI is more than just a study application — it is a complete cloud-native AI automation platform integrating:

* AI
* Kubernetes
* CI/CD
* Monitoring
* Cloud Infrastructure
* Automation

This project demonstrates real-world DevOps engineering practices combined with AI-powered productivity workflows.
