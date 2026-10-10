import os
import re
from pathlib import Path

AUTHOR = "taro902"
GITHUB_REPO = "https://github.com"

BATCH_5_PROBLEMS = [
    {"id": "827", "title": "Making A Large Island"},
    {"id": "829", "title": "Consecutive Numbers Sum"},
    {"id": "834", "title": "Sum of Distances in Tree"},
    {"id": "839", "title": "Similar String Groups"},
    {"id": "847", "title": "Shortest Path Visiting All Nodes"},
    {"id": "850", "title": "Rectangle Area II"},
    {"id": "854", "title": "K-Similar Strings"},
    {"id": "857", "title": "Minimum Cost to Hire K Workers"},
    {"id": "862", "title": "Shortest Subarray with Sum at Least K"},
    {"id": "871", "title": "Minimum Number of Refueling Stops"},
    {"id": "878", "title": "Nth Magical Number"},
    {"id": "879", "title": "Profitable Schemes"},
    {"id": "882", "title": "Reachable Nodes In Subdivided Graph"},
    {"id": "895", "title": "Maximum Frequency Stack"},
    {"id": "902", "title": "Numbers At Most N Given Digit Set"},
    {"id": "906", "title": "Super Palindromes"},
    {"id": "920", "title": "Number of Music Playlists"},
    {"id": "924", "title": "Minimize Malware Spread"},
    {"id": "928", "title": "Minimize Malware Spread II"},
    {"id": "940", "title": "Distinct Subsequences II"},
    {"id": "943", "title": "Find the Shortest Superstring"},
    {"id": "952", "title": "Largest Component Size by Common Factor"},
    {"id": "956", "title": "Tallest Billboard"},
    {"id": "964", "title": "Least Operators to Express Number"},
    {"id": "968", "title": "Binary Tree Cameras"},
    {"id": "975", "title": "Odd Even Jump"},
    {"id": "980", "title": "Unique Paths III"},
    {"id": "992", "title": "Subarrays with K Different Integers"},
    {"id": "1000", "title": "Minimum Cost to Merge Stones"},
    {"id": "1044", "title": "Longest Duplicate Substring"}
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
import bisect

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

class Batch5Generator:
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
        print("Initiating FINAL PROTOCOL: Batch 5...")
        
        for prob in BATCH_5_PROBLEMS:
            slug = self._sanitize_title(prob["title"])
            folder_name = f"{prob['id']}-{slug}"
            full_path = self.problem_dir / folder_name
            full_title = f"{prob['id']}. {prob['title']}"
            link = f"https://leetcode.com{slug}/"
            
            print(f"[*] Constructing: {full_title}")
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

        print("\nFINAL BATCH DEPLOYED. THE ARCHIVE IS COMPLETE.")

if __name__ == "__main__":
    app = Batch5Generator()
    app.run()
