"""Block inspection helpers for future diagnostics."""
from __future__ import annotations
import re
_CODE_RE = re.compile(r"```([\w-]*)\n(.*?)```", re.DOTALL)
def extract_code_languages(markdown: str) -> list[str]:
    """Extract fenced code block languages.

    Args:
        markdown: Markdown text.

    Returns:
        Code block language labels.

    Raises:
        None.

    Examples:
        >>> extract_code_languages('```python\nprint(1)\n```')
        ['python']
    """
    return [match.group(1) or "text" for match in _CODE_RE.finditer(markdown)]
