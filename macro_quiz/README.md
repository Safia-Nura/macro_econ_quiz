# Macroeconomic Surveillance Quiz

---

## Table of Contents

- [1. Introduction](#1-introduction)
- [2. Design](#2-design)
- [3. Development](#3-development)
- [4. Testing](#4-testing)
- [5. Documentation](#5-documentation)
- [6. Evaluation](#6-evaluation)

---

## 1. Introduction

I work as a Senior Research Assitant within a macroeconomic surveillance team that
monitors economic conditions in China and the United States. The team works daily
with indicators such as GDP growth, trade balances, inflation indices and exchange
rate movements. New analysts joining the team are expected to understand the
mathematical calculations that underpin these indicators before they contribute to
briefing products.

To support this, I developed a desktop quiz application using Python and Tkinter.
The application tests users on five core topic areas directly relevant to the team's
work: GDP measurement, real versus nominal GDP, growth rate calculations, trade
balance arithmetic, and exchange rates and purchasing power parity. Each topic
contains five multiple-choice questions, giving a pool of 25 questions in total.

The application is a Minimum Viable Product (MVP) designed to meet a genuine
training need. It provides a simple, self-paced interface that requires no
installation beyond Python itself. Results are saved automatically to a CSV file
after every attempt, which analysts can export and use as training evidence. The
project follows a professional development process, with code stored on GitHub,
features added incrementally, automated testing via pytest, and a continuous
integration pipeline using GitHub Actions.

---

## 2. Design

### 2.1 GUI Design

The interface is divided into three screens. The user moves through them in order:
Welcome → Quiz → Results.

**Welcome Screen**
- Name entry field
- Topic dropdown (populated from `questions.json`)
- Inline error message if name is invalid
- Start Quiz button

**Quiz Screen**
- Progress label (e.g. "Question 2 of 5 | Topic: GDP")
- Question text
- Four radio buttons for answer options
- Submit Answer button
- Feedback label showing correct or incorrect and an explanation
- Next button to advance

**Results Screen**
- Final score as a fraction and percentage
- Motivational message based on score
- View All Results button (opens a scrollable history window)
- Take Another Quiz button

### 2.2 Functional and Non-Functional Requirements

**Functional Requirements**

| ID | Requirement |
|---|---|
| F1 | The application must present multiple-choice questions one at a time |
| F2 | The user must be able to select a topic before starting |
| F3 | The application must show whether the answer was correct immediately |
| F4 | Results must be saved to a CSV file automatically after each attempt |
| F5 | The user must be able to view all past results within the application |
| F6 | Input validation must prevent empty or invalid names from being submitted |

**Non-Functional Requirements**

| ID | Requirement |
|---|---|
| N1 | The application must run on any machine with Python 3.9+ installed |
| N2 | No external libraries should be required |
| N3 | The interface must be usable by someone with no technical background |
| N4 | The CSV file must be readable in Excel without any conversion |



Tkinter was chosen over Flask or Streamlit because it is part of the Python
standard library. This means the application runs without any `pip install` step,
which makes it straightforward to share with colleagues.

### 2.4 Class Diagram


```mermaid
classDiagram
    class Question {
        -text str
        -options list
        -correct_index int
        -topic str
        -explanation str
        +is_correct(answer_index int) bool
    }

    class QuestionBank {
        -questions list
        -filepath str
        +get_topics() list
        +get_questions(topic str, count int) list
        -_load(filepath str)
    }

    class ResultStore {
        -filepath str
        -HEADERS list
        +append_result(name, topic, score, total)
        +load_results() list
        -_ensure_file_exists()
    }

    class QuizApp {
        -bank QuestionBank
        -store ResultStore
        -user_name str
        -selected_topic str
        -questions list
        -current_index int
        -score int
        -answer_var IntVar
        +start_quiz(name str, topic str) bool
        +submit_answer() tuple
        +next_question()
        +show_frame(frame_class)
    }

    class WelcomeFrame {
        -name_entry Entry
        -topic_dropdown Combobox
        -error_label Label
        +_build()
        +_on_start()
    }

    class QuizFrame {
        -progress_label Label
        -question_label Label
        -radio_buttons list
        -feedback_label Label
        +_build()
        +load_question()
        +_on_submit()
        +_on_next()
    }

    class ResultsFrame {
        -score_label Label
        -message_label Label
        +_build()
        +show_results()
        +_view_results()
        +_restart()
    }

    QuestionBank --> Question : creates
    QuizApp --> QuestionBank : uses
    QuizApp --> ResultStore : uses
    QuizApp --> WelcomeFrame : contains
    QuizApp --> QuizFrame : contains
    QuizApp --> ResultsFrame : contains
```
### 2.5 Sequence Diagram
```mermaid
sequenceDiagram
    actor User
    participant WelcomeFrame
    participant QuizApp
    participant QuestionBank
    participant QuizFrame
    participant ResultStore
    participant ResultsFrame

    User->>WelcomeFrame: Enter name and select topic
    WelcomeFrame->>QuizApp: _on_start()
    QuizApp->>QuizApp: validate_name() and validate_topic()
    QuizApp->>QuestionBank: get_questions(topic, count=5)
    QuestionBank-->>QuizApp: questions list
    QuizApp->>QuizFrame: load_question()
    QuizApp->>WelcomeFrame: show_frame(QuizFrame)

    loop For each question
        User->>QuizFrame: Select answer and click Submit
        QuizFrame->>QuizApp: submit_answer()
        QuizApp-->>QuizFrame: correct, correct_index, explanation
        QuizFrame->>User: Show feedback
        User->>QuizFrame: Click Next
        QuizFrame->>QuizApp: next_question()
    end

    QuizApp->>ResultStore: append_result(name, topic, score, total)
    ResultStore-->>QuizApp: writes to results.csv
    QuizApp->>ResultsFrame: show_results()
    QuizApp->>QuizFrame: show_frame(ResultsFrame)
    ResultsFrame->>User: Display final score
```
### 2.6 Application Flow
```mermaid
stateDiagram-v2
    [*] --> WelcomeScreen

    WelcomeScreen --> WelcomeScreen : Invalid name entered
    WelcomeScreen --> QuizScreen : Valid name and topic submitted

    QuizScreen --> QuizScreen : Answer submitted, Next clicked
    QuizScreen --> ResultsScreen : Final question answered

    ResultsScreen --> WelcomeScreen : Take Another Quiz clicked
    ResultsScreen --> ResultsScreen : View All Results clicked

    ResultsScreen --> [*]
```
---

## 3. Development

### 3.1 Question and QuestionBank

The `Question` class stores a single quiz item. The `is_correct()` method
returns `True` if the selected index matches the correct answer.

```python
class Question:
    def __init__(self, text, options, correct_index, topic, explanation=""):
        self.text = text
        self.options = options
        self.correct_index = correct_index
        self.topic = topic
        self.explanation = explanation

    def is_correct(self, answer_index: int) -> bool:
        # Compare selected answer to correct answer
        return answer_index == self.correct_index
```

`QuestionBank` loads all questions from `questions.json` on initialisation.
`get_questions()` filters by topic and returns a random selection. If more
questions are requested than are available, a `ValueError` is raised.

```python
def get_questions(self, topic: str = None, count: int = 5) -> list:
    # Filter by topic if one was given, otherwise use all questions
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
    # Pick randomly so the quiz is different each time
    return random.sample(pool, count)
```

### 3.2 ResultStore

`ResultStore` handles all CSV interaction. On first run it creates the file
with the correct headers. `append_result()` writes one row per completed
attempt, stamped with the current date and time.

```python
def append_result(self, name: str, topic: str, score: int, total: int) -> None:
    row = {
        "name": name,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "topic": topic,
        "score": score,
        "total": total
    }
    # Open in append mode so existing records are not overwritten
    with open(self.filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=self.HEADERS)
        writer.writerow(row)
```

### 3.3 Validators

Input validation uses pure functions in `validators.py`. A pure function
always returns the same output for the same input with no side effects,
which makes it straightforward to test in isolation.

```python
def validate_name(name: str) -> bool:
    # Reject empty strings, whitespace-only and names over 60 characters
    if not isinstance(name, str):
        return False
    stripped = name.strip()
    return 0 < len(stripped) <= 60
```

### 3.4 Tkinter GUI

The application uses three `tk.Frame` screens stacked on top of each other.
`tkraise()` brings the relevant frame to the front when needed. `QuizApp`
inherits from `tk.Tk` and holds all application state as instance attributes,
avoiding global variables.

```python
# Stretch the frame to fill the full window
self.grid_rowconfigure(0, weight=1)
self.grid_columnconfigure(0, weight=1)

for FrameClass in (WelcomeFrame, QuizFrame, ResultsFrame):
    frame = FrameClass(self)
    self.frames[FrameClass] = frame
    frame.grid(row=0, column=0, sticky="nsew")

self.show_frame(WelcomeFrame)
```

---

## 4. Testing

### 4.1 Testing Strategy

Two methods of testing were used. Automated unit testing with pytest was used
for all logic that does not depend on the GUI, such as the validator functions,
the `Question` class and `ResultStore`. Manual testing was used to verify GUI
behaviour including screen transitions, feedback messages and the results window.

Unit testing was prioritised for pure functions and file I/O because these are
the most likely sources of silent errors. GUI behaviour was tested manually
because Tkinter interfaces are difficult to test automatically without additional
frameworks.

### 4.2 Manual Test Outcomes

| Test | Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|
| Empty name rejected | Leave name blank, click Start | Error message appears | Error message appeared |  Pass |
| Valid name accepted | Enter "Test User", click Start | Quiz screen loads | Quiz screen loaded |  Pass |
| Wrong answer feedback | Select wrong answer, submit | Red feedback with correct answer | Correct |  Pass |
| Correct answer feedback | Select correct answer, submit | Green "Correct!" message | Correct |  Pass |
| Score saved to CSV | Complete a quiz | New row in results.csv | Row written correctly |  Pass |
| View All Results | Click View All Results | Scrollable window with history | Opened correctly | Pass |
| Take Another Quiz | Click Take Another Quiz | Returns to Welcome screen | Returned correctly |  Pass |

### 4.3 Unit Test Outcomes

The test suite contains 19 test cases across four modules. All 19 pass.

```
tests/test_question.py::test_question_stores_text          PASSED
tests/test_question.py::test_correct_answer                PASSED
tests/test_question.py::test_wrong_answer                  PASSED
tests/test_question.py::test_topic_stored                  PASSED
tests/test_question.py::test_explanation_defaults_empty    PASSED
tests/test_question_bank.py::test_loads_questions          PASSED
tests/test_question_bank.py::test_get_topics_return_list   PASSED
tests/test_question_bank.py::test_filter_by_topics         PASSED
tests/test_question_bank.py::tests_raise_if_count_too_high PASSED
tests/test_question_bank.py::test_missing_file_raises_error PASSED
tests/test_result_store.py::test_file_created_on_init      PASSED
tests/test_result_store.py::test_multiple_results          PASSED
tests/test_result_store.py::test_empty_file_returns_empty_list PASSED
tests/test_validators.py::test_valid_named                 PASSED
tests/test_validators.py::test_emptpy_name                 PASSED
tests/test_validators.py::test_whitespace_only             PASSED
tests/test_validators.py::test_name_too_long               PASSED
tests/test_validators.py::test_valid_topic                 PASSED
tests/test_validators.py::test_invalid_topic               PASSED

19 passed
```

The GitHub Actions CI pipeline runs these tests automatically on every push to
main. A green tick on a commit confirms all tests passed.

---

## 5. Documentation

### 5.1 User Documentation

**How to start the application**

1. Ensure Python 3.9 or later is installed
2. Open a terminal and navigate to the project folder
3. Run `python quiz_app.py`

**Taking a quiz**

1. Enter your name in the text field
2. Select a topic from the dropdown
3. Click Start Quiz
4. For each question, select one of the four options and click Submit Answer
5. Read the feedback, then click Next to continue
6. Your final score is shown at the end of the session

**Viewing and exporting results**

- Click View All Results on the results screen to see all past attempts
- The `results.csv` file in the project folder can be opened directly in Excel
  and submitted as appraisal evidence

### 5.2 Technical Documentation

**Running tests locally**

```
pytest tests/ -v
```

**Project structure**

```
macro_quiz/
├── quiz_app.py         — Tkinter GUI and application entry point
├── question.py         — Question class
├── question_bank.py    — Loads and filters questions
├── result_store.py     — Saves and reads results to CSV
├── validators.py       — Pure input validation functions
├── questions.json      — All 25 quiz questions
├── tests/              — pytest test suite
└── .github/workflows/  — GitHub Actions CI pipeline
```

**Adding new questions**

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

`correct_index` is 0 for A, 1 for B, 2 for C and 3 for D. No code changes
are needed when adding questions.

---

## 6. Evaluation

Overall I am pleased with how the project turned out. The application works as
intended and meets all six technical requirements in the brief. Building the
logic classes first and testing them before starting the GUI made the development
process much smoother. When bugs appeared in the interface, I could be confident
the underlying logic was correct, which made them quicker to identify and fix.

Choosing Tkinter was the right decision at this stage of the apprenticeship. It
taught me how GUI event loops, widget state and callback functions work in a
practical and direct way. Working through the indentation errors and debugging
the class structure also improved my understanding of how Python handles objects
and scope, which I found genuinely useful.

The CI pipeline was also valuable. It caught two regressions during development
that would otherwise have gone unnoticed. Seeing the green tick on GitHub after
every push gave me confidence the codebase remained stable throughout.

There are things I would improve with more time. The application has no timer,
which means questions are untimed and do not reflect the pressure of real
analytical deadlines. There is also no administrator interface, so adding new
questions requires editing the JSON file directly, which may be a barrier for
less technical colleagues. In a future version I would add a timed mode and a
simple admin screen for managing questions through the GUI. I would also
consider packaging the application as a standalone executable using
[PyInstaller](https://pyinstaller.org) so colleagues without Python installed
could run it without any setup.

---

## References

- [Python Tkinter documentation](https://docs.python.org/3/library/tkinter.html)
- [pytest documentation](https://docs.pytest.org)
- [GitHub Actions documentation](https://docs.github.com/en/actions)
- [PyInstaller documentation](https://pyinstaller.org/en/stable/)
