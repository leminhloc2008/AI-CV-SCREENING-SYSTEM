from app.modules.document_extraction.extractor import extract_resume
from app.modules.summarization.evaluator import evaluate_resume

def test_cv_evaluation():
    cv_file = "D:\Downloads\LeMinhLocCV.pdf"  

    # Extract structured data from the CV
    resume = extract_resume(cv_file)

    # Evaluate the CV using an LLM
    evaluation = evaluate_resume(resume)

    # Print the evaluation
    print("=== CV Evaluation ===")
    print(evaluation)

test_cv_evaluation()