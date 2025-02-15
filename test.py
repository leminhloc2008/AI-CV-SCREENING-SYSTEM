import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime

# Update imports to use absolute imports
from app.modules.document_extraction.extractor import extract_resume
from app.modules.scoring.scorer import calculate_total_score
from app.modules.summarization.summarizer import summarize_resume
from app.modules.summarization.evaluator import evaluate_resume
from app.modules.scoring.education import calculate_education_score
from app.modules.scoring.experience import calculate_experience_score
from app.modules.scoring.projects import calculate_projects_score
from app.modules.scoring.awards import calculate_awards_score
from app.modules.scoring.certifications import calculate_certifications_score

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('cv_processing.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_cv(file_path: str) -> Dict[str, Any]:
    """
    Process a single CV file and return evaluation results.
    
    Args:
        file_path (str): Path to the CV file
        
    Returns:
        Dict[str, Any]: Dictionary containing evaluation results
    """
    try:
        logger.info(f"Processing CV: {os.path.basename(file_path)}")
        
        # Extract structured data from CV
        resume = extract_resume(file_path)
        
        # Calculate scores
        scoring_result = calculate_total_score(resume)
        detailed_scores = {
            "education": calculate_education_score(resume.education),
            "experience": calculate_experience_score(resume.professional_experience),
            "projects": calculate_projects_score(resume.projects),
            "awards": calculate_awards_score(resume.awards),
            "certifications": calculate_certifications_score(resume.certifications),
            "total_score": scoring_result["total_score"]
        }
        
        # Generate summary and evaluation
        summary = summarize_resume(resume)
        evaluation = evaluate_resume(resume)
        
        # Prepare results
        results = {
            "file_name": os.path.basename(file_path),
            "processed_at": datetime.now().isoformat(),
            "cv_data": resume.dict(),
            "scores": detailed_scores,
            "status": "Pass" if scoring_result["total_score"] >= 70 else "Fail",
            "ai_summary": summary,
            "ai_evaluation": evaluation
        }
        
        logger.info(f"Successfully processed {os.path.basename(file_path)}")
        return results
        
    except Exception as e:
        logger.error(f"Error processing {os.path.basename(file_path)}: {str(e)}")
        return {
            "file_name": os.path.basename(file_path),
            "processed_at": datetime.now().isoformat(),
            "error": str(e),
            "status": "Error"
        }

def process_directory(directory_path: str, output_dir: str) -> None:
    """
    Process all CV files in a directory and save results.
    
    Args:
        directory_path (str): Path to directory containing CVs
        output_dir (str): Path to directory for saving results
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files
    cv_files = list(Path(directory_path).glob("*.pdf"))
    
    if not cv_files:
        logger.warning(f"No PDF files found in {directory_path}")
        return
    
    logger.info(f"Found {len(cv_files)} PDF files to process")
    
    # Process each CV
    all_results = []
    for cv_file in cv_files:
        results = process_cv(str(cv_file))
        all_results.append(results)
        
        # Save individual result
        result_file = Path(output_dir) / f"{cv_file.stem}_result.json"
        save_json(results, str(result_file))
    
    # Save summary report
    summary_report = create_summary_report(all_results)
    save_json(summary_report, str(Path(output_dir) / "summary_report.json"))
    
def create_summary_report(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Create a summary report from all processed CVs.
    
    Args:
        results (List[Dict[str, Any]]): List of individual CV results
        
    Returns:
        Dict[str, Any]: Summary report
    """
    total_cvs = len(results)
    successful = len([r for r in results if r.get("status") != "Error"])
    passed = len([r for r in results if r.get("status") == "Pass"])
    
    # Calculate average scores for successful processes
    avg_scores = {
        "education": 0.0,
        "experience": 0.0,
        "projects": 0.0,
        "awards": 0.0,
        "certifications": 0.0,
        "total_score": 0.0
    }
    
    for result in results:
        if "scores" in result:
            for category, score in result["scores"].items():
                avg_scores[category] += score
    
    if successful > 0:
        avg_scores = {k: v/successful for k, v in avg_scores.items()}
    
    return {
        "processed_at": datetime.now().isoformat(),
        "total_cvs": total_cvs,
        "successful": successful,
        "failed": total_cvs - successful,
        "passed": passed,
        "failed_screening": successful - passed,
        "average_scores": avg_scores,
        "results": results
    }

def save_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data as JSON file.
    
    Args:
        data (Dict[str, Any]): Data to save
        file_path (str): Output file path
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"Saved results to {file_path}")
    except Exception as e:
        logger.error(f"Error saving results to {file_path}: {str(e)}")

def main():
    """
    Main function to run the CV processing system.
    """
    # Configuration
    INPUT_DIR = "cvs"  # Directory containing CVs
    OUTPUT_DIR = "results"  # Directory for results
    
    try:
        logger.info("Starting CV processing system")
        
        # Create directories if they don't exist
        Path(INPUT_DIR).mkdir(exist_ok=True)
        Path(OUTPUT_DIR).mkdir(exist_ok=True)
        
        # Process all CVs in the input directory
        process_directory(INPUT_DIR, OUTPUT_DIR)
        
        logger.info("CV processing completed")
        
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main()