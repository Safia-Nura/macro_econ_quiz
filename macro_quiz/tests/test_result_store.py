import os 
import pytest
from result_store import ResultStore

TEST_FILE ="test_results.csv"

def setup_functions():
 #removes test file befopre each test to start new
 if os.path.exists(TEST_FILE):
  os.remove(TEST_FILE)
def teardown_function():
 #deletes after every test as well
 if os.path.exists(TEST_FILE):
  os.remove(TEST_FILE)

def test_file_created_on_init():
 ResultStore(filepath= TEST_FILE)
 assert os.path.exists(TEST_FILE)

 def test_file_appended_and_load():
  store = ResultStore(filepath= TEST_FILE)
  store.append_results("Jen", "GDP", 4,5)
  results = store.load_results()
  assert len(results) == 1
  assert results[0]["name"] == "Jen"
  assert results[0]["score"] =="4"
def test_multiple_results():
 store =ResultStore(filepath=TEST_FILE)
 store.append_results("Jen", "GDP", 4,5)
 store.append_results("Bob", "Real vs Nominal",3,5)
 results = store.load_results()
 assert len(results)==2

def test_empty_file_returns_empty_list():
 store =ResultStore(filepath= TEST_FILE)
 results = store.load_results()
 assert results == []



