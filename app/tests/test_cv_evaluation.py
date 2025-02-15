from app.modules.document_extraction.extractor import extract_resume
from app.modules.summarization.evaluator import evaluate_resume
from app.modules.summarization.evaluator import calculate_total_score

def test_cv_evaluation():
    cv_file = "D:\Downloads\LeMinhLocCV.pdf"  

    # Extract structured data from the CV
    resume = extract_resume(cv_file)
    score_result = calculate_total_score(resume)
    ai_reason = evaluate_resume(resume, score_result["status"])

    # Print the evaluation
    print("=== CV Evaluation ===")
    print(f"Status: {score_result['status']}")
    print(f"Reason: {ai_reason}")

test_cv_evaluation()