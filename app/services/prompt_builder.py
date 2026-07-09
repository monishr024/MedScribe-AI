import json


class PromptBuilder:

    @staticmethod
    def build(patient_data: dict) -> str:

        patient_json = json.dumps(patient_data, indent=4)

        return f"""
You are an experienced Internal Medicine Physician and Clinical Documentation Specialist.

Analyze the following patient information and generate a professional clinical report.

PATIENT DATA

{patient_json}

==========================================================

Return ONLY valid JSON.

Do NOT return markdown.

Do NOT return explanations.

Do NOT wrap the response inside ```json.

The JSON MUST exactly match the following schema.

{{
    "patient_summary": {{
        "chief_problem": "",
        "severity": "",
        "generated_on": ""
    }},

    "clinical_summary": "",

    "chief_complaint": "",

    "history_present_illness": "",

    "clinical_assessment": "",

    "differential_diagnosis": [
        {{
            "condition": "",
            "likelihood": "",
            "reason": ""
        }}
    ],

    "recommended_lab_tests": [
        {{
            "test": "",
            "reason": ""
        }}
    ],

    "recommended_imaging": [
        {{
            "scan": "",
            "reason": ""
        }}
    ],

    "red_flags": [
        {{
            "finding": "",
            "severity": ""
        }}
    ],

    "treatment_considerations": [
        ""
    ],

    "follow_up": ""
}}

==========================================================
INSTRUCTIONS
==========================================================

1. PATIENT SUMMARY

Return:

- chief_problem
- severity
- generated_on

chief_problem:
Maximum 5 words.

Examples:
- Acute Respiratory Infection
- Viral Febrile Illness
- Community Acquired Pneumonia

severity must ONLY be one of:

Low
Moderate
High
Critical

generated_on MUST be an empty string.

==========================================================

2. CLINICAL SUMMARY

Write a professional clinical summary.

Include:

- Age
- Gender
- Chief complaint
- Duration (if available)
- Important vital signs
- General examination
- Overall clinical impression

Maximum one paragraph.

==========================================================

3. CHIEF COMPLAINT

Rewrite the user's chief complaint in proper clinical language.

Maximum two sentences.

Do NOT simply copy the user's wording.

==========================================================

4. HISTORY OF PRESENT ILLNESS

Rewrite the history into a chronological medical narrative.

Use professional clinical terminology.

Do not invent symptoms.

Maximum one paragraph.

==========================================================

5. CLINICAL ASSESSMENT

Provide a detailed assessment.

Discuss:

- Clinical interpretation
- Correlation with examination findings
- Possible diagnosis
- Supporting evidence
- Limitations
- Suggested investigations

Maximum three paragraphs.

==========================================================

6. DIFFERENTIAL DIAGNOSIS

Return EXACTLY three diagnoses.

Each diagnosis MUST contain:

condition

likelihood

reason

==========================================================

7. RECOMMENDED LABORATORY TESTS

Each item MUST contain:

test

reason

Return at least three tests whenever appropriate.

==========================================================

8.Recommended Imaging

Based on the patient's presentation, determine whether imaging would help establish or confirm the diagnosis.

If imaging is clinically useful, recommend ONE or TWO studies.

Examples:

• Chest X-ray
• CT Chest
• Abdominal Ultrasound
• CT Abdomen
• MRI Brain
• ECG (if appropriate for the context, though note ECG is not imaging)

Each recommendation must include:

- scan
- reason

Only return an empty array if there is absolutely no clinical justification for imaging.

==========================================================

9. Red Flags

Identify important warning signs based on the patient's symptoms, vital signs, and examination findings.

Examples include:

• High fever
• Hypoxia
• Severe hypotension
• Altered mental status
• Respiratory distress
• Persistent tachycardia
• Neurological deficits
• Severe abdominal tenderness

Return ONE to THREE red flags whenever clinically appropriate.

Each item must contain:

- finding
- severity

Only return an empty array if there are truly no concerning findings.

==========================================================

10. TREATMENT CONSIDERATIONS

Provide general clinical management considerations.

Do NOT prescribe medications.

==========================================================

11. FOLLOW-UP

Provide an appropriate follow-up recommendation.

==========================================================

12. IMPORTANT

Never invent symptoms.

Never invent examination findings.

Base every conclusion ONLY on the supplied information.

Return ONLY valid JSON.

No markdown.

No explanations.

No extra text.

IMPORTANT

Do not leave arrays empty unless clinically appropriate.

Whenever sufficient patient information exists, populate:

- differential_diagnosis
- recommended_lab_tests
- recommended_imaging
- red_flags

Provide clinically meaningful recommendations based solely on the supplied information.

Avoid returning empty arrays unnecessarily.

IMPORTANT:

Return ONLY valid JSON.

Use EXACTLY these keys.

patient_summary
clinical_summary
chief_complaint
history_present_illness
clinical_assessment
differential_diagnosis
recommended_lab_tests
recommended_imaging
red_flags
treatment_considerations
follow_up

Do NOT rename any key.
Do NOT use synonyms like "clinical_complaint".
"""