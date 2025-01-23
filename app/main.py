import json
from modules.document_extraction.extractor import extract_resume
from modules.scoring.scorer import calculate_total_score
from modules.summarization.summarizer import summarize_resume
from modules.summarization.evaluator import evaluate_resume
from modules.scoring.education import calculate_education_score
from modules.scoring.experience import calculate_experience_score
from modules.scoring.projects import calculate_projects_score
from modules.scoring.awards import calculate_awards_score
from modules.scoring.certifications import calculate_certifications_score
from typing import Dict, Any

def get_cv_json_data(file_path: str) -> Dict[str, Any]:
    """
    Extract structured JSON data from a CV file.
    """
    try:
        resume = extract_resume(file_path)
        return resume.dict()
    except Exception as e:
        print(f"Error extracting CV data: {e}")
        return {}

def evaluate_cv(file_path: str) -> Dict[str, Any]:
    """
    Evaluate a CV and provide detailed evaluation information.
    """
    try:
        resume = extract_resume(file_path)
        scoring_result = calculate_total_score(resume)
        summary = summarize_resume(resume)
        evaluation = evaluate_resume(resume)
        
        evaluation_result = {
            "cv_data": resume.dict(),
            "scores": {
                "education": calculate_education_score(resume.education),
                "experience": calculate_experience_score(resume.professional_experience),
                "projects": calculate_projects_score(resume.projects),
                "awards": calculate_awards_score(resume.awards),
                "certifications": calculate_certifications_score(resume.certifications),
                "total_score": scoring_result["total_score"],
                "status": scoring_result["status"]
            },
            "ai_summarization": summary,
            "ai_evaluation": evaluation
        }
        
        return evaluation_result
    except Exception as e:
        print(f"Error evaluating CV: {e}")
        return {}

def export_to_json(data: Dict[str, Any], output_file: str) -> None:
    """
    Export evaluation data to a JSON file.
    
    Args:
        data (dict): The evaluation data to export.
        output_file (str): The path to the output JSON file.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Evaluation data exported to {output_file}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

if __name__ == "__main__":
    cv_file_path = "D:\Downloads\LeMinhLocCV.pdf"
    
    cv_json_data = get_cv_json_data(cv_file_path)
    print("=== CV JSON Data ===")
    print(cv_json_data)
    
    evaluation_info = evaluate_cv(cv_file_path)
    print("\n=== CV Evaluation ===")
    print(evaluation_info)
    
    export_to_json(evaluation_info, "evaluation_results.json")