from question_generator import Generator
from uuid import uuid4, UUID
import requests
import json
from tqdm import tqdm

# Create a generator object
generator = Generator("college_board")

# Add a question to the database from College Board
asmtEventId = [99, 100, 102]

# Math test is not yet implemented
# tests = [1, 2]
tests = [1]
reading_domains = ["INI", "CAS", "EOI", "SEC"]
math_domains = ["H", "P", "Q", "S"]

# College Board API constants
overview_bank = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-questions"
question_bank = "https://qbank-api.collegeboard.org/msreportingquestionbank-prod/questionbank/digital/get-question"

# test 1 is reading, test 2 is math
for test in tests:
    domains = reading_domains if test == 1 else math_domains
    print(f"Currently Populating Subject: {"Reading" if test == 1 else "Math"}")

    for domain in domains:
        print(f"\tCurrently Populating domain: {domain}")

        for eventId in asmtEventId:
            content = {"asmtEventId": eventId, "test": test, "domain": domain}
            overview_list = requests.post(overview_bank, json=content)
            print(f"\tCurrently Populating test: {eventId}")
            count = 0
            length = len(json.loads(overview_list.text))

            for overview in tqdm(json.loads(overview_list.text)):
                problem = {"external_id": overview["external_id"]}
                question_raw = requests.post(question_bank, json=problem)
                question = json.loads(question_raw.text)
                # Add the question to the database
                generator.add_question("college_board", overview, question)

                # Tracking progress
                print(f"{count * 100 // length}%: {count} out of {length}")
                count += 1