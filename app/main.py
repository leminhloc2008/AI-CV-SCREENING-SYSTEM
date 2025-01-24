from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
from typing import Dict, Any

# Import existing functions
from modules.document_extraction.extractor import extract_resume
from modules.scoring.scorer import calculate_total_score
from modules.summarization.summarizer import summarize_resume
from modules.summarization.evaluator import evaluate_resume
from modules.scoring.education import calculate_education_score
from modules.scoring.experience import calculate_experience_score
from modules.scoring.projects import calculate_projects_score
from modules.scoring.awards import calculate_awards_score
from modules.scoring.certifications import calculate_certifications_score

app = FastAPI()

@app.post("/api/evaluate-cv")
async def evaluate_cv_endpoint(file: UploadFile = File(...)) -> JSONResponse:
    """
    API endpoint to evaluate a CV file and return structured results.
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_file_path = tmp_file.name

        try:
            # Use existing evaluate_cv function
            evaluation_info = evaluate_cv(tmp_file_path)
            
            if not evaluation_info:
                raise HTTPException(status_code=500, detail="Failed to process CV")
            
            return JSONResponse(content=evaluation_info)

        finally:
            # Clean up temp file
            if os.path.exists(tmp_file_path):
                os.unlink(tmp_file_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

# Keep existing utility functions
def get_cv_json_data(file_path: str) -> Dict[str, Any]:
    """Extract structured JSON data from a CV file."""
    try:
        resume = extract_resume(file_path)
        return resume.dict()
    except Exception as e:
        print(f"Error extracting CV data: {e}")
        return {}

def evaluate_cv(file_path: str) -> Dict[str, Any]:
    """Evaluate a CV and provide detailed evaluation information."""
    try:
        resume = extract_resume(file_path)
        scoring_result = calculate_total_score(resume)
        summary = summarize_resume(resume)
        evaluation = evaluate_resume(resume)
        
        return {
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
    except Exception as e:
        print(f"Error evaluating CV: {e}")
        return {}

def export_to_json(data: Dict[str, Any], output_file: str) -> None:
    """Export evaluation data to a JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Evaluation data exported to {output_file}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)