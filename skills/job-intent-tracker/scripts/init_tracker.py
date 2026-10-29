#!/usr/bin/env python3
"""
init_tracker.py — initialize the job application tracking sheet

Usage:
    python init_tracker.py --format xlsx --output tracker.xlsx
    python init_tracker.py --format md   --output tracker.md

xlsx mode generates an Excel file with headers, dropdown validation, and conditional formatting.
md mode generates a lightweight Markdown table, easy to paste into Notion / Obsidian / Lark docs.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

COLUMNS = [
    "Company",
    "Role",
    "Source",        # Recruiter / Careers site / Referral / Job board / Other
    "JD Link",
    "Application Date",
    "Current Stage",  # Applied / Written test / Interview 1 / Interview 2 / Interview 3 / HR interview / Offer / Rejected / No response
    "Next Action",
    "Deadline",
    "Salary Range",
    "Referrer",
    "Notes",
]

STAGE_OPTIONS = [
    "Applied", "Written test", "Interview 1", "Interview 2", "Interview 3", "HR interview", "Offer", "Rejected", "No response",
]

SOURCE_OPTIONS = ["Careers site", "Referral", "Job board", "Recruiter", "Campus recruiting", "Other"]


def write_md(path: Path) -> None:
    header = "| " + " | ".join(COLUMNS) + " |"
    sep = "| " + " | ".join(["---"] * len(COLUMNS)) + " |"
    sample = "| Example Corp | Senior Product Manager | Referral | https://... | 2026-05-07 | Applied | Waiting for HR feedback | 2026-05-14 | 40-55k | John Doe | Referral code ABC123 |"
    legend_lines = [
        "",
        "## Field Notes",
        "",
        f"- **Source**: {' / '.join(SOURCE_OPTIONS)}",
        f"- **Current Stage**: {' / '.join(STAGE_OPTIONS)}",
        "- **Next Action**: write one concrete, executable step, e.g. 'send a thank-you note before 5/10' or 'if no HR reply by 5/15, follow up'",
        "- **No response**: the status for 7+ days without feedback; a reminder to follow up proactively or move on",
        "",
    ]
    content = "\n".join([
        "# Application Tracking Sheet",
        "",
        header,
        sep,
        sample,
        *legend_lines,
    ])
    path.write_text(content, encoding="utf-8")
    print(f"✓ Markdown tracking sheet generated: {path}")


def write_xlsx(path: Path) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Alignment, Font, PatternFill
        from openpyxl.worksheet.datavalidation import DataValidation
        from openpyxl.formatting.rule import CellIsRule
    except ImportError:
        print(
            "✗ openpyxl is missing. Install it first: pip install openpyxl --break-system-packages",
            file=sys.stderr,
        )
        sys.exit(1)

    wb = Workbook()
    ws = wb.active
    ws.title = "Application Tracking"

    # Header row
    ws.append(COLUMNS)
    header_fill = PatternFill("solid", fgColor="305496")
    header_font = Font(bold=True, color="FFFFFF")
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Column widths
    widths = [16, 22, 10, 28, 12, 10, 26, 12, 14, 10, 30]
    for idx, w in enumerate(widths, start=1):
        ws.column_dimensions[chr(64 + idx)].width = w

    # Sample row
    sample_row = [
        "Example Corp",
        "Senior Product Manager",
        "Referral",
        "https://example.com/jd/123",
        "2026-05-07",
        "Applied",
        "If no reply by 5/14, send a follow-up email",
        "2026-05-14",
        "40-55k",
        "John Doe",
        "Referral code ABC123",
    ]
    ws.append(sample_row)

    # Dropdown validation: Source (column C)
    dv_source = DataValidation(
        type="list",
        formula1=f'"{",".join(SOURCE_OPTIONS)}"',
        allow_blank=True,
    )
    dv_source.add(f"C2:C200")
    ws.add_data_validation(dv_source)

    # Dropdown validation: Current Stage (column F)
    dv_stage = DataValidation(
        type="list",
        formula1=f'"{",".join(STAGE_OPTIONS)}"',
        allow_blank=True,
    )
    dv_stage.add(f"F2:F200")
    ws.add_data_validation(dv_stage)

    # Conditional formatting: column F — Offer green, Rejected gray, No response yellow
    ws.conditional_formatting.add(
        "F2:F200",
        CellIsRule(operator="equal", formula=['"Offer"'],
                   fill=PatternFill("solid", fgColor="C6EFCE")),
    )
    ws.conditional_formatting.add(
        "F2:F200",
        CellIsRule(operator="equal", formula=['"Rejected"'],
                   fill=PatternFill("solid", fgColor="D9D9D9")),
    )
    ws.conditional_formatting.add(
        "F2:F200",
        CellIsRule(operator="equal", formula=['"No response"'],
                   fill=PatternFill("solid", fgColor="FFEB9C")),
    )

    # Freeze the header row
    ws.freeze_panes = "A2"

    # Second sheet: usage instructions
    legend = wb.create_sheet("How to Use")
    legend["A1"] = "Application Tracking Sheet — How to Use"
    legend["A1"].font = Font(bold=True, size=14)
    legend_lines = [
        "",
        "1. Add a new row every time you apply to a role.",
        "2. 'Source' and 'Current Stage' are dropdowns — just pick.",
        "3. 'Next Action' must be a concrete, executable step + a time point.",
        "4. When a row has been silent for 7+ days, set 'Current Stage' to 'No response' to remind yourself to follow up or move on.",
        "5. Once you get an Offer the row turns green; rejected turns gray, for easy distinction.",
        "6. Set a fixed weekly review time (e.g. Sunday evening) to go over this sheet.",
        "",
        "If you want stats like 'how many in interviews / total applications / no-response rate',",
        "you can ask the agent to build a dashboard (artifact) for you.",
    ]
    for line in legend_lines:
        legend.append([line])

    wb.save(path)
    print(f"✓ Excel tracking sheet generated: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Initialize the job application tracking sheet")
    parser.add_argument(
        "--format", choices=["xlsx", "md"], default="xlsx", help="Output format"
    )
    parser.add_argument(
        "--output", required=True, help="Output file path (including file name)"
    )
    args = parser.parse_args()

    out = Path(args.output).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)

    if args.format == "xlsx":
        write_xlsx(out)
    else:
        write_md(out)


if __name__ == "__main__":
    main()
