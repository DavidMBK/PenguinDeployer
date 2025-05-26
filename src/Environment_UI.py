import tkinter as tk
from tkinter import messagebox
from environment import EnvironmentLogic

class EnvironmentUI(tk.Frame):
    def __init__(self, parent, controller, environment):
        super().__init__(parent)
        self.controller = controller

        self.manager = environment
        
        # Main container frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame per le 4 entry di testo
        self.entries_frame = tk.Frame(self.main_frame)
        self.entries_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Creazione delle 4 entry
        self.entries = []
        for i in range(4):
            frame = tk.Frame(self.entries_frame)
            frame.pack(fill=tk.X, pady=2)
            
            label = tk.Label(frame, text=f"Testo {i+1}:", width=8, anchor="w")
            label.pack(side=tk.LEFT)
            
            entry = tk.Entry(frame)
            entry.pack(fill=tk.X, expand=True, padx=5)
            self.entries.append(entry)
        
        # Checkbox per gconfigs
        self.gconfigs_var = tk.BooleanVar()
        self.gconfigs_check = tk.Checkbutton(
            self.main_frame, 
            text="gconfigs", 
            variable=self.gconfigs_var,
            onvalue=True, 
            offvalue=False
        )
        self.gconfigs_check.pack(anchor="w", padx=5, pady=(10, 0))
        
        # Area di testo per la spiegazione
        self.explanation_frame = tk.LabelFrame(self.main_frame, text="Spiegazione", padx=5, pady=5)
        self.explanation_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.explanation_text = tk.Text(self.explanation_frame, wrap=tk.WORD, height=4)
        self.explanation_text.pack(fill=tk.BOTH, expand=True)
        self.explanation_text.insert(tk.END, "Spiegazione a cosa serve la checkbox gconfigs...")
        self.explanation_text.config(state=tk.DISABLED)  # Make it read-only
        
        # Pulsanti Import/Export
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        tk.Button(self.button_frame, text="Import", command=self.import_action).pack(side=tk.LEFT, padx=5)
        tk.Button(self.button_frame, text="Export", command=self.export_action).pack(side=tk.LEFT, padx=5)
    
    def import_action(self):
        messagebox.showinfo("Import", "Funzionalità di import")
    
    def export_action(self):
        messagebox.showinfo("Export", "Funzionalità di export")
