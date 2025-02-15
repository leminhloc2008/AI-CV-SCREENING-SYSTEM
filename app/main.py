from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import json
from typing import Dict, Any
import logging
import sys
from dotenv import load_dotenv
import logging as logger
from datetime import datetime

# Update imports to use absolute imports from app root
from app.modules.document_extraction.extractor import extract_resume
from app.modules.scoring.scorer import calculate_total_score
from app.modules.summarization.summarizer import summarize_resume
from app.modules.summarization.evaluator import evaluate_resume
from app.modules.scoring.education import calculate_education_score
from app.modules.scoring.experience import calculate_experience_score
from app.modules.scoring.projects import calculate_projects_score
from app.modules.scoring.awards import calculate_awards_score
from app.modules.scoring.certifications import calculate_certifications_score

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/api/evaluate-cv")
async def evaluate_cv_endpoint(file: UploadFile = File(...)) -> JSONResponse:
    """
    Evaluate a CV file and return detailed analysis.
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extract CV data
            resume = extract_resume(temp_path)
            logger.info("Successfully extracted resume data")

            # Calculate scores
            score_result = calculate_total_score(resume)
            logger.info("Successfully calculated scores")

            # Generate reasoning based on the status
            ai_reason = evaluate_resume(resume, score_result["status"])

            # Prepare response
            result = {
                "file_name": file.filename,
                "processed_at": datetime.now().isoformat(),
                "cv_data": resume.dict(),
                "scores": score_result["scores"],
                "weighted_scores": score_result["weighted_scores"],
                "status": score_result["status"],
                "total_score": score_result["total_score"],
                "ai_reason": ai_reason
            }

            return JSONResponse(content=result)

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to process CV: {str(e)}")

        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Error removing temp file: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global exception handler for better error messages.
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )

# Keep existing utility functions
def get_cv_json_data(file_path: str) -> Dict[str, Any]:
    """Extract structured JSON data from a CV file."""
    try:
        resume, _ = extract_resume(file_path)
        return resume.dict()
    except Exception as e:
        print(f"Error extracting CV data: {e}")
        return {}
    

'''def evaluate_cv(file_path: str) -> Dict[str, Any]:
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
        return {}'''

def export_to_json(data: Dict[str, Any], output_file: str) -> None:
    """Export evaluation data to a JSON file."""
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        # print(f"Evaluation data exported to {output_file}")
    except Exception as e:
        print(f"Error exporting to JSON: {e}")

'''
@app.post("/api/evaluate-cv")
async def evaluate_cv(file: UploadFile = File(...)) -> JSONResponse:
    """
    Evaluate a CV file and return detailed analysis.
    """
    try:
        # Validate file
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="File must be a PDF")

        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name

        try:
            # Extract CV data
            resume = extract_resume(temp_path)
            logger.info("Successfully extracted resume data")

            # Calculate scores
            score_result = calculate_total_score(resume)
            logger.info("Successfully calculated scores")

            # Generate summary and evaluation
            summary = summarize_resume(resume)
            evaluation = evaluate_resume(resume)
            logger.info("Successfully generated summary and evaluation")

            # Prepare response
            result = {
                "file_name": file.filename,
                "processed_at": datetime.now().isoformat(),
                "cv_data": resume.dict(),
                "scores": score_result["scores"],
                "weighted_scores": score_result["weighted_scores"],
                "status": score_result["status"],
                "total_score": score_result["total_score"],
                "ai_summary": summary,
                "ai_evaluation": evaluation
            }

            return JSONResponse(content=result)

        except Exception as e:
            logger.error(f"Processing error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to process CV: {str(e)}")

        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Error removing temp file: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Global exception handler for better error messages.
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )'''

if __name__ == "__main__":
    import uvicorn
    # Run directly from this file
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)