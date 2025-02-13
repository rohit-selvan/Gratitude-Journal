import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3


conn = sqlite3.connect("gratitude_journal.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS journal (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        entry TEXT NOT NULL
    )
''')
conn.commit()

class GratitudeJournal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gratitude Journal")
        self.geometry("700x600")
        self.configure(bg="#d4e6f1")  
        self.create_widgets()

    def create_widgets(self):
        
        tk.Label(self, text="Gratitude Journal", font=("Verdana", 28, "bold"), bg="#ffe4e1", fg="#2e4053").pack(pady=20)
        
        
        tk.Label(self, text="Select Date:", font=("Verdana", 12), bg="#ffe4e1").pack(pady=5)
        self.calendar = Calendar(self, font=("Verdana", 12), background="#a9cce3", foreground="black", selectmode="day")
        self.calendar.pack(pady=10)
        
        
        tk.Label(self, text="Write Your Gratitude Entry:", font=("Verdana", 12), bg="#ffe4e1").pack(pady=5)
        self.entry_text = tk.Text(self, font=("Verdana", 12), height=10, width=60)
        self.entry_text.pack(pady=10)
        
        button_frame = tk.Frame(self, bg="#ffe4e1")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Save Entry", command=self.save_entry, font=("Verdana", 14), bg="#85c1e9", fg="white", width=12).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="View Entries", command=self.view_entries, font=("Verdana", 14), bg="#aed6f1", fg="white", width=12).grid(row=0, column=1, padx=10)
        
        
        self.result_text = tk.Text(self, font=("Verdana", 12), height=10, width=80, state=tk.DISABLED, wrap=tk.WORD)
        self.result_text.pack(pady=10)

    def save_entry(self):
        date = self.calendar.get_date()
        entry = self.entry_text.get("1.0", tk.END).strip()
        
        if not entry:
            messagebox.showwarning("Input Error", "Please write something in your entry.")
            return
        
        cursor.execute("INSERT INTO journal (date, entry) VALUES (?, ?)", (date, entry))
        conn.commit()
        messagebox.showinfo("Success", "Your gratitude entry has been saved!")
        self.entry_text.delete("1.0", tk.END)

    def view_entries(self):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        
        cursor.execute("SELECT date, entry FROM journal ORDER BY date DESC")
        entries = cursor.fetchall()
        
        if not entries:
            self.result_text.insert(tk.END, "No entries found.")
        else:
            for date, entry in entries:
                self.result_text.insert(tk.END, f"Date: {date}\nEntry: {entry}\n{'-'*50}\n\n")
        
        self.result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    app = GratitudeJournal()
    app.mainloop()


conn.close()
