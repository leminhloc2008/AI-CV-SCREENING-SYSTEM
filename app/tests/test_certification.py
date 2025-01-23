from app.models.resume import CertificationItem
from app.modules.scoring.certifications import calculate_certifications_score

def test_calculate_certifications_score():
    certifications = [
        CertificationItem(name="AWS Certified Solutions Architect", org="Amazon Web Services", link="https://example.com"),
        CertificationItem(name="Google Data Engineer", org="Google", link=None)
    ]
    score = calculate_certifications_score(certifications)

    # Output the certifications score
    print("=== Certifications Score ===")
    print(f"Score: {score}")

# Run the test
test_calculate_certifications_score()