# Module 08: Container Orchestration & Cloud Infrastructure

## Objectives
Master container orchestration and Infrastructure-as-Code (IaC) for deploying resilient, auto-scaling Python microservices across Kubernetes and managed cloud platforms (AWS ECS Fargate & Google Cloud Run).

---

## Core Topics
1. **Kubernetes (K8s) for High-Throughput Python:**
   - Core API primitives: Deployments, StatefulSets, Services (ClusterIP, NodePort), and Ingress.
   - Resource tuning: Defining precise CPU/Memory `requests` and `limits`; diagnosing and preventing `OOMKilled` crashes.
   - Production health probes: `startupProbe` (slow app warmups), `readinessProbe` (traffic routing), and `livenessProbe` (unresponsive worker restarts).
   - Horizontal Pod Autoscaler (HPA) using custom metrics (requests per second / queue backlog).
   - Zero-downtime rolling updates: `maxSurge`, `maxUnavailable`, and `preStop` lifecycle hooks for connection draining.
2. **Managed Cloud Orchestration Blueprints:**
   - **AWS Blueprint (ECS Fargate & Aurora):**
     - ECS Task Definitions, execution roles, and CPU/Memory task allocations.
     - Application Load Balancer (ALB) target groups and SSL/TLS termination.
     - Connecting to AWS Aurora PostgreSQL Serverless v2 inside a private VPC.
   - **GCP Blueprint (Cloud Run & Cloud SQL):**
     - Cloud Run serverless container runtime: Concurrency per container instance, min/max instances, scale-to-zero economics.
     - Secure database connectivity via Cloud SQL Auth Proxy sidecar.
3. **Infrastructure as Code (IaC) with Terraform / OpenTofu:**
   - Structuring modular Terraform code: Network (VPC/Subnets), Compute (ECS/Cloud Run), Persistence (RDS/Cloud SQL).
   - Managing remote state backends (S3/GCS with DynamoDB/Cloud Spanner state locking).
   - Secrets and Identity: Least-privilege IAM policies, AWS IRSA (IAM Roles for Service Accounts) and GCP Workload Identity (zero static secrets).

---

## Planned Directory Structure
```text
Module_08_Container_Orchestration_Cloud_Infrastructure/
├── README.md
├── k8s/
│   ├── deployment.yaml          # Zero-downtime Deployment with probes & resource limits
│   ├── service.yaml             # ClusterIP Service
│   ├── ingress.yaml             # NGINX / Cloud Ingress with TLS
│   ├── hpa.yaml                 # Horizontal Pod Autoscaler
│   └── configmap-secrets.yaml   # External secret references
├── terraform/
│   ├── modules/
│   │   ├── networking/          # VPC, private subnets, NAT gateways
│   │   ├── database/            # RDS Aurora PostgreSQL / Cloud SQL
│   │   └── compute/             # ECS Fargate Service / Cloud Run Service
│   ├── environments/
│   │   ├── staging/
│   │   └── production/
│   └── main.tf
└── scripts/
    └── deploy_cloud.sh          # Orchestration rollout verification script
```

---

## Verification Criteria
- [ ] Kubernetes manifests pass `kubeval` and lint cleanly with zero security warnings.
- [ ] Pods transition through startup -> readiness probes with zero dropped HTTP requests during rolling updates.
- [ ] Terraform infrastructure plans execute cleanly with zero hardcoded credentials.
- [ ] Services scale up automatically under simulated load and scale down cleanly.
