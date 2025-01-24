import requests
import os
import json
from pathlib import Path

def test_cv_evaluation():
    # Use Path for cross-platform compatibility
    cv_path = Path(r"C:\Users\baolo\OneDrive - THPT Chuyên Lê Quý Đôn - Đà Nẵng\Desktop\AI-CV-SCREENING-SYSTEM\output_5.pdf")

    # Validate file
    if not cv_path.exists():
        print(f"Error: File not found at {cv_path}")
        return
    
    if not cv_path.suffix.lower() == '.pdf':
        print("Error: File must be PDF format")
        return

    url = "http://localhost:8000/api/evaluate-cv"
    
    try:
        # Open file in binary mode
        with open(cv_path, 'rb') as pdf_file:
            files = {
                "file": ("cv.pdf", pdf_file, "application/pdf")
            }
            
            print(f"Sending request to {url}...")
            response = requests.post(url, files=files)
            
            # Print detailed response info
            print(f"\nStatus Code: {response.status_code}")
            print(f"Response Headers: {response.headers}")
            
            if response.ok:
                result = response.json()
                print("\nSuccess! Response:")
                print(json.dumps(result, indent=2))
            else:
                print("\nError Response:")
                print(f"Status: {response.status_code}")
                print(f"Error: {response.text}")
                
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

if __name__ == "__main__":
    test_cv_evaluation()