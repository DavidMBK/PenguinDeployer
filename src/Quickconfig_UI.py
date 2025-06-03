import os
import pathlib
import tarfile
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from functools import partial

# Classe principale per l'interfaccia utente della configurazione rapida
class QuickConfigUI(tk.Frame):
    def __init__(self, parent, controller, quick_config_manager):
        super().__init__(parent)
        self.controller = controller
        self.manager = quick_config_manager

        # Set per tenere traccia delle selezioni
        self.selected_packages = set()
        self.selected_services = set()
        self.selected_env = None
        self.config_path = "src/configs"  # Percorso delle configurazioni

        self.current_section = "packages"  # Sezione mostrata all'avvio

        self._setup_ui()                 # Inizializza la UI
        self.load_config_structure()     # Carica file di configurazione
        self.show_packages()             # Mostra pacchetti all'avvio

    # Crea i componenti dell'interfaccia
    def _setup_ui(self):
        top_frame = tk.Frame(self)
        top_frame.pack(fill=tk.X, padx=5, pady=5)

        # Bottoni di navigazione
        tk.Button(top_frame, text="Packages", command=self.show_packages).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Services", command=self.show_services).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Environment", command=self.show_environment).pack(side=tk.LEFT, padx=5)

        # Area principale per la visualizzazione dei contenuti
        self.main_frame = tk.Frame(self, bd=2, relief=tk.GROOVE)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Barra inferiore con i comandi
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=5)

        tk.Button(bottom_frame, text="Import Config", command=self.import_config).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Export Config", command=self.export_config).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="Apply Config", command=self.apply_configs).pack(side=tk.RIGHT, padx=5)

        # Barra di stato inferiore
        self.status_var = tk.StringVar()
        status_bar = tk.Label(self, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(fill=tk.X)

    # Aggiorna il messaggio nella barra di stato
    def update_status(self, msg):
        self.status_var.set(msg)
        self.update_idletasks()

    # Pulisce la vista principale
    def clear_main_frame(self):
        for w in self.main_frame.winfo_children():
            w.destroy()

    # Carica tutti i file .config dalle sottodirectory
    def load_config_structure(self):
        def list_configs(subfolder):
            path = os.path.join(self.config_path, subfolder)
            if os.path.exists(path):
                return sorted([f for f in os.listdir(path) if f.endswith('.config')])
            return []

        self.packages_configs = list_configs("packages")
        self.services_configs = list_configs("services")
        self.env_configs = list_configs("environment")

    # Crea una lista di checkbox scrollabile per selezionare configurazioni
    def _create_scrollable_checkbox_list(self, items, selected_set, update_callback):
        frame = tk.Frame(self.main_frame)
        frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        vars_dict = {}
        for cfg in items:
            var = tk.BooleanVar(value=(cfg in selected_set))
            cb = tk.Checkbutton(scrollable_frame, text=cfg, variable=var,
                                command=partial(update_callback, cfg, var))
            cb.pack(anchor="w", padx=5, pady=2)
            vars_dict[cfg] = var
        return vars_dict

    # Mostra configurazioni di pacchetti
    def show_packages(self):
        self.current_section = "packages"
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Select Packages:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0,5))

        if not self.packages_configs:
            tk.Label(self.main_frame, text="No package configs found.", fg="red").pack()
            self.package_vars = {}
            return

        self.package_vars = self._create_scrollable_checkbox_list(
            self.packages_configs, self.selected_packages, self.update_package_selection
        )

    # Mostra configurazioni di servizi
    def show_services(self):
        self.current_section = "services"
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Select Services:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0,5))

        if not self.services_configs:
            tk.Label(self.main_frame, text="No service configs found.", fg="red").pack()
            self.service_vars = {}
            return

        self.service_vars = self._create_scrollable_checkbox_list(
            self.services_configs, self.selected_services, self.update_service_selection
        )

    # Mostra configurazioni dell'ambiente (radio button)
    def show_environment(self):
        self.current_section = "environment"
        self.clear_main_frame()
        tk.Label(self.main_frame, text="Select Environment:", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0,5))

        if not self.env_configs:
            tk.Label(self.main_frame, text="No environment configs found.", fg="red").pack()
            self.env_var = tk.StringVar()
            self.selected_env = None
            return

        if self.selected_env not in self.env_configs:
            self.selected_env = None

        self.env_var = tk.StringVar(value=self.selected_env if self.selected_env else "")
        for cfg in self.env_configs:
            rb = tk.Radiobutton(self.main_frame, text=cfg, variable=self.env_var, value=cfg,
                                command=self.update_env_selection)
            rb.pack(anchor="w", padx=5, pady=2)

    # Aggiorna selezione pacchetti
    def update_package_selection(self, config, var):
        if var.get():
            self.selected_packages.add(config)
        else:
            self.selected_packages.discard(config)
        self.update_status(f"Selected packages: {len(self.selected_packages)}")

    # Aggiorna selezione servizi
    def update_service_selection(self, config, var):
        if var.get():
            self.selected_services.add(config)
        else:
            self.selected_services.discard(config)
        self.update_status(f"Selected services: {len(self.selected_services)}")

    # Aggiorna selezione ambiente
    def update_env_selection(self):
        self.selected_env = self.env_var.get()
        self.update_status(f"Selected environment: {self.selected_env}")

    # Importa configurazione da file tar.gz
    def import_config(self):
        filepath = filedialog.askopenfilename(
            title="Import Configuration",
            filetypes=[("Tar archives", "*.tar.gz")]
        )
        if not filepath:
            return  # Utente ha annullato

        try:
            self.manager.importconfig(filepath)
            self.update_status("Configuration imported successfully")
            messagebox.showinfo("Success", "Configuration imported successfully!")
            self.load_config_structure()
            self.refresh_current_view()
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import configuration:\n{e}")
            self.update_status("Import failed")

    # Ricarica la vista attiva corrente
    def refresh_current_view(self):
        if hasattr(self, "current_section"):
            if self.current_section == "packages":
                self.show_packages()
            elif self.current_section == "services":
                self.show_services()
            elif self.current_section == "environment":
                self.show_environment()
        else:
            self.show_packages()

    # Esporta configurazione in file .tar.gz
    def export_config(self):
        filepath = filedialog.asksaveasfilename(
            title="Export Configuration",
            defaultextension=".tar.gz",
            filetypes=[("Tar archives", "*.tar.gz")]
        )
        if not filepath:
            return

        self.manager.exportconfig(filepath, pathlib.Path(filepath).name)

    # Applica le configurazioni selezionate
    def apply_configs(self):
        selected_configs = {
            "packages": list(self.selected_packages),
            "services": list(self.selected_services),
            "environment": self.selected_env
        }

        # Aggiorna le configurazioni selezionate nel manager
        for module in self.manager.selected_configs.keys():
            self.manager.selected_configs[module] = selected_configs[module.mname]

        self.manager.apply_configs()
