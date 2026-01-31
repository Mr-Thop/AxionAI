from Models import Model
from dotenv import load_dotenv
import os

load_dotenv()

class InterviewEvaluator(Model):
    def __init__(self,model,tech=None,non_tech=None):
        PROMPT = os.getenv("Eval_prompt")
        super().__init__(PROMPT,model)
        self.tech_questions = [
            "What is a stack data structure?",
            "What is a queue data structure?",
            "What is object-oriented programming?",
            "What is an API?",
            "What is a database index?"
        ]
        self.non_tech_questions = [
            "Can you introduce yourself?",
            "What are your strengths?",
            "How do you handle stress or pressure?",
            "Why do you want to work with our organization?",
            "Describe a challenge you faced and how you overcame it."
        ]

    def ask(self,id):
        if id:
            return self.tech_questions
        else:
            return self.non_tech_questions
        
    def edit(self,questions,id):
        if id:
            self.tech_questions = questions
        else:
            self.non_tech_questions = questions

    
    def score_candid(self,candidate_output):
        return self.send(candidate_output)