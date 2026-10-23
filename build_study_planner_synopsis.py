# -*- coding: utf-8 -*-
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.pdfgen import canvas

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_border()
            super().showPage()
        super().save()

    def draw_page_border(self):
        self.saveState()
        w, h = self._pagesize
        margin = 32
        self.setStrokeColor(colors.HexColor("#222222"))
        self.setLineWidth(0.8)
        self.rect(margin, margin, w - 2 * margin, h - 2 * margin, stroke=1, fill=0)
        self.restoreState()

def build_pdf(filename="AI_Study_Planner_Synopsis_Shresthi_Kesharwani.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48
    )
    
    styles = getSampleStyleSheet()
    
    t_center_bold_lg = ParagraphStyle(
        'TCenterBoldLg',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=16.5,
        leading=22,
        alignment=1,
        textColor=colors.black,
        spaceAfter=12
    )
    
    t_center_bold_md = ParagraphStyle(
        'TCenterBoldMd',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=15,
        leading=20,
        alignment=1,
        textColor=colors.black,
        spaceAfter=10
    )
    
    t_center_regular = ParagraphStyle(
        'TCenterReg',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=12.5,
        leading=18,
        alignment=1,
        textColor=colors.black,
        spaceAfter=4
    )
    
    t_center_italic = ParagraphStyle(
        'TCenterItalic',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=17,
        alignment=1,
        textColor=colors.black,
        spaceAfter=4
    )
    
    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=14,
        leading=19,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=14
    )
    
    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=12.5,
        leading=17,
        textColor=colors.black,
        spaceBefore=10,
        spaceAfter=5
    )
    
    body_style = ParagraphStyle(
        'BodyJustified',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11.5,
        leading=17.5,
        alignment=4,
        textColor=colors.black,
        spaceAfter=12
    )
    
    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11.5,
        leading=17,
        alignment=4,
        textColor=colors.black,
        leftIndent=24,
        firstLineIndent=-14,
        spaceAfter=8
    )
    
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Times-Bold',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.black,
        spaceBefore=6,
        spaceAfter=6
    )
    
    subcaption_style = ParagraphStyle(
        'SubCaptionStyle',
        parent=styles['Normal'],
        fontName='Times-Italic',
        fontSize=8.5,
        leading=12,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceBefore=4,
        spaceAfter=12
    )
    
    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=16.5,
        alignment=4,
        leftIndent=28,
        firstLineIndent=-28,
        textColor=colors.black,
        spaceAfter=14
    )

    story = []
    
    # ==================== PAGE 1: TITLE PAGE ====================
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>SYNOPSIS</b>", t_center_bold_lg))
    story.append(Paragraph("<b>ON</b>", t_center_bold_md))
    story.append(Paragraph("<b>&ldquo;AI-POWERED STUDENT STUDY PLANNER AND SMART TIMETABLE GENERATION SYSTEM&rdquo;</b>", t_center_bold_lg))
    
    story.append(Spacer(1, 16))
    story.append(Paragraph("Submitted in", t_center_regular))
    story.append(Paragraph("Partial Fulfillment of the requirements for the Award of the Degree", t_center_italic))
    story.append(Paragraph("<i>of</i>", t_center_italic))
    story.append(Paragraph("<b>Bachelor of Technology</b>", t_center_regular))
    story.append(Paragraph("<i>In</i>", t_center_italic))
    story.append(Paragraph("<b>Computer Science and Engineering</b>", t_center_regular))
    story.append(Paragraph("<i>by</i>", t_center_italic))
    
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Student Name: Shresthi Kesharwani</b>", t_center_regular))
    story.append(Paragraph("<b>Roll No.: 2501641520196</b>", t_center_regular))
    
    story.append(Spacer(1, 14))
    story.append(Paragraph("Under the supervision of", t_center_regular))
    story.append(Paragraph("<b>Supervisor Name: Mr. Rajesh Kumar</b>", t_center_regular))
    story.append(Paragraph("(Assistant Professor)", t_center_regular))
    
    story.append(Spacer(1, 16))
    if os.path.exists("psit_logo.png"):
        story.append(Image("psit_logo.png", width=1.9*72, height=0.75*72))
    story.append(Spacer(1, 12))
    story.append(Paragraph("<b>Pranveer Singh Institute of Technology.</b>", t_center_bold_md))
    story.append(Paragraph("Kanpur - Agra - Delhi National Highway - 19", t_center_regular))
    story.append(Paragraph("Bhauti - Kanpur - 209305.", t_center_regular))
    
    story.append(PageBreak())
    
    # ==================== PAGE 2: INTRODUCTION ====================
    story.append(Paragraph("<b>1. Introduction</b>", h1_style))
    story.append(Paragraph(
        "In today's rigorous academic environment, engineering and undergraduate students are confronted with extensive curricula, multiple simultaneous subjects, practical assessments, and strict examination deadlines. Effective time management is essential for academic excellence; however, a large majority of students struggle with procrastination, cognitive overload, unbalanced preparation, and severe last-minute exam anxiety. Traditional manual planning methods—such as handwritten schedules, static paper timetables, or generic spreadsheet logs—are notoriously rigid and fail to adapt when real-world delays occur, resulting in abandoned study routines and poor academic performance.",
        body_style
    ))
    story.append(Paragraph(
        "Conventional productivity tools and calendar applications merely record static task reminders without assessing workload urgency, topic difficulty, or cognitive fatigue. When a student falls behind on a particular topic, manual rescheduling requires tedious effort, often leading to total breakdown of the revision plan. Intelligent algorithmic scheduling bridges this gap by continuously evaluating examination proximity, remaining syllabus volume, and available daily study hours, automatically redistributing topics so that high-priority academic commitments receive proportional focus without overwhelming the learner.",
        body_style
    ))
    story.append(Paragraph(
        "This project proposes an AI-Powered Student Study Planner and Smart Timetable Generation System that automatically calculates optimal, personalized daily study timetables. The application models academic subjects, syllabus topics, estimated learning durations, and target examination dates. Employing an adaptive urgency-calculation algorithm combined with Pomodoro-style interval optimization (structured 45-minute focus blocks paired with 15-minute restorative breaks), the system allocates daily sessions proportionally. Students can track completion in real time via an interactive web dashboard with progress analytics and live countdowns.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Special terms:</b> Adaptive Scheduling &ndash; dynamic algorithmic reallocation of study slots based on ongoing progress; Urgency Score &ndash; a quantified priority index calculated from exam proximity and unfinished topic volume; Pomodoro Interval &ndash; a structured session technique balancing focused cognitive sprints with rest intervals; Workload Estimation &ndash; metric measuring syllabus scope in required learning hours; Relational Persistence &ndash; structured database storage tracking topics, subjects, and parameters.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==================== PAGE 3: PROJECT OBJECTIVE ====================
    story.append(Paragraph("<b>2. Project Objective</b>", h1_style))
    story.append(Paragraph(
        "The primary objective of this project is to design, develop, and deploy an intelligent, automated, and easy-to-use study planning and timetable generation platform that dynamically calculates personalized study routines, prioritizes subjects by urgency, and tracks curriculum progress in real time. The specific objectives are:",
        body_style
    ))
    
    objectives = [
        "To formulate and implement a dynamic priority algorithm that computes subject urgency scores based on days remaining until examinations and total uncompleted topic hours.",
        "To automate multi-day study timetable generation by intelligently distributing available daily study hours into structured focus sessions and restorative break intervals.",
        "To build an interactive and responsive web dashboard displaying overall completion percentages, subject-wise progress bars, and live examination countdowns.",
        "To provide seamless curriculum management allowing students to add, edit, and organize subjects with custom color tags, specific topics, and estimated learning hours.",
        "To implement real-time asynchronous topic completion tracking using AJAX and an SQLite relational database backend for frictionless user interaction.",
        "To empower learners with customizable study settings, including adjustable daily study hours, session lengths, preferred daily start hours, and break durations."
    ]
    
    for obj in objectives:
        story.append(Paragraph(f"&bull; &nbsp; {obj}", bullet_style))
        
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "At the completion of the project, students and competitive exam aspirants will have an accessible, automated, and scientifically structured tool that eliminates the stress of manual planning, mitigates exam panic, and fosters disciplined, spaced learning habits for superior academic achievement.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==================== PAGE 4: FEASIBILITY STUDY ====================
    story.append(Paragraph("<b>3. Feasibility Study</b>", h1_style))
    story.append(Paragraph(
        "A comprehensive feasibility study was conducted to evaluate whether the proposed study planner system can be successfully developed and deployed within the constraints of available resources, technical expertise, and semester deadlines. The project was assessed across five key dimensions:",
        body_style
    ))
    
    feas_points = [
        ("Technical Feasibility: ", "The system utilizes proven, open-source, and industry-standard technologies including Python, the Flask micro-framework, SQLite, and vanilla HTML5/CSS3/JavaScript. The priority scheduling algorithm requires minimal computational overhead and runs effortlessly on standard student laptops or lightweight local servers without requiring dedicated GPUs. The development team has the requisite programming proficiency in full-stack Python development, making the project technically feasible."),
        ("Operational Feasibility: ", "The platform features a clean, responsive card-based user interface that requires zero specialized onboarding. Students simply input their subjects, topics, and exam dates, and the application instantly outputs an actionable daily schedule. Because it seamlessly complements the existing revision routines of university students, operational adoption is straightforward and highly feasible."),
        ("Economic Feasibility: ", "All frameworks, libraries, runtime environments, and development tools (Flask, SQLite, VS Code, Git) are entirely open-source and free of licensing costs. No expensive external cloud APIs or proprietary third-party software are necessary, keeping overall development and hosting expenditures virtually zero. The project is therefore economically optimal for an academic project."),
        ("Schedule Feasibility: ", "The project lifecycle is divided systematically into requirement analysis, relational schema design, algorithm implementation, frontend UI assembly, testing, and documentation. All phases have been mapped to realistic milestones and can be completed well within the designated semester timeframe."),
        ("Legal Feasibility: ", "The application operates exclusively on student-entered academic details and stores information locally within an embedded SQLite database. No personal biometric or sensitive financial data is collected or distributed, ensuring strict compliance with IT ethics and data privacy norms.")
    ]
    
    for title, desc in feas_points:
        story.append(Paragraph(f"<b>{title}</b>{desc}", body_style))
    
    story.append(PageBreak())
    
    # ==================== PAGE 5: METHODOLOGY / PLANNING OF WORK ====================
    story.append(Paragraph("<b>4. Methodology / Planning of Work</b>", h1_style))
    story.append(Paragraph(
        "The project follows a structured engineering methodology from conceptualization to deployment, organized into sequential development phases:",
        body_style
    ))
    
    steps = [
        "<b>Requirement analysis:</b> investigate student revision workflows, time management bottlenecks, cognitive learning theories (spaced repetition and Pomodoro focus blocks), and feature requirements.",
        "<b>Database modeling:</b> architect a relational SQLite schema comprising subjects, hierarchical topics with completion timestamps, and global user study parameters.",
        "<b>Algorithmic formulation:</b> design the urgency calculation model that evaluates remaining hours against exam deadlines and allocates proportional daily session blocks.",
        "<b>Backend routing:</b> implement Flask application routes, database connection pooling, request validation, and RESTful asynchronous topic toggle handlers.",
        "<b>Frontend interface:</b> develop a modern, aesthetically polished UI with semantic HTML5, responsive CSS3 styling, subject color-coding, progress gauges, and multi-day timetable cards.",
        "<b>Testing & validation:</b> execute rigorous unit and boundary testing (exam on same day, zero remaining topics, overlapping subject deadlines) to verify scheduling accuracy.",
        "<b>Deployment & reporting:</b> package the application for seamless local execution, configure cloud hosting parameters, and compile complete technical documentation."
    ]
    
    for s in steps:
        story.append(Paragraph(f"&bull; &nbsp; {s}", bullet_style))
        
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "The complete architecture and flow of information between the modules is illustrated in the system architecture diagram below.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ==================== PAGE 6: ARCHITECTURE & TOOLS ====================
    story.append(Paragraph("<b>Fig. 1: System Architecture of the Proposed Study Planner &amp; Timetable System</b>", caption_style))
    
    if os.path.exists("study_planner_architecture.png"):
        story.append(Image("study_planner_architecture.png", width=6.6*72, height=2.6*72))
    
    story.append(Paragraph("<i>Core scheduling pipeline: Subject &amp; Topic Data &rarr; Urgency Calculation &rarr; Session Fitting &rarr; Daily Timetable &rarr; Progress Tracking</i>", subcaption_style))
    
    story.append(Paragraph("<b>5. Tools / Technology Used</b>", h1_style))
    story.append(Paragraph("<b>5.1 Minimum Hardware Requirements</b>", h2_style))
    story.append(Paragraph("Hardware required for the development and execution of the project.", body_style))
    
    hw_items = [
        "CPU: Intel Core i3 / i5 (8th Gen or higher) or AMD Ryzen 3 / 5, 2.0 GHz or above",
        "RAM: 4 GB (8 GB recommended for seamless multitasking and local server execution)",
        "GPU: Not required; standard integrated graphics are sufficient",
        "HDD/SSD: 128 GB SSD or 500 GB HDD with at least 5 GB free storage space",
        "Others (if any): Standard keyboard, mouse, and display monitor (1366x768 resolution or higher)"
    ]
    for item in hw_items:
        story.append(Paragraph(f"&bull; &nbsp; {item}", bullet_style))
        
    story.append(Paragraph("<b>5.2 Minimum Software Requirements</b>", h2_style))
    story.append(Paragraph("Software required for the development and execution of the project.", body_style))
    
    sw_items = [
        "OS: Windows 10/11 (64-bit) or Ubuntu Linux 22.04 LTS",
        "Programming languages: Python 3.10 or above; HTML5, CSS3, and JavaScript (ES6+)",
        "Libraries and frameworks: Flask (v3.0+), Jinja2 template engine, Werkzeug, SQLite3",
        "Database: SQLite relational database for local persistence of study records",
        "Other tools: Visual Studio Code, Git and GitHub, Modern Web Browser (Google Chrome / Firefox / Edge)"
    ]
    for item in sw_items:
        story.append(Paragraph(f"&bull; &nbsp; {item}", bullet_style))
        
    story.append(PageBreak())
    
    # ==================== PAGE 7: REFERENCES ====================
    story.append(Paragraph("<b>6. References</b>", h1_style))
    story.append(Spacer(1, 6))
    
    refs = [
        "[1] H. C. Ellis, \u201cThe role of cognitive load and retrieval practice in academic study schedules,\u201d <i>Journal of Educational Psychology</i>, vol. 112, no. 4, pp. 780\u2013795, 2020.",
        "[2] F. Cirillo, <i>The Pomodoro Technique: The Acclaimed Time-Management System That Has Transformed How We Work</i>, New York: Currency, 2018.",
        "[3] M. Grissom and D. C. Baber, \u201cAlgorithmic approaches to automated academic scheduling and deadline management,\u201d <i>IEEE Transactions on Learning Technologies</i>, vol. 14, no. 3, pp. 312\u2013324, 2021.",
        "[4] M. Grinberg, <i>Flask Web Development: Developing Web Applications with Python</i>, 2nd ed., Sebastopol, CA: O\u2019Reilly Media, 2018.",
        "[5] A. Dunlosky, K. A. Rawson, E. J. Marsh, M. J. Nathan, and D. T. Willingham, \u201cImproving students\u2019 learning with effective learning techniques: Promising directions from cognitive and educational psychology,\u201d <i>Psychological Science in the Public Interest</i>, vol. 14, no. 1, pp. 4\u201358, 2013.",
        "[6] SQLite Development Team, \u201cSQLite: An In-Process Database for Autonomous and Embedded Systems.\u201d [Online]. Available: https://www.sqlite.org"
    ]
    
    for ref in refs:
        story.append(Paragraph(ref, ref_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated Study Planner PDF: {filename}")


def set_docx_page_border(section):
    sectPr = section._sectPr
    pgBorders = parse_xml(
        r'<w:pgBorders %s w:offsetFrom="page">'
        r'  <w:top w:val="single" w:sz="6" w:space="24" w:color="333333"/>'
        r'  <w:left w:val="single" w:sz="6" w:space="24" w:color="333333"/>'
        r'  <w:bottom w:val="single" w:sz="6" w:space="24" w:color="333333"/>'
        r'  <w:right w:val="single" w:sz="6" w:space="24" w:color="333333"/>'
        r'</w:pgBorders>' % nsdecls('w')
    )
    sectPr.append(pgBorders)

def build_docx(filename="AI_Study_Planner_Synopsis_Shresthi_Kesharwani.docx"):
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.9)
        section.right_margin = Inches(0.9)
        set_docx_page_border(section)

    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    
    # --- PAGE 1: COVER ---
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run("SYNOPSIS\nON\n")
    run.bold = True
    run.font.size = Pt(16)
    run2 = p.add_run("\u201cAI-POWERED STUDENT STUDY PLANNER AND SMART TIMETABLE GENERATION SYSTEM\u201d")
    run2.bold = True
    run2.font.size = Pt(15.5)

    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p2.paragraph_format.space_before = Pt(14)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.line_spacing = 1.3
    r = p2.add_run("Submitted in\n")
    r.font.size = Pt(12)
    r = p2.add_run("Partial Fulfillment of the requirements for the Award of the Degree\nof\n")
    r.italic = True
    r.font.size = Pt(12)
    r = p2.add_run("Bachelor of Technology\n")
    r.bold = True
    r.font.size = Pt(13)
    r = p2.add_run("In\n")
    r.italic = True
    r.font.size = Pt(12)
    r = p2.add_run("Computer Science and Engineering\n")
    r.bold = True
    r.font.size = Pt(13)
    r = p2.add_run("by\n")
    r.italic = True
    r.font.size = Pt(12)

    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(12)
    p3.paragraph_format.space_after = Pt(14)
    r = p3.add_run("Student Name: Shresthi Kesharwani\nRoll No.: 2501641520196")
    r.bold = True
    r.font.size = Pt(13)

    p4 = doc.add_paragraph()
    p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p4.paragraph_format.space_before = Pt(10)
    p4.paragraph_format.space_after = Pt(14)
    r = p4.add_run("Under the supervision of\n")
    r.font.size = Pt(12)
    r = p4.add_run("Supervisor Name: Mr. Rajesh Kumar\n")
    r.bold = True
    r.font.size = Pt(13)
    r = p4.add_run("(Assistant Professor)")
    r.font.size = Pt(12)

    if os.path.exists("psit_logo.png"):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(8)
        p_img.add_run().add_picture("psit_logo.png", width=Inches(1.9))

    p5 = doc.add_paragraph()
    p5.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p5.paragraph_format.space_before = Pt(6)
    p5.paragraph_format.space_after = Pt(4)
    r = p5.add_run("Pranveer Singh Institute of Technology.\n")
    r.bold = True
    r.font.size = Pt(14)
    r = p5.add_run("Kanpur - Agra - Delhi National Highway - 19\nBhauti - Kanpur - 209305.")
    r.font.size = Pt(12)

    doc.add_page_break()

    # --- PAGE 2: INTRODUCTION ---
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("1. Introduction")
    r.bold = True
    r.font.size = Pt(14)

    intro_paras = [
        "In today's rigorous academic environment, engineering and undergraduate students are confronted with extensive curricula, multiple simultaneous subjects, practical assessments, and strict examination deadlines. Effective time management is essential for academic excellence; however, a large majority of students struggle with procrastination, cognitive overload, unbalanced preparation, and severe last-minute exam anxiety. Traditional manual planning methods—such as handwritten schedules, static paper timetables, or generic spreadsheet logs—are notoriously rigid and fail to adapt when real-world delays occur, resulting in abandoned study routines and poor academic performance.",
        "Conventional productivity tools and calendar applications merely record static task reminders without assessing workload urgency, topic difficulty, or cognitive fatigue. When a student falls behind on a particular topic, manual rescheduling requires tedious effort, often leading to total breakdown of the revision plan. Intelligent algorithmic scheduling bridges this gap by continuously evaluating examination proximity, remaining syllabus volume, and available daily study hours, automatically redistributing topics so that high-priority academic commitments receive proportional focus without overwhelming the learner.",
        "This project proposes an AI-Powered Student Study Planner and Smart Timetable Generation System that automatically calculates optimal, personalized daily study timetables. The application models academic subjects, syllabus topics, estimated learning durations, and target examination dates. Employing an adaptive urgency-calculation algorithm combined with Pomodoro-style interval optimization (structured 45-minute focus blocks paired with 15-minute restorative breaks), the system allocates daily sessions proportionally. Students can track completion in real time via an interactive web dashboard with progress analytics and live countdowns.",
        "Special terms: Adaptive Scheduling \u2013 dynamic algorithmic reallocation of study slots based on ongoing progress; Urgency Score \u2013 a quantified priority index calculated from exam proximity and unfinished topic volume; Pomodoro Interval \u2013 a structured session technique balancing focused cognitive sprints with rest intervals; Workload Estimation \u2013 metric measuring syllabus scope in required learning hours; Relational Persistence \u2013 structured database storage tracking topics, subjects, and parameters."
    ]

    for text in intro_paras:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.25
        if text.startswith("Special terms:"):
            r_bold = p.add_run("Special terms: ")
            r_bold.bold = True
            p.add_run(text[len("Special terms: "):])
        else:
            p.add_run(text)

    doc.add_page_break()

    # --- PAGE 3: PROJECT OBJECTIVE ---
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("2. Project Objective")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.25
    p.add_run("The primary objective of this project is to design, develop, and deploy an intelligent, automated, and easy-to-use study planning and timetable generation platform that dynamically calculates personalized study routines, prioritizes subjects by urgency, and tracks curriculum progress in real time. The specific objectives are:")

    objectives = [
        "To formulate and implement a dynamic priority algorithm that computes subject urgency scores based on days remaining until examinations and total uncompleted topic hours.",
        "To automate multi-day study timetable generation by intelligently distributing available daily study hours into structured focus sessions and restorative break intervals.",
        "To build an interactive and responsive web dashboard displaying overall completion percentages, subject-wise progress bars, and live examination countdowns.",
        "To provide seamless curriculum management allowing students to add, edit, and organize subjects with custom color tags, specific topics, and estimated learning hours.",
        "To implement real-time asynchronous topic completion tracking using AJAX and an SQLite relational database backend for frictionless user interaction.",
        "To empower learners with customizable study settings, including adjustable daily study hours, session lengths, preferred daily start hours, and break durations."
    ]

    for obj in objectives:
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.2
        p.add_run(obj)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.25
    p.add_run("At the completion of the project, students and competitive exam aspirants will have an accessible, automated, and scientifically structured tool that eliminates the stress of manual planning, mitigates exam panic, and fosters disciplined, spaced learning habits for superior academic achievement.")

    doc.add_page_break()

    # --- PAGE 4: FEASIBILITY STUDY ---
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("3. Feasibility Study")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.25
    p.add_run("A comprehensive feasibility study was conducted to evaluate whether the proposed study planner system can be successfully developed and deployed within the constraints of available resources, technical expertise, and semester deadlines. The project was assessed across five key dimensions:")

    feas_points = [
        ("Technical Feasibility: ", "The system utilizes proven, open-source, and industry-standard technologies including Python, the Flask micro-framework, SQLite, and vanilla HTML5/CSS3/JavaScript. The priority scheduling algorithm requires minimal computational overhead and runs effortlessly on standard student laptops or lightweight local servers without requiring dedicated GPUs. The development team has the requisite programming proficiency in full-stack Python development, making the project technically feasible."),
        ("Operational Feasibility: ", "The platform features a clean, responsive card-based user interface that requires zero specialized onboarding. Students simply input their subjects, topics, and exam dates, and the application instantly outputs an actionable daily schedule. Because it seamlessly complements the existing revision routines of university students, operational adoption is straightforward and highly feasible."),
        ("Economic Feasibility: ", "All frameworks, libraries, runtime environments, and development tools (Flask, SQLite, VS Code, Git) are entirely open-source and free of licensing costs. No expensive external cloud APIs or proprietary third-party software are necessary, keeping overall development and hosting expenditures virtually zero. The project is therefore economically optimal for an academic project."),
        ("Schedule Feasibility: ", "The project lifecycle is divided systematically into requirement analysis, relational schema design, algorithm implementation, frontend UI assembly, testing, and documentation. All phases have been mapped to realistic milestones and can be completed well within the designated semester timeframe."),
        ("Legal Feasibility: ", "The application operates exclusively on student-entered academic details and stores information locally within an embedded SQLite database. No personal biometric or sensitive financial data is collected or distributed, ensuring strict compliance with IT ethics and data privacy norms.")
    ]

    for title, desc in feas_points:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.25
        r_title = p.add_run(title)
        r_title.bold = True
        p.add_run(desc)

    doc.add_page_break()

    # --- PAGE 5: METHODOLOGY / PLANNING OF WORK ---
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(12)
    r = p.add_run("4. Methodology / Planning of Work")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.line_spacing = 1.25
    p.add_run("The project follows a structured engineering methodology from conceptualization to deployment, organized into sequential development phases:")

    method_steps = [
        ("Requirement analysis: ", "investigate student revision workflows, time management bottlenecks, cognitive learning theories (spaced repetition and Pomodoro focus blocks), and feature requirements."),
        ("Database modeling: ", "architect a relational SQLite schema comprising subjects, hierarchical topics with completion timestamps, and global user study parameters."),
        ("Algorithmic formulation: ", "design the urgency calculation model that evaluates remaining hours against exam deadlines and allocates proportional daily session blocks."),
        ("Backend routing: ", "implement Flask application routes, database connection pooling, request validation, and RESTful asynchronous topic toggle handlers."),
        ("Frontend interface: ", "develop a modern, aesthetically polished UI with semantic HTML5, responsive CSS3 styling, subject color-coding, progress gauges, and multi-day timetable cards."),
        ("Testing & validation: ", "execute rigorous unit and boundary testing (exam on same day, zero remaining topics, overlapping subject deadlines) to verify scheduling accuracy."),
        ("Deployment & reporting: ", "package the application for seamless local execution, configure cloud hosting parameters, and compile complete technical documentation.")
    ]

    for title, desc in method_steps:
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.line_spacing = 1.2
        r = p.add_run(title)
        r.bold = True
        p.add_run(desc)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.line_spacing = 1.25
    p.add_run("The complete architecture and flow of information between the modules is illustrated in the system architecture diagram below.")

    doc.add_page_break()

    # --- PAGE 6: ARCHITECTURE DIAGRAM & TOOLS ---
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Fig. 1: System Architecture of the Proposed Study Planner & Timetable System")
    r.bold = True
    r.font.size = Pt(11)

    if os.path.exists("study_planner_architecture.png"):
        p_diag = doc.add_paragraph()
        p_diag.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_diag.paragraph_format.space_after = Pt(4)
        p_diag.add_run().add_picture("study_planner_architecture.png", width=Inches(6.2))

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(14)
    r = p_sub.add_run("Core scheduling pipeline: Subject & Topic Data \u2192 Urgency Calculation \u2192 Session Fitting \u2192 Daily Timetable \u2192 Progress Tracking")
    r.italic = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(80, 80, 80)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run("5. Tools / Technology Used")
    r.bold = True
    r.font.size = Pt(14)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("5.1 Minimum Hardware Requirements")
    r.bold = True
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Hardware required for the development and execution of the project.")

    hw_items = [
        "CPU: Intel Core i3 / i5 (8th Gen or higher) or AMD Ryzen 3 / 5, 2.0 GHz or above",
        "RAM: 4 GB (8 GB recommended for seamless multitasking and local server execution)",
        "GPU: Not required; standard integrated graphics are sufficient",
        "HDD/SSD: 128 GB SSD or 500 GB HDD with at least 5 GB free storage space",
        "Others (if any): Standard keyboard, mouse, and display monitor (1366x768 resolution or higher)"
    ]
    for item in hw_items:
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(item)

    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("5.2 Minimum Software Requirements")
    r.bold = True
    r.font.size = Pt(12)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.add_run("Software required for the development and execution of the project.")

    sw_items = [
        "OS: Windows 10/11 (64-bit) or Ubuntu Linux 22.04 LTS",
        "Programming languages: Python 3.10 or above; HTML5, CSS3, and JavaScript (ES6+)",
        "Libraries and frameworks: Flask (v3.0+), Jinja2 template engine, Werkzeug, SQLite3",
        "Database: SQLite relational database for local persistence of study records",
        "Other tools: Visual Studio Code, Git and GitHub, Modern Web Browser (Google Chrome / Firefox / Edge)"
    ]
    for item in sw_items:
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(item)

    doc.add_page_break()

    # --- PAGE 7: REFERENCES ---
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(14)
    r = p.add_run("6. References")
    r.bold = True
    r.font.size = Pt(14)

    refs_data = [
        ("[1] ", "H. C. Ellis, \u201cThe role of cognitive load and retrieval practice in academic study schedules,\u201d ", "Journal of Educational Psychology", ", vol. 112, no. 4, pp. 780\u2013795, 2020."),
        ("[2] ", "F. Cirillo, ", "The Pomodoro Technique: The Acclaimed Time-Management System That Has Transformed How We Work", ", New York: Currency, 2018."),
        ("[3] ", "M. Grissom and D. C. Baber, \u201cAlgorithmic approaches to automated academic scheduling and deadline management,\u201d ", "IEEE Transactions on Learning Technologies", ", vol. 14, no. 3, pp. 312\u2013324, 2021."),
        ("[4] ", "M. Grinberg, ", "Flask Web Development: Developing Web Applications with Python", ", 2nd ed., Sebastopol, CA: O\u2019Reilly Media, 2018."),
        ("[5] ", "A. Dunlosky, K. A. Rawson, E. J. Marsh, M. J. Nathan, and D. T. Willingham, \u201cImproving students\u2019 learning with effective learning techniques: Promising directions from cognitive and educational psychology,\u201d ", "Psychological Science in the Public Interest", ", vol. 14, no. 1, pp. 4\u201358, 2013."),
        ("[6] ", "SQLite Development Team, \u201cSQLite: An In-Process Database for Autonomous and Embedded Systems.\u201d [Online]. Available: https://www.sqlite.org", "", "")
    ]

    for num, text_pre, italic_text, text_post in refs_data:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(12)
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.left_indent = Inches(0.4)
        p.paragraph_format.first_line_indent = Inches(-0.4)
        p.add_run(num)
        p.add_run(text_pre)
        if italic_text:
            r_it = p.add_run(italic_text)
            r_it.italic = True
        if text_post:
            p.add_run(text_post)

    doc.save(filename)
    print(f"Successfully generated Study Planner DOCX: {filename}")

if __name__ == "__main__":
    build_pdf()
    build_docx()
