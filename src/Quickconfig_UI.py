import tkinter as tk
from tkinter import messagebox, filedialog
import os
from functools import partial


class QuickConfigUI(tk.Frame):
    def __init__(self, parent, controller, quick_config_manager):
        super().__init__(parent)
        self.controller = controller
        self.manager = quick_config_manager
        
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titolo
        title_label = tk.Label(
            self.main_frame, 
            text="Configurazione Veloce",
            font=("Arial", 12, "bold")
        )
        title_label.pack(pady=(0, 15))
        
        # Tabella moduli-file
        self.module_entries = {}
        self.module_buttons = {}
        
        # Frame per la tabella
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(fill=tk.X, pady=5)
        
        # Intestazioni colonne
        tk.Label(table_frame, text="Modulo", width=15, anchor="w").grid(row=0, column=0, padx=5)
        tk.Label(table_frame, text="File", width=25, anchor="w").grid(row=0, column=1, padx=5)
        tk.Label(table_frame, text="Azione", width=10, anchor="w").grid(row=0, column=2, padx=5)
        
        # Righe della tabella per ogni modulo
        for i, module in enumerate(self.manager.modules, start=1):
            # Etichetta modulo
            module_label = tk.Label(table_frame, text=module.__class__.__name__, width=15, anchor="w")
            module_label.grid(row=i, column=0, padx=5, pady=2)
            
            # Campo di input per il file
            file_entry = tk.Entry(table_frame, width=25)
            file_entry.grid(row=i, column=1, padx=5, pady=2)
            self.module_entries[module] = file_entry
            
            # Pulsante per selezionare file
            btn_text = "Seleziona file" if not getattr(module, "is_multi_import", False) else "Seleziona file multipli"
            select_btn = tk.Button(
                table_frame, 
                text=btn_text, 
                width=15,
                command=partial(self.select_files, module)
            )
            select_btn.grid(row=i, column=2, padx=5, pady=2)
            self.module_buttons[module] = select_btn
        
        # Pulsanti nella parte inferiore
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=(15, 5))
        
        # Pulsanti allineati a destra
        inner_btn_frame = tk.Frame(btn_frame)
        inner_btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(
            inner_btn_frame, 
            text="apply", 
            width=10, 
            command=self.apply_configs
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            inner_btn_frame, 
            text="export", 
            width=10, 
            command=self.export_config
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            inner_btn_frame, 
            text="import", 
            width=10, 
            command=self.import_config
        ).pack(side=tk.LEFT, padx=5)
        
        # Barra di stato
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(
            self.main_frame, 
            textvariable=self.status_var, 
            bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
        
        self.update_status("Pronto")

    def update_status(self, message):
        self.status_var.set(message)
        self.update_idletasks()

    def select_files(self, module):
        """Seleziona file per un modulo specifico"""
        try:
            if module.is_multi_import:
                filepaths = filedialog.askopenfilenames(
                    title=f"Seleziona file per {module.__class__.__name__}",
                    filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
                )
                if filepaths:
                    # Prendi solo i nomi dei file (non i percorsi completi)
                    filenames = [os.path.basename(f) for f in filepaths]
                    self.module_entries[module].delete(0, tk.END)
                    self.module_entries[module].insert(0, "; ".join(filenames))
                    self.manager.selected_configs[module] = filenames
            else:
                filepath = filedialog.askopenfilename(
                    title=f"Seleziona file per {module.__class__.__name__}",
                    filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
                )
                if filepath:
                    filename = os.path.basename(filepath)
                    self.module_entries[module].delete(0, tk.END)
                    self.module_entries[module].insert(0, filename)
                    self.manager.selected_configs[module] = filename
            
            self.update_status(f"File selezionato per {module.__class__.__name__}")
        except Exception as e:
            self.update_status(f"Errore nella selezione file")
            messagebox.showerror("Errore", f"Selezione file fallita:\n{str(e)}")

    def apply_configs(self):
        """Applica le configurazioni selezionate"""
        try:
            # Prima verifichiamo che tutte le configurazioni siano selezionate
            for module in self.manager.modules:
                if not self.manager.selected_configs.get(module):
                    messagebox.showwarning("Attenzione", f"Selezionare un file di configurazione per {module.__class__.__name__}!")
                    return
            
            # Esegui l'applicazione delle configurazioni
            success = self.manager.apply_configs()
            
            if success:
                self.update_status("Configurazioni applicate con successo")
                messagebox.showinfo("Successo", "Tutte le configurazioni sono state applicate correttamente!")
                # Esegui anche la configurazione tramite il main controller
                self.controller.main.runconfig()
            else:
                self.update_status("Configurazioni mancanti")
                messagebox.showwarning("Attenzione", "Selezionare un file di configurazione per ogni modulo!")
        except Exception as e:
            self.update_status("Errore nell'applicazione")
            messagebox.showerror("Errore", f"Applicazione fallita:\n{str(e)}")

    def import_config(self):
        """Importa una configurazione da file"""
        try:
            filepath = filedialog.askopenfilename(
                title="Seleziona file configurazione da importare",
                filetypes=[("Archivio configurazione", "*.tar"), ("Tutti i file", "*.*")]
            )
            if not filepath:
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Importazione {filename} in corso...")
            
            self.manager.importconfig(filepath)
            
            # Dopo l'importazione, aggiorna l'interfaccia con i file importati
            for module in self.manager.modules:
                config = self.manager.selected_configs.get(module)
                if config:
                    if isinstance(config, list):  # File multipli
                        self.module_entries[module].delete(0, tk.END)
                        self.module_entries[module].insert(0, "; ".join(config))
                    else:  # Singolo file
                        self.module_entries[module].delete(0, tk.END)
                        self.module_entries[module].insert(0, config)
            
            self.update_status(f"Configurazione importata da {filename}")
            messagebox.showinfo("Successo", "Configurazione importata correttamente!")

        except Exception as e:
            self.update_status("Errore durante l'importazione")
            messagebox.showerror("Errore", f"Importazione fallita:\n{str(e)}")

    def export_config(self):
        """Esporta la configurazione corrente"""
        try:
            # Prima verifichiamo che tutte le configurazioni siano selezionate
            for module in self.manager.modules:
                if not self.manager.selected_configs.get(module):
                    messagebox.showwarning("Attenzione", f"Selezionare un file di configurazione per {module.__class__.__name__} prima di esportare!")
                    return

            filepath = filedialog.asksaveasfilename(
                title="Salva configurazione",
                defaultextension=".tar",
                filetypes=[("Archivio configurazione", "*.tar"), ("Tutti i file", "*.*")]
            )
            if not filepath:
                return

            filename = os.path.basename(filepath)
            self.update_status(f"Esportazione {filename} in corso...")
            
            self.manager.exportconfig(filepath)
            
            self.update_status(f"Configurazione esportata in {filename}")
            messagebox.showinfo("Successo", "Configurazione esportata correttamente!")

        except Exception as e:
            self.update_status("Errore durante l'esportazione")
            messagebox.showerror("Errore", f"Esportazione fallita:\n{str(e)}")