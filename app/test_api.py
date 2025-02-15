import requests
import json
from pathlib import Path
import logging
import mimetypes
import time
from typing import Optional, Dict, Any
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class CVAPITester:
    def __init__(self, api_url: str = "http://localhost:8000/api/evaluate-cv"):
        self.api_url = api_url
        self.session = requests.Session()

    def validate_file(self, file_path: Path) -> bool:
        """
        Validate the CV file before sending.
        """
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return False

            if not file_path.suffix.lower() == '.pdf':
                logger.error(f"Invalid file format. Expected PDF, got: {file_path.suffix}")
                return False

            # Check file size (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if file_path.stat().st_size > max_size:
                logger.error(f"File too large: {file_path.stat().st_size / 1024 / 1024:.2f}MB (max 10MB)")
                return False

            # Check if file is readable
            try:
                with open(file_path, 'rb') as f:
                    f.read(1024)  # Try reading first 1KB
            except Exception as e:
                logger.error(f"File not readable: {str(e)}")
                return False

            return True

        except Exception as e:
            logger.error(f"File validation error: {str(e)}")
            return False

    def send_cv(self, file_path: Path, retries: int = 3, delay: int = 2) -> Optional[Dict[str, Any]]:
        """
        Send CV to API with retries and error handling.
        """
        if not self.validate_file(file_path):
            return None

        for attempt in range(retries):
            try:
                with open(file_path, 'rb') as pdf_file:
                    files = {
                        "file": (file_path.name, pdf_file, "application/pdf")
                    }
                    
                    logger.info(f"Sending request to {self.api_url}")
                    logger.info(f"Attempt {attempt + 1} of {retries}")
                    
                    response = self.session.post(self.api_url, files=files)
                    
                    # Log response info
                    logger.info(f"Status Code: {response.status_code}")
                    logger.info(f"Response Headers: {dict(response.headers)}")
                    
                    if response.ok:
                        result = response.json()
                        logger.info("Request successful!")
                        return result
                    else:
                        logger.error(f"Request failed: {response.status_code}")
                        logger.error(f"Error response: {response.text}")
                        
                        if response.status_code == 413:
                            logger.error("File too large for server")
                            break  # Don't retry if file is too large
                        elif attempt < retries - 1:
                            time.sleep(delay)  # Wait before retrying
                        else:
                            logger.error("Max retries reached")
                            
            except requests.exceptions.ConnectionError:
                logger.error(f"Connection error (attempt {attempt + 1})")
                if attempt < retries - 1:
                    time.sleep(delay)
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                if attempt < retries - 1:
                    time.sleep(delay)
                    
        return None

    def save_result(self, result: Dict[str, Any], output_dir: Path) -> None:
        """
        Save API response to JSON file.
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_file = output_dir / f"cv_result_{timestamp}.json"
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
                
            logger.info(f"Results saved to: {output_file}")
            
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")

def main():
    """
    Main function to test the CV evaluation API.
    """
    # Configuration
    api_url = "http://localhost:8000/api/evaluate-cv"
    output_dir = Path("results")
    
    if len(sys.argv) < 2:
        logger.error("Please provide the path to your CV file as an argument")
        logger.info("Usage: python test_api.py path/to/your/cv.pdf")
        sys.exit(1)
        
    cv_path = Path(sys.argv[1])
    
    try:
        # Initialize tester
        tester = CVAPITester(api_url)
        
        # Send CV and get results
        logger.info(f"Processing CV: {cv_path}")
        result = tester.send_cv(cv_path)
        
        if result:
            # Save results
            tester.save_result(result, output_dir)
            
            # Print key information
            print("\nCV Processing Results:")
            print("-" * 50)
            if "scores" in result:
                print("\nScores:")
                for category, score in result["scores"].items():
                    print(f"{category}: {score}")
                    
            if "ai_summary" in result:
                print("\nSummary:")
                print(result["ai_summary"])
            
            if "ai_evaluation" in result:
                print("\nEvaluation:")
                print(result["ai_evaluation"])
        else:
            logger.error("Failed to process CV")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()