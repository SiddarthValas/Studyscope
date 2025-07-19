# gpt_helper.py

from transformers import pipeline

# Load the Flan-T5 base model from Hugging Face
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

def get_gpt_response(question):
    try:
        # Prompt engineering for better responses
        prompt = f"Answer this study question in detail and clearly:\n\n{question}"
        result = qa_pipeline(prompt, max_new_tokens=200, truncation=True)
        answer = result[0]['generated_text'].strip()
        return answer if answer else "⚠️ The model did not generate a response."
    except Exception as e:
        return f"❌ Hugging Face error: {str(e)}"
