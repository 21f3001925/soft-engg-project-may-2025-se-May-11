import os
import google.generativeai as genai

# Configure the Gemini API
try:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    model = None


def analyze_report(text: str) -> str:
    """Analyzes a report using the Gemini API to provide a summary and suggestions."""
    if not model:
        return "Error: Gemini API is not configured."

    prompt = f"""
    You are an expert medical report analyst. Your task is to analyze the following report and provide a clear, readable summary and helpful, non-prescriptive suggestions for a senior citizen. Use simple, everyday language suitable for someone without a medical background. Avoid jargon and keep sentences short.

    **Report Text:**
    {text}

    **Instructions:**
    1.  **Summary:** Provide a brief, easy-to-understand summary of the report's main findings.
    2.  **What This Means:** In a separate section, explain the key findings in simple terms. For example, if a value is high, explain what that might generally indicate.
    3.  **Key Information:** List the most important points (e.g., test results, measurements) as bullet points.
    4.  **Suggestions:** Based on the findings, provide 2-3 general suggestions. These should be safe, non-medical recommendations (e.g., 'Consider discussing these results with your doctor', 'You might want to track your daily blood pressure', 'Maintaining a balanced diet could be beneficial').
    5.  **Disclaimer:** End with the statement: 'Disclaimer: This is an AI-generated analysis and not a substitute for professional medical advice. Please consult your doctor.'

    **Output Format:**
    ### Summary
    [Your summary here]

    ### What This Means
    [Your simple explanation here]

    ### Key Information
    - [Point 1]
    - [Point 2]

    ### Suggestions
    - [Suggestion 1]
    - [Suggestion 2]

    ### Disclaimer
    [Your disclaimer here]
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return f"Error analyzing report: {e}"


def chat_with_report(report_text: str, user_question: str) -> str:
    """Answers a user's question based on the text of a report."""
    if not model:
        return "Error: Gemini API is not configured."

    try:
        # Start a chat session with the report text as context
        chat = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        f"You are a helpful chat assistant. Your task is to answer my questions based *only* on the content of the provided medical report. Do not, under any circumstances, provide information, opinions, or medical advice that is not explicitly stated in the report.\n\n**Full Report Text:**\n{report_text}"
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Okay, I understand. I will only use the provided report to answer your questions."
                    ],
                },
            ]
        )

        response = chat.send_message(user_question)
        return response.text
    except Exception as e:
        print(f"Error calling Gemini API for chat: {e}")
        return f"Error: {e}"
