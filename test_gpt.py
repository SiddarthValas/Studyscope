from backend.gpt_helper import get_gpt_response

question = "What is Object Oriented Programming?"
answer = get_gpt_response(question)
print("🔍 Answer:", answer)
