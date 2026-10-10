import os
import re
import datetime
from pathlib import Path

AUTHOR = "taro902"
GITHUB_REPO = "https://github.com"

BATCH_3_PROBLEMS = [
    {"id": "30",  "title": "Substring with Concatenation of All Words"},
    {"id": "32",  "title": "Longest Valid Parentheses"},
    {"id": "41",  "title": "First Missing Positive"},
    {"id": "44",  "title": "Wildcard Matching"},
    {"id": "60",  "title": "Permutation Sequence"},
    {"id": "68",  "title": "Text Justification"},
    {"id": "76",  "title": "Minimum Window Substring"},
    {"id": "85",  "title": "Maximal Rectangle"},
    {"id": "87",  "title": "Scramble String"},
    {"id": "115", "title": "Distinct Subsequences"},
    {"id": "123", "title": "Best Time to Buy and Sell Stock III"},
    {"id": "124", "title": "Binary Tree Maximum Path Sum"},
    {"id": "132", "title": "Palindrome Partitioning II"},
    {"id": "135", "title": "Candy"},
    {"id": "140", "title": "Word Break II"},
    {"id": "149", "title": "Max Points on a Line"},
    {"id": "154", "title": "Find Minimum in Rotated Sorted Array II"},
    {"id": "164", "title": "Maximum Gap"},
    {"id": "174", "title": "Dungeon Game"},
    {"id": "188", "title": "Best Time to Buy and Sell Stock IV"},
    {"id": "212", "title": "Word Search II"},
    {"id": "214", "title": "Shortest Palindrome"},
    {"id": "224", "title": "Basic Calculator"},
    {"id": "239", "title": "Sliding Window Maximum"},
    {"id": "273", "title": "Integer to English Words"}
]

TEMPLATES = {
    "c": """#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <limits.h>

""",
    "java": """package {package_name};

import java.util.*;
import java.util.stream.*;
import java.math.*;

public class Solution {{
    public static void main(String[] args) {{
    }}
}}
""",
    "javascript": """/**
 * @param {{any}} args
 * @return {{any}}
 */
var solution = function(args) {{
}};
""",
    "python": """import math
from typing import List, Optional, Dict, Set
from collections import defaultdict, deque

class Solution:
    def solve(self):
        pass
""",
    "racket": """(define/contract (solution args)
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

README_TEMPLATE = """# {full_title} ({lang_title})

| Status | Runtime | Memory | Language |
| --- | --- | --- | --- |
| **Accepted** | 0 ms | 0.0 MB | {lang_title} |

## 🔗 Link
[LeetCode Problem: {title}]({link})

## 📸 Proof of Submission
> ![Proof](https://placeholder.com)

## 🧠 Explanation & Complexity
- **Time Complexity:** $O(...)$
- **Space Complexity:** $O(...)$
"""

class Batch3Generator:
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

    def run(self):
        print("Initializing Batch 3 Protocol...")
        
        for prob in BATCH_3_PROBLEMS:
            slug = self._sanitize_title(prob["title"])
            folder_name = f"{prob['id']}-{slug}"
            full_path = self.problem_dir / folder_name
            full_title = f"{prob['id']}. {prob['title']}"
            link = f"https://leetcode.com{slug}/"
            
            print(f"[*] Deploying: {full_title}")
            self._ensure_dir(full_path)

            for lang, filename in FILE_MAP.items():
                lang_path = full_path / lang
                self._ensure_dir(lang_path)
                
                file_path = lang_path / filename
                if not file_path.exists():
                    content = TEMPLATES[lang].format(package_name=lang)
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                
                readme_path = lang_path / "README.md"
                if not readme_path.exists():
                    readme_content = README_TEMPLATE.format(
                        full_title=full_title,
                        title=prob["title"],
                        lang_title=lang.capitalize(),
                        link=link
                    )
                    with open(readme_path, "w", encoding="utf-8") as f:
                        f.write(readme_content)

        print("\nBatch 3 Successfully Deployed.")

if __name__ == "__main__":
    app = Batch3Generator()
    app.run()
