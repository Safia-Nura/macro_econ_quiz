from validators import validate_name, validate_topic
#here we are testing name input and question topics based on the validators.py file
#first three tests are for accept valid names, if in put is empty and if there is any gaps in the input e.g. whitespace
def test_valid_named():
    assert validate_name("Jane Doe") == True
def test_emptpy_name():
    assert validate_name("")== False
def test_whitespace_only():
    assert validate_name("   ") == False
#here we are testing the string limit - as seen in validators.py this should fail due to character limit being 60
def test_name_too_long():
 assert validate_name("a"*61) == False
def test_valid_topic():
   assert validate_topic("GDP", ["GDP","Real vs Nominal"]) == True
def test_invalid_topic():
   assert validate_topic("Unknown",[ "GDP","Real vs Nominal"])== False