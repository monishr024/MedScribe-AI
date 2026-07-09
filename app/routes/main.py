from flask import Blueprint, render_template, request, session, send_file
import json

from app.services.pdf_generator import PDFGenerator
from datetime import datetime, date

from app.services.prompt_builder import PromptBuilder
from app.services.ai_service import AIService
from app.utils.parser import ResponseParser

main_bp = Blueprint("main", __name__)


# ==========================================================
# Calculate Age from DOB
# ==========================================================

def calculate_age(dob):

    if not dob:
        return ""

    dob = datetime.strptime(dob, "%Y-%m-%d").date()

    today = date.today()

    age = today.year - dob.year

    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1

    return age


# ==========================================================
# Home
# ==========================================================

@main_bp.route("/")
def home():

    return render_template("index.html")


# ==========================================================
# Analysis
# ==========================================================

@main_bp.route("/analysis")
def analysis():

    return render_template("analysis.html")


# ==========================================================
# Generate Report
# ==========================================================

@main_bp.route("/generate-report", methods=["POST"])
def generate_report():

    # ======================================================
    # Collect Patient Data
    # ======================================================

    dob = request.form.get("dob")

    patient_data = {

        "patient_information": {

            "name": request.form.get("patient_name"),

            "dob": dob,

            "age": calculate_age(dob),

            "gender": request.form.get("gender"),

            "height": request.form.get("height"),

            "weight": request.form.get("weight")

        },

        "chief_complaint":

            request.form.get("chief_complaint"),

        "history_present_illness":

            request.form.get("present_illness"),

        "vital_signs": {

            "temperature_f":

                request.form.get("temperature"),

            "blood_pressure":

                request.form.get("blood_pressure"),

            "heart_rate":

                request.form.get("heart_rate"),

            "respiratory_rate":

                request.form.get("resp_rate"),

            "spo2":

                request.form.get("spo2"),

            "blood_glucose":

                request.form.get("blood_glucose")

        },

        "general_physical_exam": {

            "general_appearance":

                request.form.get("general_appearance"),

            "pallor":

                request.form.get("pallor"),

            "icterus":

                request.form.get("icterus"),

            "cyanosis":

                request.form.get("cyanosis"),

            "clubbing":

                request.form.get("clubbing"),

            "edema":

                request.form.get("edema")

        },

        "systemic_exam": {

            "heart_sounds":

                request.form.get("heart_sounds"),

            "cvs_findings":

                request.form.get("cvs_findings"),

            "breath_sounds":

                request.form.get("breath_sounds"),

            "resp_findings":

                request.form.get("resp_findings"),

            "abdomen_exam":

                request.form.get("abdomen_exam"),

            "abdomen_findings":

                request.form.get("abdomen_findings"),

            "consciousness":

                request.form.get("consciousness"),

            "cns_findings":

                request.form.get("cns_findings")

        }

    }

    # ======================================================
    # Build Prompt
    # ======================================================

    prompt = PromptBuilder.build(patient_data)

    ai = AIService()

    # ======================================================
    # Generate Report using Gemini
    # ======================================================

    try:

        response = ai.generate_report(prompt)

    except Exception as e:

        return render_template(

            "report.html",

            patient=patient_data,

            report=None,

            error=str(e),

            now=datetime.now()

        )

    # ======================================================
    # Parse Gemini Response
    # ======================================================

    try:
        report = ResponseParser.parse(response)

        print("=" * 80)
        print("PARSED REPORT")
        print(report)
        print("=" * 80)



    except Exception as e:

        return render_template(

            "report.html",

            patient=patient_data,

            report=None,

            error=f"Parser Error: {str(e)}",

            raw_response=response,

            now=datetime.now()

        )

    # ======================================================
    # Success
    # ======================================================

    # ======================================================
# Store Data for PDF Download
# ======================================================

    session["patient"] = json.dumps(patient_data)

    session["report"] = json.dumps(report)
    
    return render_template(

        "report.html",

        patient=patient_data,

        report=report,

        error=None,

        now=datetime.now()

    )

# ==========================================================
# Download PDF
# ==========================================================

@main_bp.route("/download-pdf")
def download_pdf():

    patient_json = session.get("patient")
    report_json = session.get("report")

    if not patient_json or not report_json:

        return "Please generate a clinical report first.", 400

    patient = json.loads(patient_json)
    report = json.loads(report_json)

    pdf = PDFGenerator.create_pdf(patient, report)

    return send_file(

        pdf,

        mimetype="application/pdf",

        as_attachment=True,

        download_name="MedScribe_AI_Clinical_Report.pdf"

    )