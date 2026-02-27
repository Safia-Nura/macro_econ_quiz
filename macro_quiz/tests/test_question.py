import pytest
from question import Question

def test_question_stores_text():
    q =Question("What is the GDP?",["A","B","C","D"],2,"GDP")
    assert q.text =="What is the GDP?"
def test_correct_answer():
    q =Question("What is the GDP?",["A","B","C","D"],2,"GDP")
    assert q.is_correct(2) == True
def test_wrong_answer():
        q =Question("What is the GDP?",["A","B","C","D"],2,"GDP")
        assert q.is_correct(0) == False
def test_topic_stored():
        q =Question("What is the GDP?",["A","B","C","D"],2,"GDP")
        assert q.topic=="GDP"
def test_explanation_defaults_empty():
          q =Question("What is the GDP?",["A","B","C","D"],2,"GDP")
          assert q.explanation== ""