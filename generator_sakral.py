import os
import re
from pathlib import Path

AUTHOR = "taro902"
GITHUB_REPO = "https://github.com"

BATCH_4_PROBLEMS = [
    {"id": "301", "title": "Remove Invalid Parentheses"},
    {"id": "312", "title": "Burst Balloons"},
    {"id": "329", "title": "Longest Increasing Path in a Matrix"},
    {"id": "336", "title": "Palindrome Pairs"},
    {"id": "354", "title": "Russian Doll Envelopes"},
    {"id": "363", "title": "Max Sum of Rectangle No Larger Than K"},
    {"id": "403", "title": "Frog Jump"},
    {"id": "407", "title": "Trapping Rain Water II"},
    {"id": "410", "title": "Split Array Largest Sum"},
    {"id": "440", "title": "K-th Smallest in Lexicographical Order"},
    {"id": "460", "title": "LFU Cache"},
    {"id": "472", "title": "Concatenated Words"},
    {"id": "480", "title": "Sliding Window Median"},
    {"id": "493", "title": "Reverse Pairs"},
    {"id": "502", "title": "IPO"},
    {"id": "564", "title": "Find the Closest Palindrome"},
    {"id": "632", "title": "Smallest Range Covering Elements from K Lists"},
    {"id": "679", "title": "24 Game"},
    {"id": "685", "title": "Redundant Connection II"},
    {"id": "719", "title": "Find K-th Smallest Pair Distance"},
    {"id": "726", "title": "Number of Atoms"},
    {"id": "745", "title": "Prefix and Suffix Search"},
    {"id": "757", "title": "Set Intersection Size At Least Two"},
    {"id": "778", "title": "Swim in Rising Water"},
    {"id": "803", "title": "Bricks Falling When Hit"}
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
from typing import List, Optional, Dict, Set, Tuple
from collections import defaultdict, deque, Counter
import heapq

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

class Batch4Generator:
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
        print("Initializing Batch 4: The Relief Provider...")
        
        for prob in BATCH_4_PROBLEMS:
            slug = self._sanitize_title(prob["title"])
            folder_name = f"{prob['id']}-{slug}"
            full_path = self.problem_dir / folder_name
            full_title = f"{prob['id']}. {prob['title']}"
            link = f"https://leetcode.com{slug}/"
            
            print(f"[*] Generating: {full_title}")
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

        print("\nBatch 4 Successfully Deployed.")

if __name__ == "__main__":
    app = Batch4Generator()
    app.run()
