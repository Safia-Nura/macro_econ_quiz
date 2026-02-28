#validates characters used for names
def validate_name(name: str) -> bool:
  
    if not isinstance(name,str):
        return False
    stripped =name.strip()
    return 0< len(stripped) <=60
#topic validations to ensure characters align with listed topics 
def validate_topic(topic: str, valid_topics: list) -> bool:

    return topic in valid_topics