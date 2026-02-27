import json
import random
from question import Question

class QuestionBank:
    #full collection of quiz questions loaded from JSON file
    def __init__(self, filepath: str= "questions.json"):
        self.questions =[]
        self._load(filepath)
    def _load(self, filepath: str) -> None:
        #reads JSON file and builds question objects
        try:
            with open(filepath,"r") as f:
                data =json.load(f)
            for item in data:
                q = Question ( 
                    text=item["text"],
                    options=item["options"],
                    correct_index=item["correct_index"],
                    topic=item["topic"],
                    explanation=item.get("explanation","")
                )
                self.questions.append(q)
        except FileNotFoundError:
            raise FileNotFoundError(f"Could not find questions file: {filepath}")
    def get_topics(self)->list:
        #returns a list of unique topic names
        return sorted(set(q.topic for q in self.questions))
    def get_questions(self,topic: str= None, count: int = 5) ->list:
        #returns random selection of question and optionally filtered by topic
     if topic:
        pool =[q for q in self.questions if q.topic == topic]
     else:
             pool =self.questions
     if count > len(pool):
         raise ValueError( f" Requested {count} questions however, only {len(pool)} available" f"for topic {topic}")    
     return random.sample(pool, count)
             

 
    
    
