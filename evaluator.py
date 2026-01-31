from Models import Model
from dotenv import load_dotenv

load_dotenv()

class InterviewEvaluator(Model):
    def __init__(self,tech=None,non_tech=None):
        PROMPT = os.getenv("Eval_prompt")
        super().__init__(PROMPT)
        self.tech_questions = tech if tech else [
            "What is a stack data structure?",
            "What is a queue data structure?",
            "What is object-oriented programming?",
            "What is an API?",
            "What is a database index?"
        ]
        self.non_tech_questions = non_tech if non_tech else [
            "Can you introduce yourself?",
            "What are your strengths?",
            "How do you handle stress or pressure?",
            "Why do you want to work with our organization?",
            "Describe a challenge you faced and how you overcame it."
        ]

    def ask_tech(self):
        return self.tech_questions

    def ask_non_tech(self):
        return self.non_tech_questions

    def score_candid(self,candidate_output):
        return self.send(candidate_output)