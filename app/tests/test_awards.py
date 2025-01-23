from app.models.resume import AwardItem
from app.modules.scoring.awards import calculate_awards_score

def test_calculate_awards_score():
    awards = [
        AwardItem(contest="International Coding Competition", prize="1st Place", description="Developed an AI model using Python.", role="Lead Developer", link="https://example.com", time="2023"),
        AwardItem(contest="Local Hackathon", prize="2nd Place", description="Built a web app using React.", role="Frontend Developer", link=None, time="2022")
    ]
    score = calculate_awards_score(awards)

    # Output the awards score
    print("=== Awards Score ===")
    print(f"Score: {score}")

test_calculate_awards_score()