from dotenv import load_dotenv
import os
from supabase import create_client, Client
import ast

# Creates a client to interact with the Supabase database
class Generator:

    '''
    Constructor for the Generator class
    :param source: The source of the questions
    '''
    def __init__(self, source: str):

        if source == 'college_board':
            load_dotenv()

            url: str = os.environ.get("SUPABASE_URL")
            key: str = os.environ.get("SUPABASE_KEY")

            self.supabase: Client = create_client(url, key)
        else:
            raise ValueError("Invalid source")
        
    def add_question(self, source : str, overview : dict, question : dict):
        if (question["type"] == "mcq"):
            response = (
                self.supabase.table("QuestionBank")
                .upsert({"question_id" : overview["questionId"], 
                        "u_id" : overview["uId"], 
                        "external_id" : overview["external_id"],
                        "source" : source,
                        "primary_cat_cd" : overview["primary_class_cd"],
                        "skill_cd" : overview["skill_cd"],
                        "difficulty" : 1 if overview["difficulty"] == "E" else 2 if overview["difficulty"] == "M" else 3,
                        "score_difficulty" : overview["score_band_range_cd"],
                        "stem" : question["stem"] if "stem" in question else None,
                        "stimulus" : question["stimulus"] if "stimulus" in question else None,
                        "type" : question["type"],
                        "ans_a" : question["answerOptions"][0]["content"],
                        "ans_b" : question["answerOptions"][1]["content"],
                        "ans_c" : question["answerOptions"][2]["content"],
                        "ans_d" : question["answerOptions"][3]["content"],
                        "correct_ans" : question["correct_answer"],
                        "explanation" : question["rationale"],
                        "test" : overview["program"],
                        "subject" : "English" if overview["primary_class_cd"] in ["INI", "CAS", "EOI", "SEC"] else "Math"
                        }, on_conflict="external_id", ignore_duplicates=True)
                .execute()
            )
        elif (question["type"] == "spr"):
            response = (
                self.supabase.table("QuestionBank")
                .upsert({"question_id" : overview["questionId"], 
                        "u_id" : overview["uId"], 
                        "external_id" : overview["external_id"],
                        "source" : source,
                        "primary_cat_cd" : overview["primary_class_cd"],
                        "skill_cd" : overview["skill_cd"],
                        "difficulty" : 1 if overview["difficulty"] == "E" else 2 if overview["difficulty"] == "M" else 3,
                        "score_difficulty" : overview["score_band_range_cd"],
                        "stem" : question["stem"] if "stem" in question else None,
                        "stimulus" : question["stimulus"] if "stimulus" in question else None,
                        "type" : question["type"],
                        "ans_a" : None,
                        "ans_b" : None,
                        "ans_c" : None,
                        "ans_d" : None,
                        "correct_ans" : question["correct_answer"],
                        "explanation" : question["rationale"],
                        "test" : overview["program"],
                        "subject" : "English" if overview["primary_class_cd"] in ["INI", "CAS", "EOI", "SEC"] else "Math"
                        }, on_conflict="external_id", ignore_duplicates=True)
                .execute()
            )
        else:
            raise ValueError("Invalid question type")

    def get_questions(self, category: str, difficulty: str, amount: int):
        query = f"SELECT * FROM questions WHERE category = '{category}' AND difficulty = '{difficulty}' ORDER BY RANDOM() LIMIT {amount}"
        response = self.client.query(query)
        return response['data']