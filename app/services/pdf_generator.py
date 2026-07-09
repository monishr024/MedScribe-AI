from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    HRFlowable,
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


class PDFGenerator:

    @staticmethod
    def create_pdf(patient, report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=(8.27 * inch, 11.69 * inch),   # A4
            leftMargin=35,
            rightMargin=35,
            topMargin=35,
            bottomMargin=35
        )

        styles = getSampleStyleSheet()

        title_style = styles["Heading1"]
        title_style.alignment = TA_CENTER
        title_style.textColor = colors.HexColor("#0F766E")
        title_style.spaceAfter = 15

        heading_style = styles["Heading2"]
        heading_style.textColor = colors.HexColor("#0F766E")
        heading_style.spaceBefore = 15
        heading_style.spaceAfter = 10

        sub_heading = styles["Heading3"]
        sub_heading.textColor = colors.HexColor("#2563EB")

        body = styles["BodyText"]
        body.leading = 18
        body.spaceAfter = 10

        subtitle_style = styles["Heading2"]

        subtitle_style.alignment = TA_CENTER

        subtitle_style.textColor = colors.HexColor("#475569")

        subtitle_style.spaceAfter = 6

        subtitle_style.fontName = "Helvetica"

        story = []

       # ====================================================
# HEADER
# ====================================================

        story.append(
            Paragraph(
                "<font color='#0F766E'><b>MEDSCRIBE AI</b></font>",
                title_style
            )
        )

        story.append(
            Paragraph(
                "AI-Powered Clinical Assessment Report",
                subtitle_style
            )
        )

        story.append(
            Paragraph(
                "<font color='#64748B'><b>Generated On:</b> "
                + datetime.now().strftime("%d %B %Y  %I:%M %p")
                + "</font>",
                body
            )
        )

        story.append(Spacer(1,0.12*inch))

        story.append(

            HRFlowable(

                width="100%",

                thickness=2,

                color=colors.HexColor("#14B8A6"),

                spaceBefore=6,

                spaceAfter=14

            )

        )

        # ====================================================
        # PATIENT INFORMATION
        # ====================================================

        PDFGenerator.add_patient_information(
            story,
            patient,
            heading_style
        )

        # ====================================================
        # AI SUMMARY
        # ====================================================

        PDFGenerator.add_ai_summary(
            story,
            report,
            heading_style
        )

        # ====================================================
        # Remaining sections
        # ====================================================

        PDFGenerator.add_chief_complaint(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_history(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_vitals(
            story,
            patient,
            heading_style
        )

        PDFGenerator.add_general_exam(
            story,
            patient,
            heading_style
        )

        PDFGenerator.add_systemic_exam(
            story,
            patient,
            heading_style
        )

        PDFGenerator.add_assessment(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_differential(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_lab_tests(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_imaging(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_red_flags(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_treatment(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_followup(
            story,
            report,
            heading_style,
            body
        )

        PDFGenerator.add_disclaimer(
            story,
            body
        )

        doc.build( story,
        onFirstPage=PDFGenerator.footer,
        onLaterPages=PDFGenerator.footer)

        buffer.seek(0)

        return buffer

    # ====================================================
    # Helper
    # ====================================================

    @staticmethod
    def section_title(story, title, style):

        story.append(
            Paragraph(
                f"<b>{title}</b>",
                style
            )
        )

    @staticmethod
    def bullet(story, text, style):

        story.append(
            Paragraph(
                f"• {text}",
                style
            )
        )

       

    # ====================================================
# PATIENT INFORMATION
# ====================================================

    @staticmethod
    def add_patient_information(story, patient, heading_style):

        PDFGenerator.section_title(
            story,
            "Patient Demographics",
            heading_style
        )

        p = patient["patient_information"]

        left = f"""
        <b>Name</b><br/>
        {p["name"]}<br/><br/>

        <b>Age</b><br/>
        {p["age"]} Years<br/><br/>

        <b>Gender</b><br/>
        {p["gender"]}
        """

        right = f"""
        <b>Date of Birth</b><br/>
        {p["dob"]}<br/><br/>

        <b>Height</b><br/>
        {p["height"]} cm<br/><br/>

        <b>Weight</b><br/>
        {p["weight"]} kg
        """

        styles = getSampleStyleSheet()

        cell = styles["BodyText"]

        cell.leading = 20

        data = [[

            Paragraph(left, cell),

            Paragraph(right, cell)

        ]]

        table = Table(

            data,

            colWidths=[3.2*inch,3.2*inch]

        )

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F8FAFC")),

            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#CBD5E1")),

            ("INNERGRID",(0,0),(-1,-1),0.25,colors.white),

            ("BOTTOMPADDING",(0,0),(-1,-1),15),

            ("TOPPADDING",(0,0),(-1,-1),15),

            ("LEFTPADDING",(0,0),(-1,-1),18),

            ("RIGHTPADDING",(0,0),(-1,-1),18),

            ("VALIGN",(0,0),(-1,-1),"TOP")

        ]))

        story.append(table)

        story.append(Spacer(1,0.25*inch))
# ====================================================
# AI SUMMARY
# ====================================================

    @staticmethod
    def add_ai_summary(story, report, heading_style):

        PDFGenerator.section_title(
            story,
            "AI Clinical Summary",
            heading_style
        )

        summary = [

            ["Chief Problem",
            report["patient_summary"]["chief_problem"]],

            ["Severity",
            report["patient_summary"]["severity"]],

            ["Generated On",
            datetime.now().strftime("%d %B %Y")]

        ]

        table = Table(
            summary,
            colWidths=[2.2 * inch, 4.0 * inch]
        )

        table.setStyle(TableStyle([

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#DBEAFE")),

            ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#1D4ED8")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8)

        ]))

        story.append(table)

        story.append(Spacer(1, 0.25 * inch))

    # ====================================================
# CHIEF COMPLAINT
# ====================================================

    @staticmethod
    def add_chief_complaint(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Chief Complaint",
            heading_style
        )

        story.append(

            Paragraph(

                report["chief_complaint"],

                body

            )

        )

        story.append(Spacer(1,0.20*inch))


    # ====================================================
    # HISTORY OF PRESENT ILLNESS
    # ====================================================

    @staticmethod
    def add_history(story, report, heading_style, body):

        PDFGenerator.section_title(

            story,

            "History of Present Illness",

            heading_style

        )

        story.append(

            Paragraph(

                report["history_present_illness"],

                body

            )

        )

        story.append(Spacer(1,0.25*inch))


    # ====================================================
    # VITAL SIGNS
    # ====================================================

    @staticmethod
    def add_vitals(story, patient, heading_style):

        PDFGenerator.section_title(

            story,

            "Vital Signs",

            heading_style

        )

        vitals = [

            ["Temperature",
            f'{patient["vital_signs"]["temperature_f"]} °F'],

            ["Blood Pressure",
            patient["vital_signs"]["blood_pressure"]],

            ["Heart Rate",
            f'{patient["vital_signs"]["heart_rate"]} bpm'],

            ["Respiratory Rate",
            f'{patient["vital_signs"]["respiratory_rate"]} /min'],

            ["SpO₂",
            f'{patient["vital_signs"]["spo2"]} %'],

            ["Blood Glucose",
            f'{patient["vital_signs"]["blood_glucose"]} mg/dL']

        ]

        table = Table(

            vitals,

            colWidths=[2.4*inch,3.8*inch]

        )

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#FEF3C7")),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#92400E")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ]))

        story.append(table)

        story.append(Spacer(1,0.25*inch))

        # ====================================================
    # GENERAL PHYSICAL EXAMINATION
    # ====================================================

    @staticmethod
    def add_general_exam(story, patient, heading_style):

        PDFGenerator.section_title(
            story,
            "General Physical Examination",
            heading_style
        )

        exam = [

            ["General Appearance",
            patient["general_physical_exam"]["general_appearance"]],

            ["Pallor",
            patient["general_physical_exam"]["pallor"]],

            ["Icterus",
            patient["general_physical_exam"]["icterus"]],

            ["Cyanosis",
            patient["general_physical_exam"]["cyanosis"]],

            ["Clubbing",
            patient["general_physical_exam"]["clubbing"]],

            ["Edema",
            patient["general_physical_exam"]["edema"]]

        ]

        table = Table(
            exam,
            colWidths=[2.5*inch,3.7*inch]
        )

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#DCFCE7")),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#166534")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ]))

        story.append(table)

        story.append(Spacer(1,0.25*inch))


    # ====================================================
    # SYSTEMIC EXAMINATION
    # ====================================================

    @staticmethod
    def add_systemic_exam(story, patient, heading_style):

        PDFGenerator.section_title(
            story,
            "Systemic Examination",
            heading_style
        )

        systemic = [

            ["Heart Sounds",
            patient["systemic_exam"]["heart_sounds"]],

            ["CVS Findings",
            patient["systemic_exam"]["cvs_findings"]],

            ["Breath Sounds",
            patient["systemic_exam"]["breath_sounds"]],

            ["Respiratory Findings",
            patient["systemic_exam"]["resp_findings"]],

            ["Abdomen Examination",
            patient["systemic_exam"]["abdomen_exam"]],

            ["Abdomen Findings",
            patient["systemic_exam"]["abdomen_findings"]],

            ["Consciousness",
            patient["systemic_exam"]["consciousness"]],

            ["CNS Findings",
            patient["systemic_exam"]["cns_findings"]]

        ]

        table = Table(
            systemic,
            colWidths=[2.5*inch,3.7*inch]
        )

        table.setStyle(TableStyle([

            ("GRID",(0,0),(-1,-1),0.5,colors.grey),

            ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#E0F2FE")),

            ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#0369A1")),

            ("FONTNAME",(0,0),(-1,-1),"Helvetica"),

            ("BOTTOMPADDING",(0,0),(-1,-1),8),

            ("TOPPADDING",(0,0),(-1,-1),8),

            ("VALIGN",(0,0),(-1,-1),"MIDDLE")

        ]))

        story.append(table)

        story.append(Spacer(1,0.30*inch))

        # ====================================================
    # CLINICAL ASSESSMENT
    # ====================================================

    @staticmethod
    def add_assessment(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Clinical Assessment",
            heading_style
        )

        story.append(

            Paragraph(

                report["clinical_assessment"],

                body

            )

        )

        story.append(Spacer(1,0.30*inch))


    # ====================================================
    # DIFFERENTIAL DIAGNOSIS
    # ====================================================

        # ====================================================
    # DIFFERENTIAL DIAGNOSIS
    # ====================================================

    @staticmethod
    def add_differential(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Differential Diagnosis",
            heading_style
        )

        diagnoses = report.get("differential_diagnosis", [])

        if not diagnoses:

            story.append(
                Paragraph(
                    "No differential diagnoses generated.",
                    body
                )
            )

            story.append(Spacer(1, 0.20 * inch))
            return

        for diagnosis in diagnoses:

            condition = diagnosis.get("condition", "")
            likelihood = diagnosis.get("likelihood", "")
            reason = diagnosis.get("reason", "")

            card = [

                [
                    Paragraph(
                        f"<font color='#0F766E'><b>{condition}</b></font>",
                        body
                    )
                ],

                [
                    Paragraph(
                        f"<b>Likelihood:</b> {likelihood}",
                        body
                    )
                ],

                [
                    Paragraph(
                        reason,
                        body
                    )
                ]

            ]

            table = Table(
                card,
                colWidths=[6.3 * inch]
            )

            table.setStyle(TableStyle([

                ("BOX",(0,0),(-1,-1),1,colors.HexColor("#14B8A6")),

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F0FDFA")),

                ("BOTTOMPADDING",(0,0),(-1,-1),10),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("LEFTPADDING",(0,0),(-1,-1),15),

                ("RIGHTPADDING",(0,0),(-1,-1),15),

                ("VALIGN",(0,0),(-1,-1),"TOP")

            ]))

            story.append(table)

            story.append(Spacer(1,0.15*inch))

            # ====================================================
    # RECOMMENDED LABORATORY TESTS
    # ====================================================

    @staticmethod
    def add_lab_tests(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Recommended Laboratory Tests",
            heading_style
        )

        tests = report.get("recommended_lab_tests", [])

        if not tests:

            story.append(
                Paragraph(
                    "No laboratory investigations recommended.",
                    body
                )
            )

            story.append(Spacer(1,0.20*inch))
            return

        for test in tests:

            name = test.get("test", "")
            reason = test.get("reason", "")

            card = [

                [
                    Paragraph(
                        f"<font color='#0F766E'><b>🧪 {name}</b></font>",
                        body
                    )
                ],

                [
                    Paragraph(
                        f"<b>Clinical Reason</b><br/>{reason}",
                        body
                    )
                ]

            ]

            table = Table(
                card,
                colWidths=[6.3*inch]
            )

            table.setStyle(TableStyle([

                ("BOX",(0,0),(-1,-1),1,colors.HexColor("#14B8A6")),

                ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#ECFDF5")),

                ("BOTTOMPADDING",(0,0),(-1,-1),10),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("LEFTPADDING",(0,0),(-1,-1),15),

                ("RIGHTPADDING",(0,0),(-1,-1),15),

                ("VALIGN",(0,0),(-1,-1),"TOP")

            ]))

            story.append(table)

            story.append(Spacer(1,0.15*inch))


        # ====================================================
    # RECOMMENDED IMAGING
    # ====================================================

    @staticmethod
    def add_imaging(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Recommended Imaging",
            heading_style
        )

        imaging = report.get("recommended_imaging", [])

        if not imaging:

            table = Table(
                [[Paragraph(
                    "<font color='#1D4ED8'><b>ℹ No imaging studies are recommended based on the current clinical findings.</b></font>",
                    body
                )]],
                colWidths=[6.3 * inch]
            )

            table.setStyle(TableStyle([

                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#EFF6FF")),

                ("BOX",(0,0),(-1,-1),1,colors.HexColor("#60A5FA")),

                ("BOTTOMPADDING",(0,0),(-1,-1),12),

                ("TOPPADDING",(0,0),(-1,-1),12),

                ("LEFTPADDING",(0,0),(-1,-1),15)

            ]))

            story.append(table)

        else:

            for scan in imaging:

                card = [

                    [Paragraph(
                        f"<font color='#2563EB'><b>🩻 {scan['scan']}</b></font>",
                        body
                    )],

                    [Paragraph(
                        f"<b>Reason</b><br/>{scan['reason']}",
                        body
                    )]

                ]

                table = Table(
                    card,
                    colWidths=[6.3 * inch]
                )

                table.setStyle(TableStyle([

                    ("BOX",(0,0),(-1,-1),1,colors.HexColor("#3B82F6")),

                    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#EFF6FF")),

                    ("BOTTOMPADDING",(0,0),(-1,-1),10),

                    ("TOPPADDING",(0,0),(-1,-1),10),

                    ("LEFTPADDING",(0,0),(-1,-1),15)

                ]))

                story.append(table)

                story.append(Spacer(1,0.15*inch))

        story.append(Spacer(1,0.25*inch))
        # ====================================================
    # RED FLAGS
    # ====================================================

    @staticmethod
    def add_red_flags(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Clinical Red Flags",
            heading_style
        )

        flags = report.get("red_flags", [])

        if not flags:

            table = Table(
                [[Paragraph(
                    "<font color='#166534'><b>✓ No immediate clinical red flags identified.</b></font>",
                    body
                )]],
                colWidths=[6.3 * inch]
            )

            table.setStyle(TableStyle([

                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F0FDF4")),

                ("BOX",(0,0),(-1,-1),1,colors.HexColor("#22C55E")),

                ("BOTTOMPADDING",(0,0),(-1,-1),12),

                ("TOPPADDING",(0,0),(-1,-1),12),

                ("LEFTPADDING",(0,0),(-1,-1),15)

            ]))

            story.append(table)

        else:

            for flag in flags:

                card = [

                    [Paragraph(
                        f"<font color='red'><b>⚠ {flag['finding']}</b></font>",
                        body
                    )],

                    [Paragraph(
                        f"<b>Severity:</b> {flag['severity']}",
                        body
                    )]

                ]

                table = Table(
                    card,
                    colWidths=[6.3 * inch]
                )

                table.setStyle(TableStyle([

                    ("BOX",(0,0),(-1,-1),1,colors.red),

                    ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#FEF2F2")),

                    ("BOTTOMPADDING",(0,0),(-1,-1),10),

                    ("TOPPADDING",(0,0),(-1,-1),10),

                    ("LEFTPADDING",(0,0),(-1,-1),15)

                ]))

                story.append(table)

                story.append(Spacer(1,0.15*inch))

        story.append(Spacer(1,0.30*inch))

        # ====================================================
    # TREATMENT CONSIDERATIONS
    # ====================================================

    @staticmethod
    def add_treatment(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Treatment Considerations",
            heading_style
        )

        treatments = report.get("treatment_considerations", [])

        if not treatments:

            story.append(
                Paragraph(
                    "No treatment recommendations available.",
                    body
                )
            )

            story.append(Spacer(1,0.20*inch))
            return

        for item in treatments:

            table = Table(
                [[
                    Paragraph(
                        f"<font color='#166534'><b>✓</b></font> {item}",
                        body
                    )
                ]],
                colWidths=[6.3*inch]
            )

            table.setStyle(TableStyle([

                ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F0FDF4")),

                ("BOX",(0,0),(-1,-1),1,colors.HexColor("#22C55E")),

                ("BOTTOMPADDING",(0,0),(-1,-1),10),

                ("TOPPADDING",(0,0),(-1,-1),10),

                ("LEFTPADDING",(0,0),(-1,-1),15)

            ]))

            story.append(table)

            story.append(Spacer(1,0.12*inch))

        story.append(Spacer(1,0.25*inch))


        # ====================================================
    # FOLLOW-UP PLAN
    # ====================================================

    @staticmethod
    def add_followup(story, report, heading_style, body):

        PDFGenerator.section_title(
            story,
            "Follow-up Plan",
            heading_style
        )

        follow = report.get(
            "follow_up",
            "No follow-up recommendation available."
        )

        table = Table(
            [[Paragraph(follow, body)]],
            colWidths=[6.3*inch]
        )

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#FFFBEB")),

            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#F59E0B")),

            ("BOTTOMPADDING",(0,0),(-1,-1),12),

            ("TOPPADDING",(0,0),(-1,-1),12),

            ("LEFTPADDING",(0,0),(-1,-1),15)

        ]))

        story.append(table)

        story.append(Spacer(1,0.30*inch))

        # ====================================================
    # DISCLAIMER
    # ====================================================

    @staticmethod
    def add_disclaimer(story, body):

        story.append(Spacer(1,0.25*inch))

        table = Table([[
            Paragraph(
                "<b>Medical Disclaimer</b><br/><br/>"
                "This report has been generated using MedScribe AI based on "
                "the information provided by the user. It is intended solely "
                "to assist healthcare professionals in documentation and "
                "clinical decision support. It must not be used as a substitute "
                "for professional medical judgement, diagnosis, or treatment.",
                body
            )
        ]], colWidths=[6.3*inch])

        table.setStyle(TableStyle([

            ("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#F8FAFC")),

            ("BOX",(0,0),(-1,-1),1,colors.HexColor("#CBD5E1")),

            ("BOTTOMPADDING",(0,0),(-1,-1),14),

            ("TOPPADDING",(0,0),(-1,-1),14),

            ("LEFTPADDING",(0,0),(-1,-1),18),

            ("RIGHTPADDING",(0,0),(-1,-1),18)

        ]))

        story.append(table)

        story.append(Spacer(1,0.20*inch))

    @staticmethod
    def footer(canvas, doc):

        canvas.saveState()

        width = doc.pagesize[0]

        canvas.setStrokeColor(colors.HexColor("#CBD5E1"))

        canvas.line(
            35,
            35,
            width-35,
            35
        )

        canvas.setFont("Helvetica",8)

        canvas.setFillColor(colors.HexColor("#64748B"))

        canvas.drawString(
            35,
            20,
            "MedScribe AI | Confidential Clinical Report"
        )

        canvas.drawRightString(
            width-35,
            20,
            f"Page {canvas.getPageNumber()}"
        )

        canvas.restoreState()