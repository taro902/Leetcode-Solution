import os
import re
import datetime
from pathlib import Path

# ==========================================
# CONFIGURATION: THE SACRED LIST (BATCH 2)
# ==========================================
AUTHOR = "taro902"
GITHUB_REPO = "https://github.com"

# NEW PRESET: "The Mental Hospital Edition"
TARGET_PROBLEMS_PRESET = [
    {"id": "4",   "title": "Median of Two Sorted Arrays"},
    {"id": "10",  "title": "Regular Expression Matching"},
    {"id": "126", "title": "Word Ladder II"},
    {"id": "84",  "title": "Largest Rectangle in Histogram"},
    {"id": "315", "title": "Count of Smaller Numbers After Self"}
]

TEMPLATES = {
    "c": """/*
 * Author: {author}
 * Date: {date}
 * Problem: {full_title}
 * Link: {link}
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <limits.h>

// Place your solution here
""",
    "java": """/*
 * Author: {author}
 * Date: {date}
 * Problem: {full_title}
 * Link: {link}
 */

package {package_name};

import java.util.*;
import java.util.stream.*;
import java.math.*;

public class Solution {{
    public static void main(String[] args) {{
        // Driver Code
    }}
}}
""",
    "javascript": """/**
 * Author: {author}
 * Date: {date}
 * Problem: {full_title}
 * Link: {link}
 */

/**
 * @param {{any}} args
 * @return {{any}}
 */
var solution = function(args) {{
    // Implementation
}};
""",
    "python": """# Author: {author}
# Date: {date}
# Problem: {full_title}
# Link: {link}

import math
from typing import List, Optional, Dict, Set
from collections import defaultdict, deque

class Solution:
    def solve(self):
        pass
""",
    "racket": """; Author: {author}
; Date: {date}
; Problem: {full_title}
; Link: {link}

(define/contract (solution args)
  (-> any/c any/c)
  (void))
"""
}

FILE_MAP = {
    "c": "solution.c",
    "java": "Solution.java",
    "javascript": "solution.js",
    "python": "solution.py",
    "racket": "solution.rkt"
}

class SacredGenerator:
    def __init__(self):
        self.root_dir = Path(os.getcwd())
        self.problem_dir = self.root_dir / "Problem"
        self._ensure_dir(self.problem_dir)

    def _ensure_dir(self, path: Path):
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

    def _sanitize_title(self, title: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        return re.sub(r'[\s-]+', '-', clean).strip().lower()

    def _generate_readme(self, path: Path, full_title: str, link: str):
        readme_path = path / "README.md"
        if not readme_path.exists():
            content = f"# {full_title}\n\nLink: [{full_title}]({link})"
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

    def create_problem(self, prob_id: str, title: str):
        slug = self._sanitize_title(title)
        folder_name = f"{prob_id}-{slug}"
        full_path = self.problem_dir / folder_name
        full_title = f"{prob_id}. {title}"
        link = f"https://leetcode.com{slug}/"
        
        print(f"[*] Constructing: {full_title}...")
        self._ensure_dir(full_path)
        self._generate_readme(full_path, full_title, link)

        date_now = datetime.datetime.now().strftime("%Y-%m-%d")

        for lang, filename in FILE_MAP.items():
            lang_path = full_path / lang
            self._ensure_dir(lang_path)
            file_path = lang_path / filename
            
            if file_path.exists() and file_path.stat().st_size > 0:
                continue

            code_content = TEMPLATES[lang].format(
                author=AUTHOR,
                date=date_now,
                full_title=full_title,
                link=link,
                package_name=lang
            )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_content)
            
            print(f"    -> {lang} ready.")

    def run_wizard(self):
        print("="*40)
        print("   ⚔️  BATCH 2 GENERATOR  ⚔️")
        print("="*40)
        print("1. Custom Problem")
        print("2. Generate BATCH 2 (The Mental Hospital List)")
        print("="*40)
        
        choice = input("Select [1/2]: ").strip()

        if choice == "1":
            pid = input("ID: ").strip()
            ptitle = input("Title: ").strip()
            if pid and ptitle:
                self.create_problem(pid, ptitle)
        elif choice == "2":
            print("\n🚀 Spawning Monsters...\n")
            for prob in TARGET_PROBLEMS_PRESET:
                self.create_problem(prob["id"], prob["title"])
            print("\n✨ Batch 2 Deployed. Good luck, you'll need it.")
        else:
            print("Invalid.")

if __name__ == "__main__":
    app = SacredGenerator()
    app.run_wizard()
