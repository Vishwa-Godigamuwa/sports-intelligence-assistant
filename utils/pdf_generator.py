import os
import re
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)


# =========================================================
# FONT SETUP
# =========================================================

def setup_fonts():

    font_dir = r"C:\Windows\Fonts"

    regular = os.path.join(font_dir, "times.ttf")
    bold = os.path.join(font_dir, "timesbd.ttf")
    italic = os.path.join(font_dir, "timesi.ttf")

    if all(os.path.exists(f) for f in [regular, bold, italic]):

        pdfmetrics.registerFont(
            TTFont("TNR", regular)
        )

        pdfmetrics.registerFont(
            TTFont("TNR-Bold", bold)
        )

        pdfmetrics.registerFont(
            TTFont("TNR-Italic", italic)
        )

        return "TNR", "TNR-Bold", "TNR-Italic"

    return "Times-Roman", "Times-Bold", "Times-Italic"


FONT, FONT_BOLD, FONT_ITALIC = setup_fonts()


# =========================================================
# STYLES
# =========================================================

title_style = ParagraphStyle(
    "Title",
    fontName=FONT_BOLD,
    fontSize=18,
    leading=22,
    textColor=colors.HexColor("#17365D"),
    alignment=1,
    spaceAfter=5
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    fontName=FONT_ITALIC,
    fontSize=11,
    leading=14,
    alignment=1,
    textColor=colors.grey,
    spaceAfter=18
)

heading_style = ParagraphStyle(
    "Heading",
    fontName=FONT_BOLD,
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#17365D"),
    spaceBefore=10,
    spaceAfter=6
)

body_style = ParagraphStyle(
    "Body",
    fontName=FONT,
    fontSize=11,
    leading=16,
    spaceAfter=7
)

question_style = ParagraphStyle(
    "Question",
    fontName=FONT_ITALIC,
    fontSize=11,
    leading=16,
    leftIndent=10,
    rightIndent=10,
    backColor=colors.HexColor("#F4F6F8"),
    borderPadding=8,
    spaceAfter=12
)


# =========================================================
# MARKDOWN CLEANUP
# =========================================================

def clean_text(text):

    text = escape(str(text))

    # Bold Markdown
    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    # Remove Markdown headings
    text = re.sub(
        r"#{1,6}\s*",
        "",
        text
    )

    return text


# =========================================================
# FORMAT AI RESPONSE
# =========================================================

def add_ai_response(elements, text):

    if not text:
        return

    # Put headings onto separate lines if Gemini returned
    # Markdown headings inside one long response.
    text = re.sub(
        r"\s+(#{1,4}\s+)",
        r"\n\1",
        str(text)
    )

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Heading
        if line.startswith("#"):

            heading = line.lstrip("#").strip()

            elements.append(
                Paragraph(
                    clean_text(heading),
                    heading_style
                )
            )

        # Bullet
        elif line.startswith(("- ", "* ", "• ")):

            bullet = line[2:].strip()

            elements.append(
                Paragraph(
                    "• " + clean_text(bullet),
                    body_style
                )
            )

        # Normal paragraph
        else:

            elements.append(
                Paragraph(
                    clean_text(line),
                    body_style
                )
            )


# =========================================================
# PAGE FOOTER
# =========================================================

def add_footer(canvas, doc):

    canvas.saveState()

    width, _ = A4

    canvas.setFont(FONT, 9)
    canvas.setFillColor(colors.grey)

    canvas.drawString(
        20 * mm,
        12 * mm,
        "Sports Intelligence Assistant"
    )

    canvas.drawRightString(
        width - 20 * mm,
        12 * mm,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# =========================================================
# GENERATE PDF
# =========================================================

def generate_pdf(
    report_data,
    filename="coaching_report.pdf"
):

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=22 * mm,
        rightMargin=22 * mm,
        topMargin=20 * mm,
        bottomMargin=22 * mm
    )

    elements = []


    # -----------------------------------------------------
    # Title
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "SPORTS INTELLIGENCE ASSISTANT",
            title_style
        )
    )

    elements.append(
        Paragraph(
            "Personalized Coaching Report",
            subtitle_style
        )
    )


    # -----------------------------------------------------
    # Report Details
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Report Information",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Sport:</b> "
            f"{escape(str(report_data.get('Sport', 'N/A')))}",
            body_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Feature:</b> "
            f"{escape(str(report_data.get('Feature', 'N/A')))}",
            body_style
        )
    )

    elements.append(
        Paragraph(
            f"<b>Generated:</b> "
            f"{datetime.now().strftime('%d %B %Y')}",
            body_style
        )
    )

    elements.append(
        Spacer(1, 8)
    )


    # -----------------------------------------------------
    # User Question
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "User Question",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            escape(
                str(
                    report_data.get(
                        "Question",
                        "No question provided."
                    )
                )
            ),
            question_style
        )
    )


    # -----------------------------------------------------
    # Coaching Advice
    # -----------------------------------------------------

    elements.append(
        Paragraph(
            "Personalized Coaching Advice",
            heading_style
        )
    )

    add_ai_response(
        elements,
        report_data.get("AI Advice", "")
    )


    # -----------------------------------------------------
    # Final Note
    # -----------------------------------------------------

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Important Note",
            heading_style
        )
    )

    elements.append(
        Paragraph(
            (
                "This AI-generated report is intended to support "
                "sports training and development. Recommendations "
                "should be adapted to the athlete's individual "
                "needs, physical condition, and coaching environment."
            ),
            body_style
        )
    )


    # -----------------------------------------------------
    # Build
    # -----------------------------------------------------

    doc.build(
        elements,
        onFirstPage=add_footer,
        onLaterPages=add_footer
    )

    return filename