#!/usr/bin/env python3
"""Fail a pull request if GACC's public website accidentally exposes obvious secrets
or adds insecure form submissions. This is a guardrail, NOT a security audit.
No dependencies, network access, or secret values in CI output.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
EXTENSIONS = {".html", ".js", ".css", ".json", ".xml", ".txt", ".md", ".yml", ".yaml", ".webmanifest"}
SKIP_DIRS = {".git", "node_modules", "vendor", ".venv"}

# Do not print matched secret content to logs.
SENSITIVE_PATTERNS = [
    ("Stripe secret/restricted key", re.compile(r"\b(?:sk|rk)_(?:live|test)_[A-Za-z0-9]{12,}")),
    ("GitHub personal access token", re.compile(r"\b(?:ghp|gho|ghu|ghs)_[A-Za-z0-9]{25,}")),
    ("GitHub fine-grained token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
]
HTTP_ACTIVE_CONTENT = re.compile(r"""(?i)\b(?:src|action)\s*=\s*['"]http://""")
INSECURE_FORM = re.compile(r"""(?i)<form\b[^>]*\baction\s*=\s*['"]http://""")
PAYMENT_FIELDS = re.compile(r"""(?i)<input\b[^>]*\b(?:name|id)\s*=\s*['"](?:card(?:_|-)?number|cvc|cvv|routing(?:_|-)?number|ssn)['"]""")

problems = []
examined = 0
for path in sorted(ROOT.rglob("*")):
    if not path.is_file() or path.suffix.lower() not in EXTENSIONS:
        continue
    if any(p in SKIP_DIRS for p in path.relative_to(ROOT).parts):
        continue
    if path.stat().st_size > 8_000_000:
        continue
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    examined += 1
    relative = str(path.relative_to(ROOT))
    for label, pattern in SENSITIVE_PATTERNS:
        if pattern.search(content):
            problems.append(f"{relative}: potential {label} detected (value suppressed)")
    if path.suffix.lower() == ".html":
        if HTTP_ACTIVE_CONTENT.search(content):
            problems.append(f"{relative}: insecure http:// script, asset or form source")
        if INSECURE_FORM.search(content):
            problems.append(f"{relative}: form submits over HTTP")
        if PAYMENT_FIELDS.search(content):
            problems.append(f"{relative}: payment or sensitive-ID collection field found; use hosted checkout")

dealer = ROOT / "dealer-application.html"
privacy = ROOT / "privacy.html"
if dealer.exists() and not privacy.exists():
    problems.append("privacy.html missing")
elif dealer.exists() and "privacy.html" not in dealer.read_text(encoding="utf-8"):
    problems.append("dealer-application.html must link to privacy.html")

if problems:
    print("GACC security checks FAILED:")
    for problem in problems:
        print(" - " + problem)
    sys.exit(1)
print(f"GACC security checks passed on {examined} source files.")
