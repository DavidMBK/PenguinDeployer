import tkinter as tk
from tkinter import messagebox, filedialog
import os
from environment import EnvironmentLogic  # Importa la logica dell'ambiente da un modulo esterno

class EnvironmentUI(tk.Frame):
    def __init__(self, parent, controller, config_folder, env_manager=None):
        super().__init__(parent)
        self.controller = controller
        # Usa l'istanza passata di EnvironmentLogic o ne crea una nuova
        self.manager = env_manager if env_manager else EnvironmentLogic(config_folder)
        
        # Frame principale della UI dove si aggiungono i widget
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Definisce i campi di configurazione con etichetta e nome interno
        self.fields = [
            ("Shell:", "shell"),
            ("Editor:", "editor"), 
            ("Prompt:", "prompt"),
            ("Hostname:", "hostname")
        ]
        
        self.entries = {}  # Dizionario per salvare i widget Entry
        
        # Crea un campo di input per ogni elemento in self.fields (Quindi Shell, Editor, Prompt, Hostname)
        for label_text, field_name in self.fields:
            frame = tk.Frame(self.main_frame)
            frame.pack(fill=tk.X, pady=5)
            # Label descrittiva a sinistra di ogni campo
            tk.Label(frame, text=label_text, width=10, anchor="w").pack(side=tk.LEFT) # Imposta l'ancoraggio a sinistra
            # Entry per l'inserimento del valore
            entry = tk.Entry(frame)
            entry.pack(fill=tk.X, expand=True, padx=5)
            self.entries[field_name] = entry
        
        # Checkbox per includere configurazioni generali di sistema
        self.gconfigs_var = tk.BooleanVar()
        self.gconfigs_check = tk.Checkbutton(
            self.main_frame,
            text="Includi configurazioni generali del sistema (gconfigs)",
            variable=self.gconfigs_var
        )
        self.gconfigs_check.pack(anchor="w", pady=10)

        # Frame per la spiegazione testuale sotto la checkbox
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
        
        # Frame con i pulsanti Importa/Esporta
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        tk.Button(btn_frame, text="Importa", command=self.import_config).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Esporta", command=self.export_config).pack(side=tk.LEFT, padx=5)
        
        # Barra di stato in basso per mostrare messaggi all'utente
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.main_frame, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, pady=(10,0))

        # Aggiorna i campi con i valori correnti della configurazione all'avvio
        self.refresh_from_manager()
        self.update_status("Pronto")

    # Metodo per aggiornare il messaggio nella barra di stato
    def update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()  # Forza aggiornamento UI immediato

    # Raccoglie i valori correnti dai campi di input e checkbox
    def get_current_values(self):
        return {
            "shell": self.entries["shell"].get(),
            "editor": self.entries["editor"].get(),
            "prompt": self.entries["prompt"].get(),
            "hostname": self.entries["hostname"].get(),
            "gconfigs": self.gconfigs_var.get()
        }

    # Imposta i valori nei campi di input e checkbox da un dizionario
    def set_current_values(self, values):
        for key in self.entries:
            self.entries[key].delete(0, tk.END)  # Pulisce il campo
            self.entries[key].insert(0, values.get(key, ""))  # Inserisce il nuovo valore
        self.gconfigs_var.set(values.get("gconfigs", False))

    # Funzione per importare una configurazione da file
    def import_config(self):
        try:
            filepath = filedialog.askopenfilename(
                title="Seleziona file configurazione",
                initialdir=os.path.join(os.path.dirname(__file__), "configs", "environment"),
                filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
            )
            if not filepath:  # Se l'utente annulla la selezione
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Importazione {filename} in corso...")

            # Usa il manager per importare la configurazione dal file selezionato
            self.manager.conf_import(filepath)

            # Aggiorna la UI con i nuovi valori importati
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

    # Funzione per esportare la configurazione corrente su file
    def export_config(self):
        try:
            current_values = self.get_current_values()

            filepath = filedialog.asksaveasfilename(
                title="Salva configurazione",
                initialdir=os.path.join(os.path.dirname(__file__), "configs", "environment"), # Cartella di default
                defaultextension=".config",
                filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
            )
            if not filepath:  # Se l'utente annulla il salvataggio
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Esportazione {filename} in corso...")

            # Aggiorna il manager con i valori correnti per esportarli
            self.manager.shell = current_values["shell"]
            self.manager.editor = current_values["editor"]
            self.manager.prompt = current_values["prompt"]
            self.manager.hostname = current_values["hostname"]
            self.manager.gconfigs = current_values["gconfigs"]

            # Chiama il metodo di esportazione del manager
            self.manager.conf_export(filepath)

            self.update_status(f"Configurazione esportata in {filename}")
            messagebox.showinfo("Successo", "Configurazione esportata correttamente!")

        except Exception as e:
            self.update_status("Errore durante l'esportazione")
            messagebox.showerror("Errore", f"Esportazione fallita:\n{str(e)}")

    # Aggiorna i campi di input UI con i valori attualmente nel manager
    def refresh_from_manager(self):
        self.set_current_values({
            "shell": self.manager.shell,
            "editor": self.manager.editor,
            "prompt": self.manager.prompt,
            "hostname": self.manager.hostname,
            "gconfigs": self.manager.gconfigs
        })
