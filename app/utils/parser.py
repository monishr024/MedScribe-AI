import json


class ResponseParser:

    REQUIRED_FIELDS = [

        "patient_summary",

        "clinical_summary",

        "chief_complaint",

        "history_present_illness",

        "clinical_assessment",

        "differential_diagnosis",

        "recommended_lab_tests",

        "recommended_imaging",

        "red_flags",

        "treatment_considerations",

        "follow_up"

    ]

    @staticmethod
    def parse(response: str):

        try:

            cleaned = (

                response

                .replace("```json", "")

                .replace("```", "")

                .strip()

            )

            data = json.loads(cleaned)

            # =====================================================
            # Validate Required Fields
            # =====================================================

            missing = [

                field

                for field in ResponseParser.REQUIRED_FIELDS

                if field not in data

            ]

            if missing:

                raise Exception(

                    f"Missing required fields: {missing}"

                )

            # =====================================================
            # Ensure patient_summary keys exist
            # =====================================================

            summary = data.get("patient_summary", {})

            summary.setdefault("chief_problem", "")

            summary.setdefault("severity", "Low")

            summary.setdefault("generated_on", "")

            data["patient_summary"] = summary

            # =====================================================
            # Ensure arrays exist
            # =====================================================

            data.setdefault("differential_diagnosis", [])

            data.setdefault("recommended_lab_tests", [])

            data.setdefault("recommended_imaging", [])

            data.setdefault("red_flags", [])

            data.setdefault("treatment_considerations", [])

            # =====================================================
            # Ensure strings exist
            # =====================================================

            data.setdefault("clinical_summary", "")

            data.setdefault("chief_complaint", "")

            data.setdefault("history_present_illness", "")

            data.setdefault("clinical_assessment", "")

            data.setdefault("follow_up", "")

            return data

        except json.JSONDecodeError as e:

            raise Exception(

                f"Invalid JSON returned by Gemini.\n\n{e}"

            )

        except Exception as e:

            raise Exception(

                f"Response Parsing Error:\n\n{e}"

            )