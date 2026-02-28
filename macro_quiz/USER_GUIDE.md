# Macroeconomic Surveillance Quiz

A desktop quiz application for testing core macroeconomic calculation skills.
Built with Python and Tkinter for use by the macroeconomic surveillance team.

---

## What the quiz covers

- GDP and the expenditure approach (C + I + G + NX)
- Real vs Nominal GDP and the GDP deflator
- Growth rate calculations
- Trade balance and current account
- Exchange rates and purchasing power parity

---

## Requirements

- Python 3.9 or later
- No additional installs needed — all libraries used are built into Python

---

## How to run the app

1. Clone the repository:
```
git clone https://https://github.com/Safia-Nura/macro_econ_quiz
```
2. Navigate into the project folder:

```
cd macro_quiz
 ```

3. Run the application:
```
python quiz_app.py
```
---
## How to run the tests
```
pytest tests/ -v
```
All 19 tests should pass.

---
## Project structure
---
```macro_quiz/
├── quiz_app.py         — Tkinter GUI, main application
├── question.py         — Question class
├── question_bank.py    — loads and filters questions from JSON
├── result_store.py     — saves and reads results to CSV
├── validators.py       — input validation functions
├── questions.json      — all 25 quiz questions
├── tests/
│   ├── test_question.py
│   ├── test_question_bank.py
│   ├── test_result_store.py
│   └── test_validators.py
├── .github/
│   └── workflows/
│       └── ci.yml      — GitHub Actions CI pipeline
├── README.md
```

---

## How results are saved

Every completed quiz attempt is automatically saved to `results.csv` in the
project folder. Each row records the user name, date, topic, score and total.
This file can be opened directly in Excel and used as appraisal evidence.

---

## How to add new questions

Open `questions.json` and add a new entry following this format:
```json
{
  "text": "Your question here?",
  "options": ["Option A", "Option B", "Option C", "Option D"],
  "correct_index": 0,
  "topic": "GDP",
  "explanation": "Brief explanation of the correct answer."
}
```

`correct_index` is the position of the correct answer — 0 for A, 1 for B,
2 for C, 3 for D.

---

## Technologies used
---
- Python 3.9+ Core programming language 
- Tkinter Desktop GUI framework 
- csv module: permeant storage for results  
- json modul:e  Loading quiz questions 
 - pytest: Unit testing 
- GitHub Actions :Continuous integration

---

## Running CI

The GitHub Actions pipeline runs automatically on every push to main.
It runs the full pytest suite and flake8 style checks.
A green tick on a commit means all tests passed.
