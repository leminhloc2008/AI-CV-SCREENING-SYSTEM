
---

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key (for GPT-4 integration)
- Required Python libraries (see `requirements.txt`)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ai-cv-screening.git
   cd ai-cv-screening
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Create a `.env` file in the root directory.
   - Add your OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

---

## Usage

### Extract CV Data
To extract structured JSON data from a CV:
```python
from main import get_cv_json_data

cv_file_path = "path/to/your/cv.pdf"
cv_data = get_cv_json_data(cv_file_path)
print(cv_data)
```

### Evaluate CV
To evaluate a CV and get detailed evaluation information:
```python
from main import evaluate_cv

cv_file_path = "path/to/your/cv.pdf"
evaluation_info = evaluate_cv(cv_file_path)
print(evaluation_info)
```

### Export to JSON
To export evaluation results to a JSON file:
```python
from main import evaluate_cv, export_to_json

cv_file_path = "path/to/your/cv.pdf"
evaluation_info = evaluate_cv(cv_file_path)
export_to_json(evaluation_info, "evaluation_results.json")
```

### Run the API server
To run the API server:
```python
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
---


## Configuration

### JSON Lookup Files
- **`data/universities.json`**: Contains university rankings and reputation scores.
- **`data/companies.json`**: Contains company size categories and reputation scores.
- **`data/technical_terms.json`**: Contains technical keywords for semantic analysis.

### Scoring Rules
- Scoring rules and weights are defined in `models/scoring_rules.py`.
- You can modify the weights to align with your organization's hiring criteria.

---

## Testing

To run unit tests:
- First add your pdf cv into the root folder
- Then change the path of the cv in test_api.py
- After that run 
```bash
cd app
python test_api.py
```
