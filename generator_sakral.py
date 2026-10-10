import os
import re
import datetime
from pathlib import Path

AUTHOR = "taro902"
GITHUB_REPO = "https://github.comhttps://github.com/taro902/Leetcode-Solution/tree/main"

TARGET_PROBLEMS_PRESET = [
    {"id": "887", "title": "Super Egg Drop"},
    {"id": "65",  "title": "Valid Number"},
    {"id": "488", "title": "Zuma Game"},
    {"id": "218", "title": "The Skyline Problem"},
    {"id": "736", "title": "Parse Lisp Expression"}
]

# Template untuk setiap bahasa biar gak kosong melompong
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

public class Solution {{
    public static void main(String[] args) {{
        // Test driver
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
    // Your code here
}};
""",
    "python": """# Author: {author}
# Date: {date}
# Problem: {full_title}
# Link: {link}

import math
from typing import List, Optional

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
        # Ubah "Super Egg Drop" jadi "super-egg-drop"
        clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        return re.sub(r'[\s-]+', '-', clean).strip().lower()

    def _generate_readme(self, path: Path, full_title: str, link: str):
        readme_path = path / "README.md"
        if not readme_path.exists():
            content = f"# {full_title}\n\nProblem Link: [{full_title}]({link})\n\n## Description\n\n(Add description here)"
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(content)

    def create_problem(self, prob_id: str, title: str):
        slug = self._sanitize_title(title)
        folder_name = f"{prob_id}-{slug}"
        full_path = self.problem_dir / folder_name
        full_title = f"{prob_id}. {title}"
        link = f"https://leetcode.com{slug}/"
        
        print(f"[*] Processing: {full_title}...")
        self._ensure_dir(full_path)
        self._generate_readme(full_path, full_title, link)

        date_now = datetime.datetime.now().strftime("%Y-%m-%d")

        for lang, filename in FILE_MAP.items():
            lang_path = full_path / lang
            self._ensure_dir(lang_path)
            
            file_path = lang_path / filename
            
            # Safety Check: Jangan overwrite kalau file udah ada isinya
            if file_path.exists() and file_path.stat().st_size > 0:
                print(f"    [SKIP] {lang}/{filename} already exists.")
                continue

            # Inject Template
            code_content = TEMPLATES[lang].format(
                author=AUTHOR,
                date=date_now,
                full_title=full_title,
                link=link,
                package_name=lang
            )

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code_content)
            
            print(f"    [OK] Generated {lang} template.")

    def run_wizard(self):
        print("="*50)
        print("   ⚔️  THE SACRED LEETCODE GENERATOR  ⚔️")
        print("="*50)
        print("1. Generate SINGLE Problem (Manual Input)")
        print("2. Generate THE SACRED LIST (887, 65, 488, 218, 736)")
        print("="*50)
        
        choice = input("Select Mode [1/2]: ").strip()

        if choice == "1":
            pid = input("Problem ID (e.g., 1): ").strip()
            ptitle = input("Problem Title (e.g., Two Sum): ").strip()
            if pid and ptitle:
                self.create_problem(pid, ptitle)
        elif choice == "2":
            print("\n🚀 Initiating Batch Sequence...\n")
            for prob in TARGET_PROBLEMS_PRESET:
                self.create_problem(prob["id"], prob["title"])
            print("\n✨ All Sacred Problems Generated Successfully.")
        else:
            print("Invalid Choice.")

if __name__ == "__main__":
    app = SacredGenerator()
    app.run_wizard()