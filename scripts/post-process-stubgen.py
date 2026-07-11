"""
Adds the @runtime_checkable decorator back to the Protocol class definitions,
after the stubgen tool regenerated it.
By default it strips this decorator, which can result in some issues later.
"""

import re
from pathlib import Path


def post_process_stub(filepath: Path):
    content = filepath.read_text()
    protocol_class_pat = re.compile(
        r"^(class \w+Protocol(?:\[[^\]]+\])?\(Protocol\):)", re.MULTILINE
    )

    if not protocol_class_pat.search(content):
        return

    def decorate(match: re.Match[str]):
        start_idx = match.start()
        preceding = content[max(0, start_idx - 40) : start_idx]
        if "@runtime_checkable" in preceding:
            return match.group(1)
        return "@runtime_checkable\n" + match.group(1)

    new_content = protocol_class_pat.sub(decorate, content)

    if new_content != content:
        has_import = False
        for line in content.splitlines():
            if "typing" in line and "runtime_checkable" in line:
                has_import = True
                break
        if not has_import:
            new_content = "from typing import runtime_checkable\n" + new_content
        _ = filepath.write_text(new_content)
        print(f"Post-processed: Added @runtime_checkable to {filepath.name}")


for filepath in Path("src/cflowpy").glob("*.pyi"):
    post_process_stub(filepath)
