"""Pre-commit secret detection script to prevent accidental credential leakage in public repos.

Scans staged Git diffs for high-risk patterns such as private keys, API tokens,
and raw cloud credentials before allowing a commit to be created.
"""

import re
import subprocess
import sys

# High-risk token and credential patterns
SECRET_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Private Key Header", re.compile(r"-----BEGIN\s+(?:RSA|OPENSSH|EC|DSA|PGP|PRIVATE)\s+KEY-----")),
    ("OpenAI API Key", re.compile(r"sk-[a-zA-Z0-9]{20,}")),
    ("Anthropic API Key", re.compile(r"sk-ant-[a-zA-Z0-9_-]{20,}")),
    ("AWS Access Key ID", re.compile(r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}")),
    ("GitHub Personal Access Token", re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}")),
    ("Slack API Token", re.compile(r"xox[baprs]-[0-9a-zA-Z]{10,48}")),
    ("Generic High-Entropy Secret Assignment", re.compile(
        r'(?i)(?:api_key|api_secret|aws_secret_access_key|access_token|private_key|auth_token)\s*=\s*["\'][a-zA-Z0-9_\-+/]{20,}["\']'
    )),
]

# Allow-listed patterns (e.g., explicit example/placeholder tokens)
ALLOW_LIST: list[str] = [
    "sk-placeholder-key",
    "sk-ant-placeholder-key",
    "change-me-in-local-dev",
    "change-me-in-production",
    "postgres_insecure_default",
    "your_local_postgres_password_here",
]


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


def scan_staged_diff() -> int:
    """Scan staged diff lines for forbidden secret patterns."""
    diff_text = get_staged_diff()
    if not diff_text.strip():
        return 0

    violations: list[str] = []

    current_file = "unknown"
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            current_file = line[6:]
            continue

        # Only inspect added lines
        if line.startswith("+") and not line.startswith("+++"):
            added_content = line[1:].strip()

            if is_allowed(added_content):
                continue

            for pattern_name, pattern in SECRET_PATTERNS:
                if pattern.search(added_content):
                    violations.append(
                        f"  [ERROR] {pattern_name} detected in '{current_file}':\n    Line: {added_content[:80]}..."
                    )

    if violations:
        print("\n" + "=" * 78, file=sys.stderr)
        print(" [SECURITY ALERT] PRE-COMMIT CHECK BLOCKED A POTENTIAL SECRET LEAK!", file=sys.stderr)
        print("=" * 78, file=sys.stderr)
        for violation in violations:
            print(violation, file=sys.stderr)
        print("\nCommit aborted to protect your public repository.", file=sys.stderr)
        print("If this is a false positive, verify the token is a mock value in ALLOW_LIST.", file=sys.stderr)
        print("=" * 78 + "\n", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(scan_staged_diff())
