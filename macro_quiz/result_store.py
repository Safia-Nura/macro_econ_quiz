import csv
import os
from datetime import datetime
class ResultStore:
    #handles reading/writing quiz results to a CSV file
    HEADERS =["name", "date", "topic","score","total"]
    def __init__(self, filepath:str ="results.csv"):
        #sets up the class with filepath
        self.filepath = filepath
        self._ensure_file_exists()
    def _ensure_file_exists(self) -> None:
        #creates CSV file with headers
        if not os.path.exists(self.filepath):
            try:
                with open(self.filepath, "w", newline ="") as f:
                    writer = csv.DictWriter(f, fieldnames= self.HEADERS)
                    writer.writeheader()
            except OSError as e:
                raise OSError (f"Couldn't create results file: {e}")
    def append_results( self,name: str, topic: str, score:int, total: int) -> None:
        #saves single quiz result as  CSV file
        row = {
            "name": name,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "topic": topic,
            "score": score,
            "total": total
        }
        try:
            with open(self.filepath,"a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames= self.HEADERS)
                writer.writerow(row)
        except OSError as e:
            raise OSError(f"Couldn't write result:{e}-")
    def load_results(self) ->list:
        #loads results from CSV file
        try:
         with open(self.filepath, "r", newline ="") as f:
            reader = csv.DictReader(f)
            return list(reader)
        except (OSError, csv.ERROR):
         return 