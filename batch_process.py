import json
import logging
from pathlib import Path
import concurrent.futures
from app.test_api import CVAPITester

# Configure logging for both file & console output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("batch_process.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def process_file(file_path: Path, tester: CVAPITester, output_dir: Path):
    logger.info(f"Processing CV: {file_path}")
    result = tester.send_cv(file_path)
    if result:
        tester.save_result(result, output_dir)
        logger.info(f"Successfully processed and saved result for {file_path.name}")
    else:
        logger.error(f"Failed to process CV: {file_path}")
    return result

def main():
    # Define input and output directories (using raw strings for Windows paths)
    input_dir = r"C:\Users\Admin\Documents\AI-CV-SCREENING-SYSTEM\cvs"
    output_dir = Path(r"C:\Users\Admin\Documents\AI-CV-SCREENING-SYSTEM\results")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Get up to 10 PDF files from the input directory
    cv_files = list(Path(input_dir).glob("*.pdf"))[:10]
    
    if not cv_files:
        logger.error(f"No PDF files found in {input_dir}")
        return
    
    logger.info(f"Found {len(cv_files)} CV files to process.")
    
    # Initialize the API tester (replace URL if needed)
    tester = CVAPITester(api_url="http://localhost:8000/api/evaluate-cv")
    
    # Process files concurrently using a thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {
            executor.submit(process_file, file, tester, output_dir): file
            for file in cv_files
        }
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Exception processing {file}: {e}")
    
    logger.info("Batch processing complete.")

if __name__ == "__main__":
    main() 