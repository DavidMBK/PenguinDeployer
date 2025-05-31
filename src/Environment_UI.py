import tkinter as tk
from tkinter import messagebox, filedialog
import os
from environment import EnvironmentLogic

class EnvironmentUI(tk.Frame):
    def __init__(self, parent, controller, config_folder):

        super().__init__(parent)
        self.controller = controller
        self.manager = EnvironmentLogic(config_folder)
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.fields = [
            ("Shell:", "shell"),
            ("Editor:", "editor"), 
            ("Prompt:", "prompt"),
            ("Hostname:", "hostname")
        ]
        
        self.entries = {}
        
        for label_text, field_name in self.fields:
            frame = tk.Frame(self.main_frame)
            frame.pack(fill=tk.X, pady=5)
            tk.Label(frame, text=label_text, width=10, anchor="w").pack(side=tk.LEFT)
            entry = tk.Entry(frame)
            entry.pack(fill=tk.X, expand=True, padx=5)
            self.entries[field_name] = entry
        
        self.gconfigs_var = tk.BooleanVar()
        self.gconfigs_check = tk.Checkbutton(
            self.main_frame,
            text="Includi configurazioni generali del sistema (gconfigs)",
            variable=self.gconfigs_var
        )
        self.gconfigs_check.pack(anchor="w", pady=10)

        info_frame = tk.Frame(self.main_frame)
        info_frame.pack(fill=tk.X, pady=(2, 10), padx=5)

        info_label = tk.Label(
            info_frame,
            text="Se selezionato, include anche le configurazioni generali di sistema (gconfigs)\n"
                "come file bashrc, profili di sistema, configurazioni di terminale ecc.",
            font=("Arial", 9),
            justify="left",
            fg="gray30",
            wraplength=600
        )
        info_label.pack(anchor="w")
        
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="Importa", command=self.import_config).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Esporta", command=self.export_config).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Aggiorna", command=self.refresh_from_manager).pack(side=tk.LEFT, padx=5)
        
        
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10,0))

        
        
        self.update_status("Pronto")

    def update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()

    def get_current_values(self):
        return {
            "shell": self.entries["shell"].get(),
            "editor": self.entries["editor"].get(),
            "prompt": self.entries["prompt"].get(),
            "hostname": self.entries["hostname"].get(),
            "gconfigs": self.gconfigs_var.get()
        }

    def set_current_values(self, values):
        for key in self.entries:
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, values.get(key, ""))
        self.gconfigs_var.set(values.get("gconfigs", False))

    def import_config(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Seleziona file configurazione",
                initialdir=os.path.join(os.path.dirname(__file__), "configs", "environment"),
                filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
            )
            if not filepath:
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Importazione {filename} in corso...")

            self.manager.conf_import(filepath)

            self.set_current_values({
                "shell": self.manager.shell,
                "editor": self.manager.editor,
                "prompt": self.manager.prompt,
                "hostname": self.manager.hostname,
                "gconfigs": self.manager.gconfigs
            })

            self.update_status(f"Configurazione importata da {filename}")
            messagebox.showinfo("Successo", "Configurazione importata correttamente!")

        except Exception as e:
            self.update_status("Errore durante l'importazione")
            messagebox.showerror("Errore", f"Importazione fallita:\n{str(e)}")

    def export_config(self):
        try:
            current_values = self.get_current_values()

            filepath = filedialog.asksaveasfilename(
                title="Salva configurazione",
                initialdir=os.path.join(os.path.dirname(__file__), "configs", "environment"),
                defaultextension=".config",
                filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
            )
            if not filepath:
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Esportazione {filename} in corso...")

            self.manager.shell = current_values["shell"]
            self.manager.editor = current_values["editor"]
            self.manager.prompt = current_values["prompt"]
            self.manager.hostname = current_values["hostname"]
            self.manager.gconfigs = current_values["gconfigs"]

            self.manager.conf_export(filepath)

            self.update_status(f"Configurazione esportata in {filename}")
            messagebox.showinfo("Successo", "Configurazione esportata correttamente!")

        except Exception as e:
            self.update_status("Errore durante l'esportazione")
            messagebox.showerror("Errore", f"Esportazione fallita:\n{str(e)}")

    def refresh_from_manager(self):
        self.set_current_values({
            "shell": self.manager.shell,
            "editor": self.manager.editor,
            "prompt": self.manager.prompt,
            "hostname": self.manager.hostname,
            "gconfigs": self.manager.gconfigs
        })
        print(self.manager.shell)
        print("TEST")