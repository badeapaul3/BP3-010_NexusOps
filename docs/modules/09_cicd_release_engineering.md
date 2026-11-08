# Module 09: Enterprise CI/CD Automation, Release Engineering & GitOps

## Objectives
Design and automate end-to-end continuous integration and deployment pipelines, implement automated semantic release engineering, manage private artifact registries, and execute safe zero-downtime deployment strategies (Canary & Blue-Green).

---

## Core Topics
1. **High-Speed GitHub Actions CI Pipeline:**
   - Multi-job workflows with strict dependency gates: Lint (`ruff`), Strict Typecheck (`mypy`), Unit Tests, Integration Tests.
   - Cache optimization: Restoring `uv` cache and Docker layer caches to achieve sub-2-minute total CI runtime.
   - Running live database containers directly inside GitHub Actions runner service containers.
2. **Automated Release Engineering & Versioning:**
   - Enforcing Conventional Commits (`feat:`, `fix:`, `chore:`, `perf:`).
   - Automated Semantic Versioning (SemVer) with automated changelog generation.
   - Building and publishing Python wheels (`.whl`) and source distributions (`sdist`) to AWS CodeArtifact / GCP Artifact Registry.
   - Image signing using Sigstore `cosign` and publishing provenance attestations.
3. **Advanced Zero-Downtime Deployment Strategies:**
   - Automated database migration execution: Running `alembic upgrade head` in an ephemeral pre-deployment task before shifting traffic.
   - Blue-Green deployments: Spinning up an isolated identical environment and shifting DNS / ALB listener rules.
   - Canary releases: Routing 5% -> 25% -> 100% of user traffic while monitoring error rates and automatic rollback triggers.
   - GitOps workflows: Declarative repository-driven deployments using ArgoCD or Flux.

---

## Planned Directory Structure
```text
Module_09_CICD_Automation_Release_Engineering/
├── README.md
├── .github/
│   ├── workflows/
│   │   ├── ci-pipeline.yml      # Lint, typecheck, test with service containers
│   │   ├── publish-package.yml  # Build & publish wheel to private artifact index
│   │   ├── build-image.yml      # Multi-arch Docker build, CVE scan, cosign sign
│   │   └── cd-deploy.yml        # Cloud Run / ECS blue-green rollout
│   └── pull_request_template.md
├── scripts/
│   ├── run_migrations.sh        # Pre-traffic database migration runner
│   └── canary_monitor.sh       # Automated error-rate monitor & rollback script
└── docs/
    └── release_strategy.md      # Semantic release & branching strategy guide
```

---

## Verification Criteria
- [ ] Pull requests trigger parallel CI checks and enforce status checks before merge.
- [ ] Releases automatically generate changelogs, tag git commits, and publish versioned artifacts.
- [ ] Database migrations execute safely prior to new container container deployment.
- [ ] Simulated error spikes during canary rollout trigger an automated rollback to the previous stable revision.
