from dotenv import load_dotenv
import os
from supabase import create_client, Client
from bs4 import BeautifulSoup
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
                        "stem" : (BeautifulSoup(question["stem"], "html.parser").p.get_text()),
                        "stimulus" : (BeautifulSoup(question["stimulus"], "html.parser").p.get_text()),
                        "type" : question["type"],
                        "ans_a" : (BeautifulSoup(question["answerOptions"][0]["content"], "html.parser").p.get_text()),
                        "ans_b" : (BeautifulSoup(question["answerOptions"][1]["content"], "html.parser").p.get_text()),
                        "ans_c" : (BeautifulSoup(question["answerOptions"][2]["content"], "html.parser").p.get_text()),
                        "ans_d" : (BeautifulSoup(question["answerOptions"][3]["content"], "html.parser").p.get_text()),
                        "correct_ans" : question["correct_answer"][0],
                        "explanation" : (BeautifulSoup(question["rationale"], "html.parser").p.get_text()),
                        "test" : overview["program"],
                        "subject" : "English" if overview["primary_class_cd"] in ["INI", "CAS", "EOI", "SEC"] else "Math"
                        })
                .on_conflict("external_id")
                .do_nothing()
                .execute()
            )
        elif (question["type"] == "spr"):
            # response = (
            #     self.supabase.table("QuestionBank")
            #     .insert({"question_id" : overview["questionId"], 
            #             "u_id" : overview["uId"], 
            #             "external_id" : overview["external_id"],
            #             "source" : source,
            #             "primary_cat_cd" : overview["primary_class_cd"],
            #             "skill_cd" : overview["skill_cd"],
            #             "difficulty" : 1 if overview["difficulty"] == "E" else 2 if overview["difficulty"] == "M" else 3,
            #             "score_difficulty" : overview["score_band_range_cd"],
            #             "stem" : (BeautifulSoup(question["stem"], "html.parser").p.get_text()),
            #             "stimulus" : (BeautifulSoup(question["stimulus"], "html.parser").p.get_text()),
            #             "type" : question["type"],
            #             "ans_a" : (BeautifulSoup(question["answerOptions"][0]["content"], "html.parser").p.get_text()),
            #             "ans_b" : (BeautifulSoup(question["answerOptions"][1]["content"], "html.parser").p.get_text()),
            #             "ans_c" : (BeautifulSoup(question["answerOptions"][2]["content"], "html.parser").p.get_text()),
            #             "ans_d" : (BeautifulSoup(question["answerOptions"][3]["content"], "html.parser").p.get_text()),
            #             "correct_ans" : question["correct_answer"][0],
            #             "explanation" : (BeautifulSoup(question["rationale"], "html.parser").p.get_text()),
            #             "test" : overview["program"],
            #             "subject" : "English" if overview["primary_class_cd"] in ["INI", "CAS", "EOI", "SEC"] else "Math"
            #             })
            #     .execute()
            # )
            raise ValueError("Not implemented")
        else:
            raise ValueError("Invalid question type")

    def get_questions(self, category: str, difficulty: str, amount: int):
        query = f"SELECT * FROM questions WHERE category = '{category}' AND difficulty = '{difficulty}' ORDER BY RANDOM() LIMIT {amount}"
        response = self.client.query(query)
        return response['data']