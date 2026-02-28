import tkinter as tk
from tkinter import ttk , messagebox
from question_bank import QuestionBank
from result_store import ResultStore
from validators import validate_name, validate_topic

class QuizApp:
    # main Tkinter app for my MacroEconomic key formula's quiz

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macroeconomic knowledge quiz")
        self.root.geometry("650x500")
        self.root.resizable(False,False)

        self.bank =QuestionBank()
        self.store = ResultStore()

        self.user_name =""
        self.selected_topic =""
        self.questions = []
        self.current_index =0
        self.score =0
        self.answer_var = tk.IntVar(value=-1)
        # stretches frame to match window size
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

         # Create all frames
        self.welcome_frame = WelcomeFrame(self)
        self.quiz_frame = QuizFrame(self)
        self.results_frame = ResultsFrame(self)

        self.welcome_frame.grid(row=0, column=0, sticky="nsew" )
        self.quiz_frame.grid(row=0, column=0, sticky="nsew" )
        self.results_frame.grid(row=0, column=0, sticky="nsew" )
        self.show_frame(self.welcome_frame)


  

    def start_quiz(self, name, topic):
    # here this will validate inputs and begin a quiz session.
        name = self.name_entry.get()
        topic = self.topic_var.get()
        if not validate_name(name):
         messagebox.showerror("Error, please enter valid name")
         return
        if not validate_topic(topic, self.bank.get_topics()):
         messagebox.showerror("Error, please select valid topic")
         return

        self.user_name = name
        self.selected_topic = topic
        self.questions = self.bank.get_questions(topic=topic, count=5)
        self.current_index = 0
        self.score = 0
        self.show_frame(self.quiz_frame)
      

    def submit_answer(self):
        #Checks the selected answer and updates score.
        selected = self.answer_var.get()
        if selected == -1:
            messagebox.showwarning("Please select an answer")
            return
        question = self.questions[self.current_index]
        if question.is_correct(selected):
            self.score += 1
            messagebox.showinfo("Correct!", question.explanation)
        else: 
            messagebox.showinfo("Wrong", f" the correct answer was option{ question.correct_index+1}")

    def next_question(self):
        #go to the next question or finish the quiz
        self.current_index += 1
        self.answer_var.set(-1)

        if self.current_index < len(self.questions):
            self.quiz_frame.load_question()
        else:
            self.show_frame(self.results_frame)


class WelcomeFrame(tk.Frame):
#The starting screen where the user enters their name and picks a topic.

    def __init__(self, master):
        #Build the welcome screen widgets.
        super().__init__(master.root, bg="#f0f4f8")
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
        super().__init__(master.root)
        self.configure(bg= "#4a6886")
        self.master = master
        self._build()

    def _build(self):
        #Create and layout all widgets on the quiz screen
      self.question_label = tk.Label(self, text="", font=("Arial",13))
      self.question_label.pack(pady=10)

      self.answer_var = tk.IntVar()
      self.rb1 = tk.Radiobutton(self, text="", variable = self.answer_var, value=0)
      self.rb2 = tk.Radiobutton(self, text="", variable = self.answer_var, value=1)
      self.rb3 = tk.Radiobutton(self, text="", variable = self.answer_var, value=2)
      self.rb4 = tk.Radiobutton(self, text="", variable = self.answer_var, value=3)
      self.rb1.pack()
      self.rb2.pack()
      self.rb3.pack()
      self.rb4.pack()

      tk.Button(self,text ="submit", command =self._on_submit).pack(pady=10)


    def load_question(self):
        #here widgets will populate with the current questions 
     question = self.master.questions[self.master.current_index]
     self.question_label.config(text=question.text)
     self.rb1.config(text=question.options[0])
     self.rb2.config(text=question.options[1])
     self.rb3.config(text=question.options[2])
     self.rb4.config(text=question.options[3])


    def _on_submit(self):
        # here this code chunk handles the submit answer button 
        selected = self.master.answer_var.get()
        if selected == -1:
            messagebox.showwarning("please select answer")
            return
        question = self.master.questions[self.master.current_index]
        if question.is_correct(selected):
            messagebox.showinfo("Result","correct!!")
            self.master.score +=1
        else:
            messagebox.showinfo("Result",f"Wrong! the correct answer was: {question.options[question.correct_index]}")
            self.master.next_question()

    def _on_next(self):
       # this handles next button click so user can go to the next question
        self.master.next_question()


class ResultsFrame(tk.Frame):
    #The screen shown at the end of a quiz session
    def __init__(self,master):
        super().__init__(master.root)
        self.master = master
        tk.Label(self, text ="Quiz Complete!", font=("Arial",16)).pack(pady=20)

        self.score_label=tk.Label(self, text="", font=("Arial",13))
        self.score_label.pack(pady=10)

        self.message_label = tk.Label(self, text="")
        self.message_label.pack(pady=5)
        tk.Button(self, text =" View all results", command= self._view_results).pack(pady=10)
        tk.Button(self, text =" Try quiz again!", command= self._restart).pack(pady=5)


 

    def show_results(self):
       
       """ shows the final score on screen and depending
        on the outcomes a message will appear """
       
       score = self.master.score
       total = len(self.master.questions)
       percent = round((score / total) * 100)
    
       self.score_label.config(
            text=f"You scored {score} out of {total} ({percent}%)"
        )
        
       if percent >= 80:
            msg = "Excellent work!"
       elif percent >= 60:
            msg = "Good effort, you can review the questions you missed"
       else:
            msg = "Keep practising, you will improve!!"
       self.message_label.config(text=msg)

    def _view_results(self):
      # opens a new window with past results from the quiz
      results = self.master.store.load_results()
      win = tk.Toplevel(self.master)
      win.title("All results")

      tk.Label(win,text ="All quiz results", font =("Arial",13)).pack(pady=10)
      if not results:
          tk.Label(win, text="No results yet").pack()
      else:
          for r in results:
              tk.Label(win, text=f"{r['name']} -{r['score']}/{r['total']}").pack()

    def _restart(self):
        #Returns to the welcome screen for another attempt
        self.master.show_frame(WelcomeFrame)


app = QuizApp()
app.root.mainloop()