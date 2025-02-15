# AI CV Screening System - Product Requirements Document

## Overview

### Purpose
The AI CV Screening System is designed to automate and enhance the CV screening process by leveraging artificial intelligence to evaluate candidates' qualifications, experience, and potential fit for technical positions.

### Objectives
- Automate CV data extraction and structured analysis
- Provide consistent and unbiased evaluation of candidates
- Reduce time spent on initial CV screening
- Generate detailed insights and recommendations
- Support the Vietnamese job market context

## System Architecture

### 1. Core Components

#### 1.1 Document Extraction Module
- Input: CV files (PDF/DOCX)
- Output: Structured Resume object
- Key Features:
  - OCR using GPT-4o or LLAMA-3
  - Structured data extraction
  - Vietnamese text handling
  - Document caching

#### 1.2 Scoring Framework
- Input: Resume object
- Output: Detailed scoring analysis
- Components:
  - Base scoring infrastructure
  - Individual scorer modules
  - Bias detection
  - Audit trail

#### 1.3 Knowledge Base
- Components:
  - University rankings database
  - Company information
  - Technical skills dictionary
  - Vietnam-specific context
  - Lookup mechanisms

#### 1.4 Embedding System
- Features:
  - PhoBERT integration
  - Semantic analysis
  - Error rate ≤1e-6
  - Async processing
  - Embedding caching

## Scoring System

### 1. Education (15% Weight)
Fields and Scoring Breakdown:
- School (30%)
  - Overseas: 30 points
  - International: 20 points
  - Public (Top): 20 points
  - Public (Others): 10 points

- Class Year (30%)
  - Senior: 30 points
  - Junior: 20 points
  - Sophomore: 10 points
  - Freshman: 10 points

- Major/Minor (30%)
  - Technical Major: 30 points
  - Non-technical Major: 0 points
  - Technical Minor (if major non-technical): 30 points

- GPA (10%)
  - ≥3.2: 10 points
  - 2.8-3.2: 5 points
  - <2.8: 0 points

### 2. Professional Experience (25% Weight)
Fields and Scoring Breakdown:
- Company (25%)
  - MNC/Established (1000+ employees): 25 points
  - Scale-up (101-500 employees): 20 points
  - Growth Startup (11-100 employees): 15 points
  - Early Startup (1-10 employees): 5 points

- Position (25%)
  - Technical Role: 25 points
  - Non-technical Role: 0 points

- Description (25%)
  - Clarity and Focus: 10 points
  - Achievements/Impact: 10 points
  - Use of Tools/Technologies: 5 points

- Location (5%)
  - Overseas/HCMC: 5 points
  - Other: 0 points

- Seniority (5%)
  - Full-time: 5 points
  - Internship: 0 points

- Duration (5%)
  - ≥6 months: 5 points
  - <6 months: 0 points

### 3. Projects (20% Weight)
Fields and Scoring Breakdown:
- Name (10%)
  - With Description: 10 points
  - Name Only: 5 points

- Link (20%)
  - GitHub/Live Project: 20 points
  - No Link: 0 points

- Tech Stack (25%)
  - ≥4 relevant technologies: 25 points
  - 2-3 relevant technologies: 15-20 points
  - 1 relevant technology: 5-10 points

- Duration (5%)
  - Listed: 5 points
  - Not Listed: 0 points

- Description (40%)
  - Role and Responsibilities: 20 points
  - Impact/Achievements: 15 points
  - Team Collaboration: 5 points

### 4. Awards (15% Weight)
Fields and Scoring Breakdown:
- Contest (30%)
  - International: 30 points
  - National: 20 points
  - Local: 10 points

- Prize (25%)
  - First Place/Gold: 25 points
  - Second Place/Silver: 20 points
  - Third Place/Bronze: 15 points
  - Participation: 10 points

- Description (25%)
  - Technical Details: 15 points
  - Impact/Achievement: 10 points

- Role (10%)
  - Technical Role: 10 points
  - Non-technical Role: 0 points

- Link/Time (10%)
  - Has Link: 5 points
  - Has Time: 5 points

### 5. Certifications (5% Weight)
Fields and Scoring Breakdown:
- Name (50%)
  - Well-known Technical Cert: 50 points
  - General Technical Cert: 30 points
  - Non-technical Cert: 10 points

- Organization (40%)
  - Major Tech Company: 40 points
  - Known Platform: 25 points
  - Others: 10 points

- Link (10%)
  - Has Link: 10 points
  - No Link: 0 points

### 6. Skills (5% Weight)
Fields and Scoring Breakdown:
- Technical Skills:
  - High Relevance: 50 points
  - Medium Relevance: 30 points
  - Low Relevance: 10 points

## Decision Making

### Final Score Calculation
Total Score = Sum of (Category Score × Category Weight)

### Status Assignment
- Pass: ≥70 points
- Consider: 50-69 points
- Fail: <50 points

## Technical Requirements

### 1. System Requirements
- Python 3.8 or higher
- FastAPI for REST API
- OpenAI API access
- GPU support (optional)

### 2. Performance Requirements
- Processing Time: <60 seconds per CV
- Concurrent Processing: 10+ CVs
- Availability: 99.9%
- Error Rate: <0.1%

### 3. Security Requirements
- Secure File Upload
- Data Encryption
- Access Control
- Audit Logging

## Integration

### 1. API Integration
- REST API endpoints
- Webhook support
- Rate limiting
- Error handling

### 2. Google Sheets Integration
- Auto-populate scores
- Generate PDF reports
- Highlight scoring rationale

## Testing & Validation

### 1. Test Cases
- Unit tests for each module
- Integration tests
- Performance tests
- Bias testing

### 2. Validation Metrics
- Accuracy: 90% alignment with human recruiters
- Consistency: 95% score match on re-evaluation
- Processing Speed: <60 seconds per CV

## Documentation

### 1. Technical Documentation
- API documentation
- System architecture
- Database schema
- Integration guide

### 2. User Documentation
- User manual
- Installation guide
- Troubleshooting guide
- FAQ

## Compliance

### 1. Legal Requirements
- PDPA compliance
- Data protection
- Privacy policy
- Terms of service

### 2. Ethical Requirements
- Bias mitigation
- Fairness in evaluation
- Transparency in scoring
- Appeal process