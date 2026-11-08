# Security Policy & Secret Leak Prevention

## 1. Zero-Hardcoded Secrets Policy

As a public repository, **BP3-010_NexusOps** enforces a strict zero-hardcoded-credentials policy:
- No real API keys, cloud access tokens, passwords, private certificates, or production connection strings may ever be committed.
- All secrets must be supplied via local environment variables, `.env` files (which are strictly Git-ignored), or cloud secret managers (AWS Secrets Manager / GCP Secret Manager).
- Pydantic v2 domain settings must always mask sensitive attributes using `pydantic.SecretStr` or `pydantic.SecretBytes`.

---

## 2. Active Defense & Security Controls

The repository incorporates multiple concentric layers of defense to prevent credential leakage:

1. **Strict Git Ignore Rules ([`.gitignore`](./.gitignore)):**
   - Blocks `.env`, `.env.*`, cryptographic keys (`*.pem`, `*.key`), cloud credentials (`credentials.json`, `service_account*.json`), Terraform state files (`*.tfstate`, `*.tfvars`), and local database files.
2. **Template Configuration ([`.env.example`](./.env.example)):**
   - Standardized template containing only non-functional, mock placeholders.
3. **Local Pre-Commit Hook ([`scripts/detect_secrets.py`](./scripts/detect_secrets.py)):**
   - Automatically scans staged Git diffs before every commit. Blocks commits containing private keys, AWS tokens, OpenAI/Anthropic keys, or high-entropy secrets.
4. **Automated CI Scanning ([`.github/workflows/security-scan.yml`](./.github/workflows/security-scan.yml)):**
   - GitHub Actions executes Gitleaks on every push and pull request with full history scanning.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability or suspect an accidental credential exposure, please do not open a public issue. Instead, report it directly to the repository maintainer:

- **Maintainer:** badeapaul3 (badeapaul3@gmail.com)
