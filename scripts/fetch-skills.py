#!/usr/bin/env python3
"""
fetch-skills.py — Pull SKILL.md content from awesome-claude-skills and awesome-skills.com repos.

Usage:
    python3 scripts/fetch-skills.py [--dry-run] [--update-catalog]

What it does:
  1. Fetches all skill folders from ComposioHQ/awesome-claude-skills via GitHub API.
  2. Downloads SKILL.md from each folder and saves to skills/<id>.md
  3. Optionally reads awesome-skills.com-sourced repos (from AWESOME_SKILLS_REPOS below).
  4. If --update-catalog: appends new entries to skills/catalog.json with content_url set.

Requirements: python3 stdlib only (urllib, json, os, time).
GitHub rate limit: 60 req/hour unauthenticated. Set GITHUB_TOKEN env var to raise to 5000.
"""

import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

DRY_RUN = "--dry-run" in sys.argv
UPDATE_CATALOG = "--update-catalog" in sys.argv

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
CATALOG_PATH = SKILLS_DIR / "catalog.json"

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
COMPOSIO_REPO = "ComposioHQ/awesome-claude-skills"
MARKETPLACE_RAW_BASE = "https://raw.githubusercontent.com/insighture/tracelet-marketplace/main/skills"

# Skills from awesome-skills.com that are well-suited for enterprise governance use.
# Format: (repo_owner/repo_name, skill_id, name, description, kind, category, hue, tags, skill_md_path)
AWESOME_SKILLS_REPOS = [
    (
        "obra/superpowers", "tdd-superpowers",
        "Test-Driven Development", "Red-green-refactor discipline for AI agents: write failing test first, implement minimally, refactor.",
        "skill", "Development", 120,
        ["tdd", "testing", "quality"],
        "skills/test-driven-development/SKILL.md",
    ),
    (
        "obra/superpowers", "systematic-debugging",
        "Systematic Debugging", "Structured debugging protocol: reproduce → isolate → hypothesize → verify. Prevents shotgun fixes.",
        "skill", "Development", 35,
        ["debugging", "quality"],
        "skills/systematic-debugging/SKILL.md",
    ),
    (
        "trailofbits/skills", "security-review-tob",
        "Security Review (Trail of Bits)", "Trail of Bits security review skill: threat modelling, vuln classes, remediation patterns.",
        "skill", "Security", 0,
        ["security", "review", "appsec"],
        "SKILL.md",
    ),
    (
        "anthropics/claude-code-security-review", "claude-code-security-review",
        "Claude Code Security Review", "Official Anthropic security review skill for Claude Code: OWASP checks, secret detection, auth review.",
        "skill", "Security", 10,
        ["security", "claude-code", "official"],
        "SKILL.md",
    ),
    (
        "Pimzino/claude-code-spec-workflow", "spec-workflow",
        "Spec Workflow", "Structured spec-first development: requirements → design → implementation → review checklist.",
        "skill", "Development", 200,
        ["spec", "planning", "workflow"],
        "SKILL.md",
    ),
    (
        "alirezarezvani/claude-skills", "software-architect",
        "Software Architect", "System design skill: trade-off analysis, ADR generation, scalability review, and component diagrams.",
        "skill", "Architecture", 260,
        ["architecture", "design", "adr"],
        "skills/software-architect/SKILL.md",
    ),
    (
        "alirezarezvani/claude-skills", "code-reviewer",
        "Code Reviewer", "Structured code review: correctness, security, performance, style, and test coverage checklist.",
        "skill", "Development", 45,
        ["code-review", "quality"],
        "skills/code-reviewer/SKILL.md",
    ),
    (
        "hashicorp/agent-skills", "hashicorp-terraform",
        "HashiCorp Terraform Skills", "Terraform best practices: module structure, state management, provider patterns, and security.",
        "skill", "Infrastructure", 100,
        ["terraform", "infrastructure", "hashicorp"],
        "SKILL.md",
    ),
]


def gh_headers() -> dict:
    h = {"Accept": "application/vnd.github+json", "User-Agent": "tracelet-marketplace-fetcher/1.0"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def fetch_url(url: str, retries: int = 3) -> bytes | None:
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=gh_headers())
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if e.code == 403 and attempt < retries - 1:
                print(f"  Rate limited, sleeping 60s…", flush=True)
                time.sleep(60)
                continue
            print(f"  HTTP {e.code} for {url}", flush=True)
            return None
        except Exception as e:
            print(f"  Error fetching {url}: {e}", flush=True)
            return None
    return None


def list_composio_folders() -> list[dict]:
    url = f"https://api.github.com/repos/{COMPOSIO_REPO}/contents/"
    data = fetch_url(url)
    if not data:
        return []
    items = json.loads(data)
    return [i for i in items if i["type"] == "dir" and not i["name"].startswith(".")]


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def kind_for_composio(folder: str, content: str) -> str:
    """Guess skill kind from folder name and content."""
    f = folder.lower()
    if "claude" in f or "claude.md" in content.lower():
        return "claude_md"
    if "agent" in f:
        return "agents_md"
    if "cursor" in f or ".cursorrules" in content.lower():
        return "cursor_rules"
    return "skill"


def category_for_composio(folder: str) -> str:
    mapping = {
        "document": "Document Processing",
        "invoice": "Document Processing",
        "brand": "Design",
        "canvas": "Design",
        "theme": "Design",
        "image": "Creative",
        "video": "Creative",
        "slack": "Communication",
        "internal-comms": "Communication",
        "content": "Writing",
        "changelog": "Development",
        "mcp": "Development",
        "webapp": "Development",
        "developer": "Development",
        "skill": "Tooling",
        "connect": "Integration",
        "meeting": "Productivity",
        "file": "Productivity",
        "lead": "Marketing",
        "competitive": "Marketing",
        "twitter": "Marketing",
        "raffle": "Productivity",
        "domain": "Productivity",
        "tailored": "HR",
        "langsmith": "AI/ML",
        "composio": "Integration",
    }
    f = folder.lower()
    for key, cat in mapping.items():
        if key in f:
            return cat
    return "Productivity"


def hue_for_category(cat: str) -> int:
    hues = {
        "Development": 215,
        "Security": 0,
        "Architecture": 260,
        "Design": 300,
        "Document Processing": 30,
        "Writing": 140,
        "Communication": 190,
        "Marketing": 330,
        "Productivity": 45,
        "Integration": 170,
        "Infrastructure": 100,
        "AI/ML": 200,
        "Tooling": 60,
        "HR": 20,
        "Creative": 280,
        "Language": 175,
        "Frontend": 200,
    }
    return hues.get(cat, 180)


def fetch_composio_skills(existing_ids: set[str]) -> list[dict]:
    """Fetch all skill folders from ComposioHQ/awesome-claude-skills."""
    print(f"\n=== ComposioHQ/awesome-claude-skills ===")
    folders = list_composio_folders()
    print(f"Found {len(folders)} folders")

    skip = {"template-skill", "skill-share", "skill-creator", "connect", "connect-apps-plugin",
            "connect-apps", "composio-skills", ".github"}
    results = []

    for folder in folders:
        name = folder["name"]
        if name in skip:
            continue

        skill_id = f"composio-{name}"
        if skill_id in existing_ids:
            print(f"  [skip] {skill_id} already in catalog")
            continue

        raw_url = f"https://raw.githubusercontent.com/{COMPOSIO_REPO}/master/{name}/SKILL.md"
        print(f"  Fetching {name}/SKILL.md…", end=" ", flush=True)
        content = fetch_url(raw_url)
        if not content:
            print("not found, skipping")
            continue

        text = content.decode("utf-8", errors="replace")
        print(f"{len(text)} bytes")

        # Extract description from YAML frontmatter
        description = name.replace("-", " ").title()
        fm_match = re.search(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
        if fm_match:
            fm = fm_match.group(1)
            desc_match = re.search(r"^description:\s*(.+)$", fm, re.MULTILINE)
            if desc_match:
                description = desc_match.group(1).strip().strip('"').strip("'")

        cat = category_for_composio(name)
        kind = kind_for_composio(name, text)
        hue = hue_for_category(cat)
        display_name = name.replace("-", " ").title()

        # Save file
        dest = SKILLS_DIR / f"{skill_id}.md"
        if not DRY_RUN:
            dest.write_text(text, encoding="utf-8")

        results.append({
            "id": skill_id,
            "name": display_name,
            "description": description,
            "kind": kind,
            "category": cat,
            "vendor_url": f"https://github.com/{COMPOSIO_REPO}/tree/master/{name}",
            "content_url": f"{MARKETPLACE_RAW_BASE}/{skill_id}.md",
            "hue": hue,
            "tags": [t for t in name.split("-") if len(t) > 2],
        })

        time.sleep(0.3)  # gentle rate limiting

    return results


def fetch_awesome_skills(existing_ids: set[str]) -> list[dict]:
    """Fetch SKILL.md from curated awesome-skills.com repos."""
    print(f"\n=== awesome-skills.com curated repos ===")
    results = []

    for (repo, skill_id, name, description, kind, category, hue, tags, skill_path) in AWESOME_SKILLS_REPOS:
        if skill_id in existing_ids:
            print(f"  [skip] {skill_id} already in catalog")
            continue

        raw_url = f"https://raw.githubusercontent.com/{repo}/main/{skill_path}"
        print(f"  Fetching {repo}/{skill_path}…", end=" ", flush=True)
        content = fetch_url(raw_url)

        # Try master branch if main fails
        if not content:
            raw_url = f"https://raw.githubusercontent.com/{repo}/master/{skill_path}"
            content = fetch_url(raw_url)

        if not content:
            print("not found, skipping")
            continue

        text = content.decode("utf-8", errors="replace")
        print(f"{len(text)} bytes")

        dest = SKILLS_DIR / f"{skill_id}.md"
        if not DRY_RUN:
            dest.write_text(text, encoding="utf-8")

        results.append({
            "id": skill_id,
            "name": name,
            "description": description,
            "kind": kind,
            "category": category,
            "vendor_url": f"https://github.com/{repo}",
            "content_url": f"{MARKETPLACE_RAW_BASE}/{skill_id}.md",
            "hue": hue,
            "tags": tags,
        })

        time.sleep(0.3)

    return results


def main():
    SKILLS_DIR.mkdir(exist_ok=True)

    catalog: list[dict] = []
    if CATALOG_PATH.exists():
        catalog = json.loads(CATALOG_PATH.read_text())

    existing_ids = {e["id"] for e in catalog}

    # Patch existing entries that are missing content_url
    changed = False
    for entry in catalog:
        if not entry.get("content_url"):
            entry["content_url"] = f"{MARKETPLACE_RAW_BASE}/{entry['id']}.md"
            changed = True

    new_composio = fetch_composio_skills(existing_ids)
    new_awesome = fetch_awesome_skills(existing_ids | {e["id"] for e in new_composio})

    all_new = new_composio + new_awesome
    print(f"\nFetched {len(all_new)} new skills ({len(new_composio)} Composio, {len(new_awesome)} awesome-skills)")

    if UPDATE_CATALOG and (all_new or changed):
        catalog.extend(all_new)
        catalog.sort(key=lambda e: e["name"].lower())
        if not DRY_RUN:
            CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
            print(f"Updated {CATALOG_PATH} ({len(catalog)} total entries)")
        else:
            print(f"[dry-run] would write {len(catalog)} entries to {CATALOG_PATH}")
    else:
        print("Pass --update-catalog to write changes to catalog.json")

    if DRY_RUN:
        print("\n[dry-run] no files written")


if __name__ == "__main__":
    main()
