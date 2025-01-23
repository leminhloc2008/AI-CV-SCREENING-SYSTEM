from app.modules.document_extraction.extractor import extract_resume
from app.modules.summarization.summarizer import summarize_resume

def test_cv_summarization():
    cv_file = "D:\Downloads\LeMinhLocCV.pdf"  

    resume = extract_resume(cv_file)

    summary = summarize_resume(resume)

    # Print the summary
    print("=== CV Summary ===")
    print(summary)

test_cv_summarization()