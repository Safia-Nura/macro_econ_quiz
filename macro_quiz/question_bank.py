import json
import random
from question import Question
class QuestionBank:
    def __init__(self, filepath: str = "questions.json"):
       # Start with an empty list then load questions from the file
        self.questions = []
        self._load(filepath)
    def _load(self, filepath: str) -> None:
        try:
                   with open(filepath) as f:
                        data = json.load(f) 
                        for item in data:
                             q = Question(text=item["text"],
                                           options=item["options"],
                                           correct_index=item["correct_index"],
                                           topic=item["topic"],
                                           explanation=item.get("explanation", ""))
                             # Add the question to list
                             self.questions.append(q)
        except FileNotFoundError:
            # Raise a clear error message if the file cannot be found
             raise FileNotFoundError(f"Could not find questions file: {filepath}")
    def get_topics(self) -> list:
        # Pull the topic from every question remove duplicates, then sort
        topics = []
        for q in self.questions:
             if q.topic not in topics:
                  topics.append(q.topic)
        return sorted(topics)
    def get_questions(self,topic,count):
        # Filter by topic if one was given otherwise use all questions
        pool = []
        for q in self.questions:
             if topic == None or q.topic == topic:
                  pool.append(q)
            # Check we have enough questions before trying to pick
             if count >len(pool):
              print ("Not enough questions")
             return[]
        # Picks randomly from the pool so the quiz is different each time
        return random.sample(pool, count)
             

 
    
    
