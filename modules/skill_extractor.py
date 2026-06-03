import re
from typing import List

class SkillExtractor:
    def __init__(self, skills_file: str = None):
        self.skills_list = []
        if skills_file:
            try:
                with open(skills_file, 'r', encoding='utf-8') as f:
                    self.skills_list = [line.strip() for line in f if line.strip()]
            except FileNotFoundError:
                self.skills_list = []

    def extract(self, text: str) -> List[str]:
        """Extract known skills from free text using simple matching.

        This is a lightweight extractor intended as a starting point. It
        performs case-insensitive substring and token matching against a
        configurable skills list.
        """
        if not text:
            return []

        found = set()
        lower = text.lower()
        for skill in self.skills_list:
            s = skill.lower()
            # match whole words or simple substrings
            if re.search(r'\b' + re.escape(s) + r'\b', lower) or s in lower:
                found.add(skill)

        return sorted(found)
