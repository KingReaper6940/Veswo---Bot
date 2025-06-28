import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
import json
import threading
import webbrowser
from PIL import Image, ImageTk
import io
import base64
import os
import sys
import subprocess

class AIAssistantApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Assistant")
        self.root.geometry("400x600")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create tabs
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Screen Analysis Tab
        self.screen_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.screen_tab, text='Screen')
        
        # Problem Solving Tab
        self.problem_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.problem_tab, text='Problem')
        
        # Essay Writing Tab
        self.essay_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.essay_tab, text='Essay')
        
        self.tab_control.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Setup Screen Analysis Tab
        self.setup_screen_tab()
        
        # Setup Problem Solving Tab
        self.setup_problem_tab()
        
        # Setup Essay Writing Tab
        self.setup_essay_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Start backend server in a separate thread
        self.start_backend_server()
        
    def setup_screen_tab(self):
        # Screen Analysis Controls
        ttk.Label(self.screen_tab, text="Screen Analysis").grid(row=0, column=0, pady=5)
        
        # Capture button
        self.capture_btn = ttk.Button(self.screen_tab, text="Capture Screen", command=self.capture_screen)
        self.capture_btn.grid(row=1, column=0, pady=5)
        
        # Result display
        self.screen_result = scrolledtext.ScrolledText(self.screen_tab, height=10)
        self.screen_result.grid(row=2, column=0, pady=5, sticky=(tk.W, tk.E))
        
    def setup_problem_tab(self):
        # Problem Solving Controls
        ttk.Label(self.problem_tab, text="Problem Solver").grid(row=0, column=0, pady=5)
        
        # Problem input
        self.problem_input = scrolledtext.ScrolledText(self.problem_tab, height=5)
        self.problem_input.grid(row=1, column=0, pady=5, sticky=(tk.W, tk.E))
        
        # Solve button
        self.solve_btn = ttk.Button(self.problem_tab, text="Solve Problem", command=self.solve_problem)
        self.solve_btn.grid(row=2, column=0, pady=5)
        
        # Result display
        self.problem_result = scrolledtext.ScrolledText(self.problem_tab, height=10)
        self.problem_result.grid(row=3, column=0, pady=5, sticky=(tk.W, tk.E))
        
    def setup_essay_tab(self):
        # Essay Writing Controls
        ttk.Label(self.essay_tab, text="Essay Writer").grid(row=0, column=0, pady=5)
        
        # Topic input
        ttk.Label(self.essay_tab, text="Topic:").grid(row=1, column=0, pady=5)
        self.topic_input = ttk.Entry(self.essay_tab, width=40)
        self.topic_input.grid(row=2, column=0, pady=5)
        
        # Length input
        ttk.Label(self.essay_tab, text="Length (words):").grid(row=3, column=0, pady=5)
        self.length_input = ttk.Entry(self.essay_tab, width=10)
        self.length_input.insert(0, "500")
        self.length_input.grid(row=4, column=0, pady=5)
        
        # Write button
        self.write_btn = ttk.Button(self.essay_tab, text="Write Essay", command=self.write_essay)
        self.write_btn.grid(row=5, column=0, pady=5)
        
        # Result display
        self.essay_result = scrolledtext.ScrolledText(self.essay_tab, height=10)
        self.essay_result.grid(row=6, column=0, pady=5, sticky=(tk.W, tk.E))
        
    def start_backend_server(self):
        def run_server():
            try:
                # Get the path to the Python executable in the virtual environment
                if sys.platform == "win32":
                    python_path = os.path.join("venv", "Scripts", "python.exe")
                else:
                    python_path = os.path.join("venv", "bin", "python")
                
                # Start the backend server
                subprocess.Popen([python_path, "backend/main.py"])
                self.status_var.set("Backend server started")
            except Exception as e:
                self.status_var.set(f"Error starting server: {str(e)}")
        
        # Start server in a separate thread
        threading.Thread(target=run_server, daemon=True).start()
        
    def capture_screen(self):
        try:
            response = requests.post("http://localhost:8000/analyze-screen")
            if response.status_code == 200:
                result = response.json()
                self.screen_result.delete(1.0, tk.END)
                self.screen_result.insert(tk.END, result.get("text", "No text found"))
                self.status_var.set("Screen captured successfully")
            else:
                self.status_var.set("Error capturing screen")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            
    def solve_problem(self):
        try:
            problem = self.problem_input.get(1.0, tk.END).strip()
            if not problem:
                self.status_var.set("Please enter a problem")
                return
                
            response = requests.post(
                "http://localhost:8000/solve-problem",
                json={"problem": problem}
            )
            
            if response.status_code == 200:
                result = response.json()
                self.problem_result.delete(1.0, tk.END)
                self.problem_result.insert(tk.END, result.get("solution", "No solution found"))
                self.status_var.set("Problem solved successfully")
            else:
                self.status_var.set("Error solving problem")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            
    def write_essay(self):
        try:
            topic = self.topic_input.get().strip()
            length = self.length_input.get().strip()
            
            if not topic:
                self.status_var.set("Please enter a topic")
                return
                
            try:
                length = int(length)
            except ValueError:
                self.status_var.set("Please enter a valid length")
                return
                
            response = requests.post(
                "http://localhost:8000/write-essay",
                json={
                    "topic": topic,
                    "length": length
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                self.essay_result.delete(1.0, tk.END)
                self.essay_result.insert(tk.END, result.get("essay", "No essay generated"))
                self.status_var.set("Essay written successfully")
            else:
                self.status_var.set("Error writing essay")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")

def main():
    root = tk.Tk()
    app = AIAssistantApp(root)
    
    # Position window in bottom-right corner
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 400
    window_height = 600
    x = screen_width - window_width - 20
    y = screen_height - window_height - 40
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 