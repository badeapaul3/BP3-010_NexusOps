"""Pre-commit secret detection script to prevent accidental credential leakage in public repos.

Scans staged Git diffs (or the entire repository when run with --all) for high-risk patterns
such as private keys, API tokens, and raw cloud credentials.
"""

import re
import subprocess
import sys
from pathlib import Path

# High-risk token and credential patterns
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    (
        "Private Key Header",
        re.compile(r"-----BEGIN\s+(?:RSA|OPENSSH|EC|DSA|PGP|PRIVATE)\s+KEY-----"),
    ),
    ("OpenAI API Key", re.compile(r"sk-[a-zA-Z0-9]{20,}")),
    ("Anthropic API Key", re.compile(r"sk-ant-[a-zA-Z0-9_-]{20,}")),
    (
        "AWS Access Key ID",
        re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
    ),
    ("GitHub Personal Access Token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}")),
    ("Slack API Token", re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}")),
    (
        "Generic High-Entropy Secret Assignment",
        re.compile(
            r"(?i)(?:api_key|api_secret|aws_secret_access_key|access_token|private_key|auth_token)"
            r'\s*=\s*["\'][a-zA-Z0-9_\-+/]{20,}["\']'
        ),
    ),
]

# Allow-listed patterns (e.g., explicit example/placeholder tokens)
ALLOW_LIST: list[str] = [
    "sk-placeholder-key",
    "sk-ant-placeholder-key",
    "change-me-in-local-dev",
    "change-me-in-production",
    "postgres_insecure_default",
    "your_local_postgres_password_here",
    "your_openai_api_key_here",
    "your_anthropic_api_key_here",
]

# Files excluded from whole-repo scans (e.g. self-referential detector, lockfiles)
EXCLUDED_SCAN_FILES: set[str] = {
    "scripts/detect_secrets.py",
    "scripts\\detect_secrets.py",
    "uv.lock",
    ".gitleaks.toml",
}


def is_allowed(line: str) -> bool:
    """Return True if matched line contains a known benign placeholder."""
    return any(placeholder in line for placeholder in ALLOW_LIST)


def get_staged_diff() -> str:
    """Retrieve Git diff for all currently staged changes."""
    result = subprocess.run(
        ["git", "diff", "--staged", "--unified=0"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout


def scan_diff(diff_text: str) -> list[str]:
    """Inspect diff additions for forbidden secret patterns."""
    violations: list[str] = []
    current_file = "unknown"

    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        if line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:].strip()
            if is_allowed(added_content):
                continue

            for pattern_name, pattern in SECRET_PATTERNS:
                if pattern.search(added_content):
                    snippet = added_content[:60]
                    violations.append(
                        f"  [ERROR] {pattern_name} detected in '{current_file}':\n"
                        f"    Line: {snippet}..."
                    )

    return violations


def scan_all_tracked_files() -> list[str]:
    """Scan all tracked files in the repository for forbidden patterns."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    tracked_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    violations: list[str] = []

    for file_path_str in tracked_files:
        if file_path_str in EXCLUDED_SCAN_FILES:
            continue

        file_path = Path(file_path_str)
        if not file_path.is_file():
            continue

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        for line_num, line in enumerate(content.splitlines(), start=1):
            if is_allowed(line):
                continue
            for pattern_name, pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    snippet = line.strip()[:60]
                    violations.append(
                        f"  [ERROR] {pattern_name} detected in '{file_path_str}:{line_num}':\n"
                        f"    Line: {snippet}..."
                    )

    return violations


def main() -> int:
    """Execute secret detection scan."""
    scan_all = "--all" in sys.argv or "--ci" in sys.argv

    if scan_all:
        violations = scan_all_tracked_files()
    else:
        diff_text = get_staged_diff()
        violations = scan_diff(diff_text)

    if violations:
        print("\n" + "=" * 78, file=sys.stderr)
        print(" [SECURITY ALERT] SECRET DETECTION CHECK FAILED!", file=sys.stderr)
        print("=" * 78, file=sys.stderr)
        for violation in violations:
            print(violation, file=sys.stderr)
        print("\nAborted to protect your public repository.", file=sys.stderr)
        print("Check ALLOW_LIST in scripts/detect_secrets.py if false positive.", file=sys.stderr)
        print("=" * 78 + "\n", file=sys.stderr)
        return 1

    print("Secret scan passed: zero credentials or private keys detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
