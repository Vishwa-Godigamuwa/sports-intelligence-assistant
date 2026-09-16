from utils.pdf_generator import generate_pdf

report_data = {
    "Sport": "Cricket",
    "Feature": "Batting Improvement",
    "Question": "How can I improve my cover drive?",
    "Player Level": "Beginner",
    "Strengths": "Interested in technique",
    "Weaknesses": "Footwork, Timing",
    "Training Plan": "Practice 3 times per week",
    "Expected Progress": "4-6 weeks",
    "Recommendations": "Focus on balance and foot movement"
}

pdf_file = generate_pdf(report_data)

print(f"PDF Generated: {pdf_file}")