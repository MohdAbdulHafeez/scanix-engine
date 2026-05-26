def detect_risks(
    text: str,
):

    text = text.lower()

    risks = []

    if "salt" in text:

        risks.append(

            "High sodium"

        )

    if "sugar" in text:

        risks.append(

            "Sugar exposure"

        )

    if "oil" in text:

        risks.append(

            "Processed oil"

        )

    return risks