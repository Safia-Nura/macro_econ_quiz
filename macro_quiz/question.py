class Question:
    # represents a single quick question
    #attributes: test =  question text, options = list of four answers (strings), correct_index = index (0-3) of correct answers, topic = topic category the question belongs to and explanation: optional expliantion after the Q. is answered.
    def __init__(self, text:str, options:list,correct_index:int,
                 topic:str, explanation:str =""):
        self.text =text
        self.options =options
        self.correct_index =correct_index
        self.topic =topic
        self.explanation =explanation
    
    def is_correct(self,answer_index: int) ->bool:
        #checks whether the answer is correct
        # argument: answer_index: the index (0-3) the user choose, returns true if correct/false otherwise
        return answer_index ==self.correct_index