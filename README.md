# Cloud Infrastructure Monitor

A fully provisioned cloud infrastructure on AWS built with Terraform — spins up ECS, RDS, and S3 with a single `terraform apply`. Includes a Prometheus + Grafana observability stack with real-time metrics and auto-scaling.

## Architecture
Internet → ALB → ECS Fargate (FastAPI) → RDS PostgreSQL
↓
Prometheus → Grafana

## Stack

| Layer | Technology |
|---|---|
| Infrastructure | Terraform |
| Compute | AWS ECS Fargate |
| Database | AWS RDS PostgreSQL |
| Storage | AWS S3 |
| Monitoring | Prometheus + Grafana |
| Container Registry | AWS ECR |
| CI/CD | GitHub Actions |
| App | Python + FastAPI |

## What it does

- **Single command deployment** — `terraform apply` provisions the entire AWS stack
- **Containerised app** — FastAPI service running on ECS Fargate, no servers to manage
- **Real-time observability** — Prometheus scrapes metrics every 15s, Grafana dashboards show request rate, p99 latency, and error rate
- **Auto-scaling** — ECS scales from 1 to 10 tasks based on CPU (>60%) and memory (>70%) thresholds
- **Full CI/CD** — every push to `main` builds, pushes to ECR, and deploys to ECS automatically

## Metrics tracked

- `http_requests_total` — request count by method, path, status
- `http_request_duration_seconds` — latency histogram (p50, p95, p99)
- `http_errors_total` — error count by path and status code

## Local development

```bash
# Start full stack locally
docker compose up --build

# App:        http://localhost:8000
# Prometheus: http://localhost:9090
# Grafana:    http://localhost:3000 (admin/admin)
```

## Deploy to AWS

```bash
# 1. Configure AWS credentials
aws configure

# 2. Provision infrastructure
cd terraform
terraform init
terraform apply -var="db_password=YOUR_PASSWORD"

# 3. Push Docker image to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ECR_REGISTRY
docker build -t cloud-infra-monitor .
docker tag cloud-infra-monitor:latest YOUR_ECR_REGISTRY/cloud-infra-monitor:latest
docker push YOUR_ECR_REGISTRY/cloud-infra-monitor:latest

# 4. Force ECS deployment
aws ecs update-service --cluster cloud-infra-monitor-cluster --service cloud-infra-monitor-service --force-new-deployment
```

## CI/CD Pipeline

Every push to `main` triggers:

1. Build Docker image
2. Push to ECR with git SHA tag
3. Update ECS task definition
4. Rolling deploy to Fargate
5. Health check confirmation

## Tear down

Run the **Destroy Infrastructure** workflow manually from the GitHub Actions tab — type `DESTROY` to confirm. This runs `terraform destroy` and removes all AWS resources.

## Cost

Runs within AWS free tier — ECS Fargate, RDS db.t3.micro, and S3 are all covered. Terraform, Prometheus, and Grafana are fully open source.

## Live Demo

Base URL: `http://cloud-infra-monitor-alb-212185390.us-east-1.elb.amazonaws.com`

| Endpoint | Description |
|---|---|
| `/health` | Health check |
| `/metrics` | Prometheus metrics |
| `/status` | Service info |

/health — http://cloud-infra-monitor-alb-212185390.us-east-1.elb.amazonaws.com/health
/metrics — http://cloud-infra-monitor-alb-212185390.us-east-1.elb.amazonaws.com/metrics
/status — http://cloud-infra-monitor-alb-212185390.us-east-1.elb.amazonaws.com/status

<img width="2874" height="1457" alt="image" src="https://github.com/user-attachments/assets/7938d513-dc86-429c-93b5-9fd195095ecc" />
<img width="2879" height="1050" alt="image" src="https://github.com/user-attachments/assets/3b9691c6-adeb-458a-aa1c-cd818b53dc71" />
<img width="2410" height="1244" alt="image" src="https://github.com/user-attachments/assets/e82aeffd-6bb2-497c-871c-3adecbecea9f" />
<img width="2106" height="296" alt="image" src="https://github.com/user-attachments/assets/225c30a9-8e71-42fd-a1be-a323614717b0" />
