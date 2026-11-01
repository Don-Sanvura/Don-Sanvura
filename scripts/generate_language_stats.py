#!/usr/bin/env python3
"""Generate a self-hosted language breakdown for the public GitHub profile."""
from __future__ import annotations

import html
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

USERNAME = os.environ.get("GITHUB_USERNAME", "Don-Sanvura")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUTPUT = Path(os.environ.get("OUTPUT_FILE", "assets/language-stats.svg"))
API = "https://api.github.com"
COLORS = {
    "Python": "#3572A5", "JavaScript": "#f1e05a", "TypeScript": "#3178c6",
    "HTML": "#e34c26", "CSS": "#563d7c", "C#": "#178600", "C++": "#f34b7d",
    "Java": "#b07219", "Jupyter Notebook": "#DA5B0B", "PHP": "#4F5D95",
    "Go": "#00ADD8", "Rust": "#dea584", "Kotlin": "#A97BFF",
    "Swift": "#F05138", "Dart": "#00B4AB", "Ruby": "#701516",
    "Shell": "#89e051", "Vue": "#41b883", "SCSS": "#c6538c",
    "C": "#555555", "PowerShell": "#012456", "R": "#198CE7",
}
DEFAULT_COLORS = ["#22d3ee", "#0d9488", "#60a5fa", "#a78bfa", "#f59e0b"]


def request_json(url: str) -> tuple[object, dict[str, str]]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "Don-Sanvura-language-stats",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    last_error = None
    for attempt in range(5):
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as response:
                return json.loads(response.read().decode("utf-8")), dict(response.headers.items())
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in (403, 429, 500, 502, 503, 504):
                raise RuntimeError(f"GitHub API returned HTTP {exc.code} for {url}") from exc
            remaining = exc.headers.get("X-RateLimit-Remaining")
            reset = exc.headers.get("X-RateLimit-Reset")
            if remaining == "0" and reset:
                delay = max(1, min(60, int(reset) - int(time.time()) + 1))
            else:
                delay = min(2 ** attempt, 20)
            if attempt < 4:
                time.sleep(delay)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < 4:
                time.sleep(min(2 ** attempt, 20))
    raise RuntimeError(f"GitHub API request failed after retries: {last_error}")


def public_repositories() -> list[dict]:
    repos: list[dict] = []
    page = 1
    while True:
        query = urllib.parse.urlencode({
            "type": "owner", "visibility": "public",
            "per_page": 100, "page": page, "sort": "updated",
        })
        data, _ = request_json(f"{API}/users/{USERNAME}/repos?{query}")
        if not isinstance(data, list):
            raise RuntimeError("Unexpected repository-list response from GitHub.")
        repos.extend(repo for repo in data if not repo.get("fork", False) and repo.get("private") is False)
        if len(data) < 100:
            break
        page += 1
    return repos


def collect_languages(repos: list[dict]) -> dict[str, int]:
    totals: defaultdict[str, int] = defaultdict(int)
    for index, repo in enumerate(repos, start=1):
        full_name = repo.get("full_name")
        if not full_name:
            continue
        encoded = urllib.parse.quote(full_name, safe="/")
        data, _ = request_json(f"{API}/repos/{encoded}/languages")
        if not isinstance(data, dict):
            raise RuntimeError(f"Unexpected language response for {full_name}.")
        for language, byte_count in data.items():
            if isinstance(byte_count, int) and byte_count > 0:
                totals[language] += byte_count
        print(f"[{index}/{len(repos)}] Analysed {full_name}")
    return dict(totals)


def make_svg(totals: dict[str, int], repo_count: int) -> str:
    total_bytes = sum(totals.values())
    ranked = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    top = ranked[:9]
    if len(ranked) > 9:
        top.append(("Other", sum(value for _, value in ranked[9:])))
    width, left, right = 960, 230, 90
    row_height, top_y = 48, 112
    height = max(250, top_y + len(top) * row_height + 55)
    bar_width = width - left - right
    generated = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}" width="100%" height="auto">',
        '<title id="title">Most-used programming languages</title>',
        f'<desc id="desc">Language byte totals from {repo_count} public, non-fork repositories owned by {html.escape(USERNAME)}.</desc>',
        '<rect width="100%" height="100%" rx="18" fill="#0b1220"/>',
        '<text x="34" y="48" fill="#f8fafc" font-family="Segoe UI,Arial,sans-serif" font-size="25" font-weight="700">Most-used languages</text>',
        f'<text x="34" y="76" fill="#94a3b8" font-family="Segoe UI,Arial,sans-serif" font-size="13">{repo_count} public repositories · GitHub language bytes · {html.escape(generated)}</text>',
    ]
    if not top or total_bytes == 0:
        parts.append('<text x="34" y="145" fill="#cbd5e1" font-family="Segoe UI,Arial,sans-serif" font-size="17">No language data is available yet.</text>')
    else:
        for index, (language, value) in enumerate(top):
            y = top_y + index * row_height
            percent = value / total_bytes * 100
            fill = COLORS.get(language, DEFAULT_COLORS[index % len(DEFAULT_COLORS)])
            label = html.escape(language)
            parts.extend([
                f'<text x="34" y="{y + 19}" fill="#e2e8f0" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="600">{label}</text>',
                f'<rect x="{left}" y="{y}" width="{bar_width}" height="13" rx="6.5" fill="#1e293b"/>',
                f'<rect x="{left}" y="{y}" width="{bar_width * percent / 100:.2f}" height="13" rx="6.5" fill="{fill}"/>',
                f'<text x="{width - 34}" y="{y + 12}" fill="#cbd5e1" text-anchor="end" font-family="Segoe UI,Arial,sans-serif" font-size="14">{percent:.1f}%</text>',
            ])
    parts.append('<text x="34" y="{}" fill="#64748b" font-family="Segoe UI,Arial,sans-serif" font-size="11">Generated automatically from the GitHub REST API · Updates daily</text>'.format(height - 18))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> int:
    try:
        repos = public_repositories()
        languages = collect_languages(repos)
        svg = make_svg(languages, len(repos))
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        temporary = OUTPUT.with_suffix(OUTPUT.suffix + ".tmp")
        temporary.write_text(svg, encoding="utf-8")
        temporary.replace(OUTPUT)
        print(f"Generated {OUTPUT} using {len(repos)} public, non-fork repositories and {len(languages)} languages.")
        return 0
    except Exception as exc:  # Preserve the last known-good SVG on every failure.
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
