"""Theme models for Markprint."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class ThemeSpec(BaseModel):
    """Theme metadata and loaded assets."""

    model_config = ConfigDict(extra="forbid")
    name: str
    css: str = ""
    template: str = "document.html.j2"
    base_dir: Path | None = None
    pygments_style: str = "default"
    metadata: dict[str, str] = Field(default_factory=dict)
