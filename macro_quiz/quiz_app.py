import tkinter as tk
from tkinter import ttk , messagebox
from question_bank import QuestionBank
from result_store import ResultStore
from validators import validate_name, validate_topic

class QuizApp(tk.Tk):
    # main Tkinter app for my MacroEconomic key formula's quiz

    def __init__(self):
        super().__init__()
        self.title("Macroeconomic knowledge quiz")
        self.geometry("650x500")
        self.resizable(False,False)

        self.bank =QuestionBank()
        self.store = ResultStore()

        self.user_name =""
        self.selected_topic =""
        self.questions = []
        self.current_index =0
        self.score =0
        self.answer_var = tk.IntVar(value=-1)
        # stretches frame to match window size
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
         # Create all frames
        self.frames = {}
        for FrameClass in (WelcomeFrame, QuizFrame, ResultsFrame):
            frame = FrameClass(self)
            self.frames[FrameClass] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WelcomeFrame)

    def show_frame(self, frame_class):
        #Brings specified frame to the front.

        
        frame = self.frames[frame_class]
        frame.tkraise()

    def start_quiz(self, name: str, topic: str):
    # here this will validate inputs and begin a quiz session.
        if not validate_name(name):
            return False
        if not validate_topic(topic, self.bank.get_topics()):
            return False

        self.user_name = name
        self.selected_topic = topic
        self.questions = self.bank.get_questions(topic=topic, count=5)
        self.current_index = 0
        self.score = 0
        self.answer_var.set(-1)

        self.frames[QuizFrame].load_question()
        self.show_frame(QuizFrame)
        return True

    def submit_answer(self):
        #Checks the selected answer and updates score.

        selected = self.answer_var.get()
        question = self.questions[self.current_index]
        correct = question.is_correct(selected)
        if correct:
            self.score += 1
        return correct, question.correct_index, question.explanation

    def next_question(self):
        #go to the next question or finish the quiz
        self.current_index += 1
        self.answer_var.set(-1)

        if self.current_index < len(self.questions):
            self.frames[QuizFrame].load_question()
        else:
            self.store.append_result(
                self.user_name,
                self.selected_topic,
                self.score,
                len(self.questions)
            )
            self.frames[ResultsFrame].show_results()
            self.show_frame(ResultsFrame)


class WelcomeFrame(tk.Frame):
#The starting screen where the user enters their name and picks a topic.

    def __init__(self, master):
        #Build the welcome screen widgets.
        super().__init__(master, bg="#f0f4f8")
        self.master = master
        self._build()

    def _build(self):
        #Create and layout all widgets on the welcome screen
        tk.Label(
            self, text="Macroeconomic Surveillance Quiz",
            font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1F3864"
        ).pack(pady=(40, 5))

        tk.Label(
            self, text="Test your macroeconomic calculation skills",
            font=("Arial", 11), bg="#f0f4f8", fg="#555555"
        ).pack(pady=(0, 30))

        # Name entry
        tk.Label(
            self, text="Your Name:", font=("Arial", 11), bg="#f0f4f8"
        ).pack()
        self.name_entry = tk.Entry(self, font=("Arial", 11), width=30)
        self.name_entry.pack(pady=(5, 15))

        # Topic dropdown
        tk.Label(
            self, text="Select Topic:", font=("Arial", 11), bg="#f0f4f8"
        ).pack()
        self.topic_var = tk.StringVar()
        topics = self.master.bank.get_topics()
        self.topic_dropdown = ttk.Combobox(
            self, textvariable=self.topic_var,
            values=topics, state="readonly", width=28
        )
        self.topic_dropdown.pack(pady=(5, 5))
        self.topic_dropdown.current(0)

        # Error label 
        self.error_label = tk.Label(
            self, text="", font=("Arial", 10), bg="#f0f4f8", fg="red"
        )
        self.error_label.pack(pady=(5, 0))

        # Start button
        tk.Button(
            self, text="Start Quiz", font=("Arial", 12, "bold"),
            bg="#2E75B6", fg="white", padx=20, pady=8,
            command=self._on_start
        ).pack(pady=20)

    def _on_start(self):
        #Handle the Start Quiz button
        name = self.name_entry.get()
        topic = self.topic_var.get()

        if not validate_name(name):
            self.error_label.config(
                text="Please enter a valid name (1-60 characters)."
            )
            return

        self.error_label.config(text="")
        self.master.start_quiz(name, topic)


class QuizFrame(tk.Frame):
    #displays questions and answer options

    def __init__(self, master):
        #Build the quiz screen widgets.
        super().__init__(master, bg="#f0f4f8")
        self.master = master
        self._build()

    def _build(self):
        #Create and layout all widgets on the quiz screen
        self.progress_label = tk.Label(
            self, text="", font=("Arial", 10), bg="#f0f4f8", fg="#555555"
        )
        self.progress_label.pack(pady=(20, 5))

        self.question_label = tk.Label(
            self, text="", font=("Arial", 13, "bold"),
            bg="#f0f4f8", fg="#1F3864", wraplength=560, justify="left"
        )
        self.question_label.pack(pady=(10, 20), padx=40)

        # Radio buttons for answer options
        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(
                self, text="", font=("Arial", 11),
                bg="#f0f4f8", variable=self.master.answer_var,
                value=i, anchor="w"
            )
            rb.pack(fill="x", padx=60, pady=3)
            self.radio_buttons.append(rb)

        self.feedback_label = tk.Label(
            self, text="", font=("Arial", 11),
            bg="#f0f4f8", wraplength=560
        )
        self.feedback_label.pack(pady=(15, 5), padx=40)

        self.submit_btn = tk.Button(
            self, text="Submit Answer", font=("Arial", 11, "bold"),
            bg="#2E75B6", fg="white", padx=15, pady=6,
            command=self._on_submit
        )
        self.submit_btn.pack(pady=10)

        self.next_btn = tk.Button(
            self, text="Next", font=("Arial", 11, "bold"),
            bg="#1F3864", fg="white", padx=15, pady=6,
            command=self._on_next
        )

    def load_question(self):
        #here widgets will populate with the current questions 
        idx = self.master.current_index
        total = len(self.master.questions)
        question = self.master.questions[idx]

        self.progress_label.config(
            text=f"Question {idx + 1} of {total}  |  Topic: {question.topic}"
        )
        self.question_label.config(text=question.text)

        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=question.options[i], state="normal")

        self.feedback_label.config(text="")
        self.submit_btn.pack(pady=10)
        self.next_btn.pack_forget()
        self.master.answer_var.set(-1)

    def _on_submit(self):
        # here this code chunk handles the submit answer button 
        if self.master.answer_var.get() == -1:
            self.feedback_label.config(
                text="Please select an answer first.", fg="orange"
            )
            return

        correct, correct_index, explanation = self.master.submit_answer()
        question = self.master.questions[self.master.current_index]

        for rb in self.radio_buttons:
            rb.config(state="disabled")

        if correct:
            feedback = "Correct!"
            colour = "green"
        else:
            feedback = (
                f"Incorrect. "
                f"The correct answer was: {question.options[correct_index]}"
            )
            colour = "red"

        if explanation:
            feedback += f"\n{explanation}"

        self.feedback_label.config(text=feedback, fg=colour)
        self.submit_btn.pack_forget()
        self.next_btn.pack(pady=10)

    def _on_next(self):
        """Handle the Next button click."""
        self.master.next_question()


class ResultsFrame(tk.Frame):
    #The screen shown at the end of a quiz session

    def __init__(self, master):
        """Build the results screen widgets.

        Args:
            master: The parent QuizApp instance.
        """
        super().__init__(master, bg="#f0f4f8")
        self.master = master
        self._build()

    def _build(self):
        #Create and layout all widgets on the results screen
        tk.Label(
            self, text="Quiz Complete!",
            font=("Arial", 18, "bold"), bg="#f0f4f8", fg="#1F3864"
        ).pack(pady=(40, 10))

        self.score_label = tk.Label(
            self, text="", font=("Arial", 14), bg="#f0f4f8"
        )
        self.score_label.pack(pady=10)

        self.message_label = tk.Label(
            self, text="", font=("Arial", 11), bg="#f0f4f8", fg="#555555"
        )
        self.message_label.pack(pady=5)

        tk.Button(
            self, text="View All Results", font=("Arial", 11),
            bg="#2E75B6", fg="white", padx=15, pady=6,
            command=self._view_results
        ).pack(pady=10)

        tk.Button(
            self, text="Take Another Quiz", font=("Arial", 11),
            bg="#1F3864", fg="white", padx=15, pady=6,
            command=self._restart
        ).pack(pady=5)

    def show_results(self):
        #Updates the score display for the completed session
        score = self.master.score
        total = len(self.master.questions)
        percent = round((score / total) * 100)
        self.score_label.config(
            text=f"You scored {score} out of {total} ({percent}%)"
        )
        if percent >= 80:
            msg = "Excellent work!"
        elif percent >= 60:
            msg = "Good effort — review the questions you missed."
        else:
            msg = "Keep practising — you'll improve with each attempt."
        self.message_label.config(text=msg)

    def _view_results(self):
        #Open a new window showing all past results
        results = self.master.store.load_results()
        win = tk.Toplevel(self.master)
        win.title("All Results")
        win.geometry("500x400")

        tk.Label(
            win, text="All Quiz Results", font=("Arial", 13, "bold")
        ).pack(pady=10)

        text = tk.Text(win, font=("Arial", 10), padx=10, pady=10)
        text.pack(fill="both", expand=True, padx=10, pady=10)

        if not results:
            text.insert("end", "No results yet.")
        else:
            for r in results:
                line = (
                    f"{r['date']}  |  {r['name']}  |  "
                    f"{r['topic']}  |  "
                    f"{r['score']}/{r['total']}\n"
                )
                text.insert("end", line)

        text.config(state="disabled")

    def _restart(self):
        #Returns to the welcome screen for another attempt
        self.master.show_frame(WelcomeFrame)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()