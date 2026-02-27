import pytest
from question_bank import QuestionBank

# real questions must be used by .json file
def test_loads_questions():
    bank =QuestionBank()
    assert len(bank.questions) >0

def test_get_topics_return_list():
    bank =QuestionBank()
    topics =bank.get_topics()
    assert isinstance(topics,list)
    assert len(topics)>0

def test_filter_by_topics():
    bank = QuestionBank()
    topic = bank.get_topics()[0]
    questions =bank.get_questions(topic=topic, count=1)
    assert all(q.topic == topic for q in questions)
def tests_raise_if_count_too_high():
    bank = QuestionBank()
    topic = bank.get_topics()[0]
    with pytest.raises(ValueError):
        bank.get_questions(topic=topic, count= 9999)
def test_missing_file_raises_error():
    with pytest.raises(FileNotFoundError):
        QuestionBank(filepath="nonexistent.json")
        
