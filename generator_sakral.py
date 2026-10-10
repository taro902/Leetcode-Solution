import os
import re
from pathlib import Path

AUTHOR = "taro902"

ALL_PROBLEMS = [
    {"id": "887", "title": "Super Egg Drop"},
    {"id": "65",  "title": "Valid Number"},
    {"id": "488", "title": "Zuma Game"},
    {"id": "218", "title": "The Skyline Problem"},
    {"id": "736", "title": "Parse Lisp Expression"},
    {"id": "4",   "title": "Median of Two Sorted Arrays"},
    {"id": "10",  "title": "Regular Expression Matching"},
    {"id": "126", "title": "Word Ladder II"},
    {"id": "84",  "title": "Largest Rectangle in Histogram"},
    {"id": "315", "title": "Count of Smaller Numbers After Self"}
]

LANGUAGES = ["c", "java", "javascript", "python", "racket"]

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

class RestructureSacred:
    def __init__(self):
        self.root_dir = Path(os.getcwd())
        self.problem_dir = self.root_dir / "Problem"

    def _sanitize_title(self, title: str) -> str:
        clean = re.sub(r'[^a-zA-Z0-9\s-]', '', title)
        return re.sub(r'[\s-]+', '-', clean).strip().lower()

    def run(self):
        print("Starting Restructure...")

        for prob in ALL_PROBLEMS:
            slug = self._sanitize_title(prob["title"])
            folder_name = f"{prob['id']}-{slug}"
            full_path = self.problem_dir / folder_name
            full_title = f"{prob['id']}. {prob['title']}"
            link = f"https://leetcode.com{slug}/"

            if not full_path.exists():
                print(f"[SKIP] {folder_name} not found")
                continue

            print(f"[*] Processing: {full_title}")

            main_readme = full_path / "README.md"
            if main_readme.exists():
                os.remove(main_readme)
                print(f"    [-] Deleted outer README")

            for lang in LANGUAGES:
                lang_path = full_path / lang
                if not lang_path.exists():
                    continue
                
                readme_lang_path = lang_path / "README.md"
                
                if not readme_lang_path.exists():
                    content = README_TEMPLATE.format(
                        full_title=full_title,
                        title=prob["title"],
                        lang_title=lang.capitalize(),
                        link=link
                    )
                    with open(readme_lang_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"    [+] Created README in /{lang}")
                else:
                    print(f"    [!] README in /{lang} already exists")

        print("\nDone.")

if __name__ == "__main__":
    app = RestructureSacred()
    app.run()
