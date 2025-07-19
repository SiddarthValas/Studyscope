from backend.search_engine import get_answer_from_notes

subject = "oop"

print("📚 OOP StudyScope Search")
while True:
    question = input("❓ Ask a question (or type 'exit'): ")
    if question.lower() == "exit":
        break

    answer = get_answer_from_notes(question, subject)
    if answer:
        print("🔎 Most Relevant Answer:")
        print(answer)
    else:
        print("❌ No confident match found in your notes.")
