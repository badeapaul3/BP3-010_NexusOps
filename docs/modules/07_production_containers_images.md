# Module 07: Production Containerization & Image Engineering

## Objectives
Master enterprise-grade Docker engineering for Python services. Build minimal, non-root, cache-optimized OCI container images with sub-second rebuilds, vulnerability hardening, and correct POSIX signal handling.

---

## Core Topics
1. **High-Performance Multi-Stage Builds:**
   - Separating build-time dependencies (compilers, build tools, wheel building) from runtime images.
   - Leveraging Docker BuildKit cache mounts (`--mount=type=cache,target=/root/.cache/uv`) for ultra-fast dependency caching.
   - Minimal runtime base images: `python:3.12-slim` vs Google Distroless (`gcr.io/distroless/python3-debian12`) vs Chainguard images.
   - Target image footprint: Achieving production images under 120MB.
2. **Container Security & Hardening:**
   - Running as an unprivileged, non-root user (`USER appuser` with explicit UID/GID `10001:10001`).
   - Read-only root filesystem configurations (`read_only: true` with tmpfs mounts for `/tmp`).
   - Dropping Linux capabilities (`cap_drop: ALL`) and preventing privilege escalation.
   - Vulnerability scanning and CVE gating with `trivy` and Software Bill of Materials (SBOM) generation with `syft`.
3. **Process Supervision & Signal Propagation (PID 1):**
   - The PID 1 problem in Docker: Why standard Python scripts fail to handle `SIGTERM` and leave zombie processes.
   - Using init wrappers like `tini` or `dumb-init` for proper signal forwarding and sub-process reaping.
   - Healthcheck directives: Configuring `HEALTHCHECK` with proper interval, timeout, start-period, and retries.
4. **OCI Image Distribution & Registries:**
   - Multi-architecture builds (`linux/amd64` and `linux/arm64`) using `docker buildx`.
   - Managing and authenticating with enterprise registries (AWS ECR and GCP Artifact Registry).
   - Image signing and verification using Sigstore `cosign`.

---

## Planned Directory Structure
```text
Module_07_Production_Containers_Image_Engineering/
├── README.md
├── docker/
│   ├── Dockerfile               # Multi-stage production Dockerfile (uv + non-root)
│   ├── Dockerfile.distroless    # Ultra-secure Google Distroless runtime
│   ├── .dockerignore            # Strict ignore rules (wheels, caches, envs, tests)
│   ├── docker-compose.yml       # Local integration stack (API + DB + Redis)
│   └── entrypoint.sh            # Process initialization and signal trap script
├── scripts/
│   ├── build.sh                 # Buildx multi-arch build script
│   └── scan_vulnerabilities.sh  # Trivy CVE scan & SBOM generation script
└── tests/
    └── test_container.py        # Automated container smoke tests (healthcheck, user verification)
```

---

## Verification Criteria
- [ ] Docker image builds in under 5 seconds on warm cache with `uv`.
- [ ] Production runtime image size is strictly below 150MB.
- [ ] Container runs verified as non-root user (`id -u` returns non-zero).
- [ ] Zero HIGH or CRITICAL vulnerabilities reported by `trivy`.
- [ ] Container responds cleanly to `docker stop` (graceful shutdown in under 3 seconds).
