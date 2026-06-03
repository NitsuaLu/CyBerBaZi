"""报告模板引擎 (Report Template Engine).

Simple template-based report generation for BaZi analysis.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Report:
    """A complete BaZi analysis report."""
    title: str = "八字命理分析报告"
    sections: list[tuple[str, str]] = field(default_factory=list)

    def add_section(self, heading: str, content: str):
        self.sections.append((heading, content))

    def render(self) -> str:
        """Render the full report as markdown text."""
        lines = [f"# {self.title}", ""]
        for heading, content in self.sections:
            lines.append(f"## {heading}")
            lines.append("")
            lines.append(content)
            lines.append("")
        return "\n".join(lines)

    def render_plain(self) -> str:
        """Render as plain text (no markdown headers)."""
        lines = [f"═══ {self.title} ═══", ""]
        for heading, content in self.sections:
            lines.append(f"【{heading}】")
            lines.append(content)
            lines.append("")
        return "\n".join(lines)
