# --- quiz_generator.py ---
from transformers import pipeline
import random
import re

# Load FLAN-T5 model pipeline
quiz_model = pipeline("text2text-generation", model="google/flan-t5-base")

def parse_quiz_output(text):
    """
    Parses model output into structured quiz format.
    Returns (question, options, answer_letter) or None if parsing fails.
    """
    try:
        # Normalize
        text = text.replace("\n", " ").strip()

        # Extract parts using regex
        q_match = re.search(r"Question:\s*(.*?)\s*Options:", text)
        opts_match = re.search(r"Options:\s*(.*?)\s*Answer:", text)
        ans_match = re.search(r"Answer:\s*([A-D])", text)

        if not (q_match and opts_match and ans_match):
            return None

        question = q_match.group(1).strip()
        options_block = opts_match.group(1).strip()
        answer_letter = ans_match.group(1).strip().upper()

        # Extract all options A) ... D)
        options = []
        for prefix in ["A)", "B)", "C)", "D)"]:
            match = re.search(f"{re.escape(prefix)}\s*(.*?)(?=\s*[A-D]\)|$)", options_block)
            if match:
                options.append(match.group(1).strip())

        if len(options) == 4 and answer_letter in ["A", "B", "C", "D"]:
            return question, options, answer_letter
    except Exception as e:
        print(f"⚠️ Parsing failed: {e}")
    return None

def generate_quiz_from_notes(chunks, num_questions=5):
    selected = random.sample(chunks, min(num_questions, len(chunks)))
    quiz = []

    for text in selected:
        if len(text.strip()) < 50:
            continue  # skip too-short notes

        prompt = f"""Generate a multiple choice question from this note:
{text}

Format:
Question: <question>
Options: A) <option1> B) <option2> C) <option3> D) <option4>
Answer: <correct_option_letter>"""

        try:
            result = quiz_model(prompt, max_new_tokens=150, do_sample=False)[0]['generated_text'].strip()
            parsed = parse_quiz_output(result)

            if parsed:
                question, options, answer = parsed
                quiz.append({
                    "question": question,
                    "options": options,
                    "answer": answer
                })
            else:
                print("⚠️ Skipped due to bad format:", result)

        except Exception as e:
            print(f"⚠️ Quiz generation error: {e}")
            continue

    return quiz
