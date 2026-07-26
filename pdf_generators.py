
# ============================================================
# MEDIASSIST AI
# Professional Hospital Style PDF Generator
# Version 2.0
# Developed for IBM NASSCOM GenAI Project
# ============================================================

from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    PageBreak,
    KeepTogether,
    ListFlowable,
    ListItem
)

from reportlab.graphics.shapes import (
    Drawing,
    Rect,
    String,
    Circle,
    Line
)

# ============================================================
# PAGE SETTINGS
# ============================================================

PAGE_WIDTH, PAGE_HEIGHT = A4

LEFT_MARGIN = 18 * mm
RIGHT_MARGIN = 18 * mm
TOP_MARGIN = 18 * mm
BOTTOM_MARGIN = 18 * mm

CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN

# ============================================================
# COLOUR PALETTE
# ============================================================

NAVY = colors.HexColor("#0D47A1")
PRIMARY = colors.HexColor("#1565C0")
SECONDARY = colors.HexColor("#42A5F5")

LIGHT_BLUE = colors.HexColor("#E3F2FD")
VERY_LIGHT_BLUE = colors.HexColor("#F7FBFF")

GREEN = colors.HexColor("#2E7D32")
LIGHT_GREEN = colors.HexColor("#E8F5E9")

ORANGE = colors.HexColor("#F57C00")
LIGHT_ORANGE = colors.HexColor("#FFF3E0")

RED = colors.HexColor("#C62828")
LIGHT_RED = colors.HexColor("#FFEBEE")

GREY = colors.HexColor("#616161")
LIGHT_GREY = colors.HexColor("#EEEEEE")

DARK = colors.HexColor("#212121")

WHITE = colors.white

# ============================================================
# REPORT INFORMATION
# ============================================================

PROJECT_NAME = "MediAssist AI"

PROJECT_SUBTITLE = "AI Powered Healthcare Diagnosis Report"

PROJECT_VERSION = "Version 2.0"

MODEL_NAME = "Random Forest Classifier"

DEVELOPER = "Aditi Agrawal"

ORGANIZATION = "IBM NASSCOM GenAI Project"

# ============================================================
# STYLES
# ============================================================

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    fontName="Helvetica-Bold",
    fontSize=24,
    leading=30,
    alignment=TA_CENTER,
    textColor=WHITE,
)

SUBTITLE_STYLE = ParagraphStyle(
    "SubtitleStyle",
    parent=styles["Heading2"],
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    alignment=TA_CENTER,
    textColor=WHITE,
)

SECTION_STYLE = ParagraphStyle(
    "SectionStyle",
    parent=styles["Heading2"],
    fontName="Helvetica-Bold",
    fontSize=14,
    leading=18,
    textColor=PRIMARY,
    spaceAfter=8,
    spaceBefore=12,
)

BODY_STYLE = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=10,
    leading=18,
    textColor=DARK,
)

SMALL_STYLE = ParagraphStyle(
    "SmallStyle",
    parent=styles["BodyText"],
    fontName="Helvetica",
    fontSize=8,
    leading=12,
    textColor=GREY,
)

# ============================================================
# SMALL HELPERS
# ============================================================

def safe_text(value, default="Not Available"):
    """
    Return a clean printable string.
    """

    if value is None:
        return default

    if str(value).strip() == "":
        return default

    return str(value)


def format_bmi(bmi):
    """
    Format BMI.
    """

    if bmi is None:
        return "Not Available"

    if isinstance(bmi, (int, float)):
        return f"{bmi:.1f}"

    return str(bmi)


def bmi_status(bmi):

    if not isinstance(bmi, (int, float)):
        return "Not Available"

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


def report_id():

    return datetime.now().strftime("MA-%Y%m%d-%H%M%S")
# ============================================================
# HOSPITAL HEADER
# ============================================================

def hospital_header():

    drawing = Drawing(CONTENT_WIDTH, 85)

    # Background Banner
    drawing.add(
        Rect(
            0,
            18,
            CONTENT_WIDTH,
            67,
            fillColor=NAVY,
            strokeColor=NAVY
        )
    )

    # Bottom Accent Strip
    drawing.add(
        Rect(
            0,
            14,
            CONTENT_WIDTH,
            4,
            fillColor=SECONDARY,
            strokeColor=SECONDARY
        )
    )

    # Medical Logo
    drawing.add(
        Circle(
            30,
            52,
            16,
            fillColor=WHITE,
            strokeColor=WHITE
        )
    )

    drawing.add(
        String(
            30,
            46,
            "+",
            textAnchor="middle",
            fontName="Helvetica-Bold",
            fontSize=20,
            fillColor=PRIMARY
        )
    )

    # Main Title
    drawing.add(
        String(
            58,
            60,
            PROJECT_NAME,
            fontName="Helvetica-Bold",
            fontSize=22,
            fillColor=WHITE
        )
    )

    drawing.add(
        String(
            58,
            43,
            PROJECT_SUBTITLE,
            fontName="Helvetica",
            fontSize=10,
            fillColor=WHITE
        )
    )

    drawing.add(
        String(
            58,
            29,
            ORGANIZATION,
            fontName="Helvetica",
            fontSize=8,
            fillColor=LIGHT_BLUE
        )
    )

    # Report Information
    now = datetime.now()

    drawing.add(
        String(
            CONTENT_WIDTH - 175,
            60,
            "REPORT ID",
            fontName="Helvetica-Bold",
            fontSize=8,
            fillColor=LIGHT_BLUE
        )
    )

    drawing.add(
        String(
            CONTENT_WIDTH - 175,
            47,
            report_id(),
            fontSize=9,
            fillColor=WHITE
        )
    )

    drawing.add(
        String(
            CONTENT_WIDTH - 175,
            33,
            now.strftime("%d %b %Y"),
            fontSize=8,
            fillColor=WHITE
        )
    )

    drawing.add(
        String(
            CONTENT_WIDTH - 175,
            21,
            now.strftime("%I:%M %p"),
            fontSize=8,
            fillColor=WHITE
        )
    )

    return drawing


# ============================================================
# SECTION TITLE
# ============================================================

def section(title):

    return Paragraph(

        f"""
        <font color="#1565C0">
        <b>{title}</b>
        </font>
        """,

        SECTION_STYLE

    )


# ============================================================
# DIVIDER
# ============================================================

def divider():

    return HRFlowable(

        width="100%",

        thickness=0.8,

        color=LIGHT_GREY,

        spaceBefore=8,

        spaceAfter=10

    )


# ============================================================
# FOOTER
# ============================================================

def footer(canvas, doc):

    canvas.saveState()

    canvas.setStrokeColor(LIGHT_GREY)

    canvas.line(

        LEFT_MARGIN,

        18,

        PAGE_WIDTH - RIGHT_MARGIN,

        18

    )

    canvas.setFont("Helvetica", 8)

    canvas.setFillColor(GREY)

    canvas.drawString(

        LEFT_MARGIN,

        8,

        f"{PROJECT_NAME} | {MODEL_NAME}"

    )

    canvas.drawRightString(

        PAGE_WIDTH - RIGHT_MARGIN,

        8,

        f"Page {canvas.getPageNumber()}"

    )

    canvas.restoreState()

# ============================================================
# CONFIDENCE PROGRESS BAR
# ============================================================

def confidence_bar(confidence):

    if confidence is None:
        confidence = 0

    confidence = max(0, min(100, float(confidence)))

    drawing = Drawing(220, 22)

    drawing.add(
        Rect(
            0,
            7,
            180,
            8,
            fillColor=LIGHT_GREY,
            strokeColor=LIGHT_GREY
        )
    )

    colour = GREEN

    if confidence < 70:
        colour = ORANGE

    if confidence < 50:
        colour = RED

    drawing.add(
        Rect(
            0,
            7,
            180 * confidence / 100,
            8,
            fillColor=colour,
            strokeColor=colour
        )
    )

    drawing.add(
        String(
            188,
            6,
            f"{confidence:.1f}%",
            fontName="Helvetica-Bold",
            fontSize=9,
            fillColor=DARK
        )
    )

    return drawing


# ============================================================
# SEVERITY
# ============================================================

def severity_details(confidence):

    if confidence >= 90:
        return "HIGH", RED, LIGHT_RED

    elif confidence >= 70:
        return "MEDIUM", ORANGE, LIGHT_ORANGE

    return "LOW", GREEN, LIGHT_GREEN


# ============================================================
# BMI BADGE
# ============================================================

def bmi_badge(bmi):

    status = bmi_status(bmi)

    if status == "Normal":
        return status, GREEN, LIGHT_GREEN

    elif status == "Overweight":
        return status, ORANGE, LIGHT_ORANGE

    elif status == "Obese":
        return status, RED, LIGHT_RED

    return status, GREY, LIGHT_GREY


# ============================================================
# PATIENT INFORMATION CARD
# ============================================================

def patient_card(
    name,
    age,
    gender,
    blood_group,
    height,
    weight,
    bmi,
    existing_disease,
    allergies
):

    bmi_text = format_bmi(bmi)
    bmi_state, _, _ = bmi_badge(bmi)

    rows = [

        ["Name", safe_text(name)],
        ["Age", safe_text(age)],
        ["Gender", safe_text(gender)],
        ["Blood Group", safe_text(blood_group)],
        ["Height", safe_text(f"{height} cm" if height else None)],
        ["Weight", safe_text(f"{weight} kg" if weight else None)],
        ["BMI", bmi_text],
        ["BMI Status", bmi_state],
        ["Existing Disease", safe_text(existing_disease, "None")],
        ["Allergies", safe_text(allergies, "None")]

    ]

    table = Table(
        rows,
        colWidths=[120, CONTENT_WIDTH - 120]
    )

    style = [

        ("GRID",(0,0),(-1,-1),0.35,LIGHT_GREY),

        ("BACKGROUND",(0,0),(0,-1),LIGHT_BLUE),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

        ("TEXTCOLOR",(0,0),(0,-1),NAVY),

        ("BOTTOMPADDING",(0,0),(-1,-1),8),

        ("TOPPADDING",(0,0),(-1,-1),8),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE")

    ]

    for i in range(len(rows)):

        style.append(
            (
                "BACKGROUND",
                (1, i),
                (1, i),
                WHITE if i % 2 == 0 else VERY_LIGHT_BLUE
            )
        )

    table.setStyle(TableStyle(style))

    return table


# ============================================================
# DIAGNOSIS CARD
# ============================================================

def diagnosis_card(
    disease,
    confidence,
    doctor
):

    severity, text_colour, background = severity_details(confidence)

    rows = [

        ["Predicted Disease", safe_text(disease)],

        ["Recommended Doctor", safe_text(doctor)],

        ["Disease Severity", severity]

    ]

    table = Table(
        rows,
        colWidths=[150, CONTENT_WIDTH - 150]
    )

    style = [

        ("GRID",(0,0),(-1,-1),0.35,LIGHT_GREY),

        ("BACKGROUND",(0,0),(0,-1),PRIMARY),

        ("TEXTCOLOR",(0,0),(0,-1),WHITE),

        ("FONTNAME",(0,0),(0,-1),"Helvetica-Bold"),

        ("BOTTOMPADDING",(0,0),(-1,-1),9),

        ("TOPPADDING",(0,0),(-1,-1),9),

    ]

    for i in range(len(rows)):
        style.append(
            (
                "BACKGROUND",
                (1, i),
                (1, i),
                WHITE
            )
        )

    style.append(
        (
            "BACKGROUND",
            (1,2),
            (1,2),
            background
        )
    )

    style.append(
        (
            "TEXTCOLOR",
            (1,2),
            (1,2),
            text_colour
        )
    )

    table.setStyle(TableStyle(style))

    return table

# ============================================================
# INFO CARD
# ============================================================

def info_card(title, text):

    if text is None or str(text).strip() == "":
        text = "Not Available"

    title_para = Paragraph(
        f"<font color='#1565C0'><b>{title}</b></font>",
        SECTION_STYLE
    )

    body_para = Paragraph(
        safe_text(text),
        BODY_STYLE
    )

    table = Table(
        [[title_para], [body_para]],
        colWidths=[CONTENT_WIDTH]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,0), LIGHT_BLUE),
            ("BACKGROUND", (0,1), (-1,-1), WHITE),

            ("BOX", (0,0), (-1,-1), 0.8, LIGHT_GREY),
            ("LINEBELOW", (0,0), (-1,0), 0.6, PRIMARY),

            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("TOPPADDING", (0,0), (-1,-1), 10),

            ("LEFTPADDING", (0,0), (-1,-1), 12),
            ("RIGHTPADDING", (0,0), (-1,-1), 12),
        ])
    )

    return table


# ============================================================
# BULLET CARD
# ============================================================

def bullet_card(title, items, icon="•"):

    if not items:
        items = ["Not Available"]

    bullet_items = []

    for item in items:

        bullet_items.append(

            ListItem(

                Paragraph(

                    safe_text(item),

                    BODY_STYLE

                )

            )

        )

    bullets = ListFlowable(

        bullet_items,

        bulletType="bullet",

        start=icon

    )

    title_para = Paragraph(

        f"<font color='#1565C0'><b>{title}</b></font>",

        SECTION_STYLE

    )

    table = Table(

        [

            [title_para],

            [bullets]

        ],

        colWidths=[CONTENT_WIDTH]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,0),LIGHT_BLUE),

            ("BACKGROUND",(0,1),(-1,-1),WHITE),

            ("BOX",(0,0),(-1,-1),0.8,LIGHT_GREY),

            ("LINEBELOW",(0,0),(-1,0),0.6,PRIMARY),

            ("BOTTOMPADDING",(0,0),(-1,-1),10),

            ("TOPPADDING",(0,0),(-1,-1),10),

            ("LEFTPADDING",(0,0),(-1,-1),12),

            ("RIGHTPADDING",(0,0),(-1,-1),12)

        ])

    )

    return table


# ============================================================
# DISCLAIMER CARD
# ============================================================

def disclaimer_card():

    warning = Paragraph(

        """
        <font color='#C62828'><b>Important Medical Disclaimer</b></font>
        <br/><br/>

        This report has been generated using an Artificial Intelligence
        model for educational purposes only.

        <br/><br/>

        It should not be used as a substitute for professional
        medical advice, diagnosis or treatment.

        <br/><br/>

        Always consult a qualified healthcare professional before
        making any medical decisions.
        """,

        BODY_STYLE

    )

    table = Table(

        [[warning]],

        colWidths=[CONTENT_WIDTH]

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),LIGHT_ORANGE),

            ("BOX",(0,0),(-1,-1),1.2,ORANGE),

            ("BOTTOMPADDING",(0,0),(-1,-1),14),

            ("TOPPADDING",(0,0),(-1,-1),14),

            ("LEFTPADDING",(0,0),(-1,-1),14),

            ("RIGHTPADDING",(0,0),(-1,-1),14)

        ])

    )

    return table


# ============================================================
# SYMPTOMS CARD
# ============================================================

def symptoms_card(symptoms):

    if not symptoms:
        symptoms = ["No symptoms selected"]

    formatted = []

    for symptom in symptoms:

        formatted.append(

            "✔ " +

            safe_text(symptom).replace("_", " ").title()

        )

    return bullet_card(

        "🩺 Selected Symptoms",

        formatted

    )

# ============================================================
# GENERATE PDF
# ============================================================

def generate_pdf(
    name,
    age,
    gender,
    disease,
    doctor,
    description,
    precautions,
    remedies,
    foods,
    tests,
    symptoms=None,
    confidence=None,
    bmi=None,
    blood_group=None,
    height=None,
    weight=None,
    existing_disease=None,
    allergies=None,
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
    )

    story = []

    # ========================================================
    # HEADER
    # ========================================================

    story.append(hospital_header())

    story.append(Spacer(1, 12))

    # ========================================================
    # REPORT INFORMATION
    # ========================================================

    report_table = Table(
        [
            ["Report ID", report_id()],
            ["Generated On", datetime.now().strftime("%d %B %Y")],
            ["Generated At", datetime.now().strftime("%I:%M %p")],
            ["Model", MODEL_NAME],
            ["Version", PROJECT_VERSION],
        ],
        colWidths=[120, CONTENT_WIDTH - 120],
    )

    report_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, LIGHT_GREY),
                ("BACKGROUND", (0, 0), (0, -1), LIGHT_BLUE),
                ("BACKGROUND", (1, 0), (1, -1), WHITE),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("TEXTCOLOR", (0, 0), (0, -1), NAVY),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(report_table)

    story.append(Spacer(1, 14))

    # ========================================================
    # PATIENT INFORMATION
    # ========================================================

    story.append(section("👤 Patient Information"))

    story.append(
        patient_card(
            name,
            age,
            gender,
            blood_group,
            height,
            weight,
            bmi,
            existing_disease,
            allergies,
        )
    )

    story.append(Spacer(1, 14))

    # ========================================================
    # AI DIAGNOSIS
    # ========================================================

    story.append(section("🤖 AI Diagnosis"))

    story.append(
        diagnosis_card(
            disease,
            confidence,
            doctor,
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        Paragraph(
            "<b>Prediction Confidence</b>",
            BODY_STYLE,
        )
    )

    story.append(
        confidence_bar(confidence)
    )

    story.append(Spacer(1, 15))

    # ========================================================
    # SELECTED SYMPTOMS
    # ========================================================

    story.append(symptoms_card(symptoms))

    story.append(Spacer(1, 12))

    # ========================================================
    # DISEASE DESCRIPTION
    # ========================================================

    story.append(

        info_card(

            "📖 Disease Description",

            description

        )

    )

    story.append(Spacer(1, 12))

    # ========================================================
    # PRECAUTIONS
    # ========================================================

    story.append(

        bullet_card(

            "💊 Recommended Precautions",

            precautions

        )

    )

    story.append(Spacer(1, 12))

    # ========================================================
    # HOME REMEDIES
    # ========================================================

    story.append(

        bullet_card(

            "🏠 Home Remedies",

            remedies

        )

    )

    story.append(Spacer(1, 12))

    # ========================================================
    # FOODS TO AVOID
    # ========================================================

    story.append(

        bullet_card(

            "🚫 Foods To Avoid",

            foods

        )

    )

    story.append(Spacer(1, 12))

    # ========================================================
    # MEDICAL TESTS
    # ========================================================

    story.append(

        bullet_card(

            "🧪 Suggested Medical Tests",

            tests

        )

    )

    story.append(Spacer(1, 16))

    # ========================================================
    # DISCLAIMER
    # ========================================================

    story.append(

        disclaimer_card()

    )

    story.append(Spacer(1, 18))

    # ========================================================
    # DEVELOPER INFORMATION
    # ========================================================

    footer_table = Table(

        [[

            Paragraph(

                f"""

                <b>Developed By</b><br/>

                {DEVELOPER}<br/>

                {ORGANIZATION}<br/><br/>

                <b>Machine Learning Model</b><br/>

                {MODEL_NAME}<br/>

                <b>Project Version</b><br/>

                {PROJECT_VERSION}

                """,

                SMALL_STYLE

            )

        ]],

        colWidths=[CONTENT_WIDTH]

    )

    footer_table.setStyle(

        TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),VERY_LIGHT_BLUE),

            ("BOX",(0,0),(-1,-1),0.5,LIGHT_GREY),

            ("BOTTOMPADDING",(0,0),(-1,-1),12),

            ("TOPPADDING",(0,0),(-1,-1),12),

            ("LEFTPADDING",(0,0),(-1,-1),12),

            ("RIGHTPADDING",(0,0),(-1,-1),12)

        ])

    )

    story.append(footer_table)

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(

        story,

        onFirstPage=footer,

        onLaterPages=footer

    )

    buffer.seek(0)

    return buffer