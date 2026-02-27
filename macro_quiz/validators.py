def validate_name(name: str) -> bool:
    #check name is non-empty and under 60 characters.
    #argument name: the users name input 
    #returns true if valid and false otherwise
    if not isinstance(name,str):
        return False
    stripped =name.strip()
    return 0< len(stripped) <=60
def validate_topic(topic: str, valid_topics: list) -> bool:
    # checks topic is one of the allowed/expected options
    #argument topic: the selected topic string
    #valid_topics = lists of accepted topic names.
    # simialr to the first test will return true if valid, false otherwise
    return topic in valid_topics