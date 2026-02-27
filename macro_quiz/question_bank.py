import json
import random
import os
from question import Question
class QuestionBank:
    def __init__(self, filepath: str = None):
        # If no filepath given, find questions.json in the same folder as this file
        if filepath is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filepath = os.path.join(base_dir, "questions.json")
        # Start with an empty list then load questions from the file
        self.questions = []
        self._load(filepath)
    def _load(self, filepath: str) -> None:
        try:
            # Open and read the JSON file
            with open(filepath, "r") as f:
                data = json.load(f)
            # Loop through each entry and create a Question object from it
            for item in data:
                q = Question(
                    text=item["text"],
                    options=item["options"],
                    correct_index=item["correct_index"],
                    topic=item["topic"],
                    explanation=item.get("explanation", "")
                )
                # Add the question to list
                self.questions.append(q)
        except FileNotFoundError:
            # Raise a clear error message if the file cannot be found
            raise FileNotFoundError(f"Could not find questions file: {filepath}")
    def get_topics(self) -> list:
        # Pull the topic from every question remove duplicates, then sort
        return sorted(set(q.topic for q in self.questions))
    def get_questions(self, topic: str = None, count: int = 5) -> list:
        # Filter by topic if one was given otherwise use all questions
        if topic:
            pool = [q for q in self.questions if q.topic == topic]
        else:
            pool = self.questions
        # Check we have enough questions before trying to pick
        if count > len(pool):
            raise ValueError(
                f"Requested {count} questions however, only {len(pool)} available "
                f"for topic '{topic}'."
            )
        # Picks randomly from the pool so the quiz is different each time
        return random.sample(pool, count)
             

 
    
    
