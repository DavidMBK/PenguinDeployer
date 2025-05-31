import pathlib
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import filedialog
from Services import ServicesLogic  # importa la classe logica

class ServicesUI(tk.Frame):
    def __init__(self, parent, controller, config_folder, service_manager=None):
        super().__init__(parent)
        self.controller = controller
        self.manager = service_manager if service_manager else ServicesLogic(config_folder)

        self.service_states = {}

        self.selected_service = None  # servizio selezionato

        # Top frame
        self.top_frame = tk.LabelFrame(self, padx=10, pady=10)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Bottom frame
        self.bottom_frame = tk.LabelFrame(self, padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Scrollable area
        self.container = tk.Frame(self.top_frame)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

        # Bottom controls
        self.search_entry = tk.Entry(self.bottom_frame)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        for label in ["Aggiungi", "Rimuovi", "Import", "Export"]:
            if label == "Aggiungi":
                cmd = self.open_service_popup
            elif label == "Rimuovi":
                cmd = self.remove_selected_service
            elif label == "Import":
                cmd = self.Import
            elif label == "Export":
                cmd = self.Export
            tk.Button(self.bottom_frame, text=label, command=cmd).pack(side=tk.LEFT, padx=2)


    def placeholder_action(self):
        messagebox.showinfo("Info", "Funzionalità non implementata.")

    def _update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self.canvas.yview_scroll(1, "units")

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")



    def add_service_row(self, pkg_name):
        row = tk.Frame(self.scrollable_frame, name=pkg_name)  # assegna un name usabile da winfo_name
        row.pack(fill=tk.X, expand=True)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=0)

        def on_select(event, name=pkg_name):
            self.selected_service = name
            # Evidenzia la riga selezionata
            for widget in self.scrollable_frame.winfo_children():
                widget.config(bg="#d9d9d9")
            row.config(bg="#bdbdbd")

        name_label = tk.Label(row, text=pkg_name, anchor="w")
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        name_label.bind("<Button-1>", on_select)
        row.bind("<Button-1>", on_select)

        toggle_btn = tk.Button(row)
        toggle_btn.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        toggle_btn.config(
            text=self._get_button_text(pkg_name),
            command=lambda name=pkg_name, btn=toggle_btn: self.toggle_install(name, btn)
        )


    def toggle_install(self, pkg_name, button):
        self.service_states[pkg_name] = not self.service_states[pkg_name]
        new_state = self.service_states[pkg_name]

        button.config(text=self._get_button_text(pkg_name))
        action = "Enable" if new_state else "Disable"

        if new_state:
            # Aggiunto alla lista to_enable
            if pkg_name not in self.manager.to_enable:
                self.manager.to_enable.append(pkg_name)
            # Rimosso dalla lista to_disable, se presente
            if pkg_name in self.manager.to_disable:
                self.manager.to_disable.remove(pkg_name)
        else:
            # Aggiunto alla lista to_disable
            if pkg_name not in self.manager.to_disable:
                self.manager.to_disable.append(pkg_name)
            # Rimosso dalla lista to_enable, se presente
            if pkg_name in self.manager.to_enable:
                self.manager.to_enable.remove(pkg_name)
        self.manager.debug()

      
    def _get_button_text(self, pkg_name):
        # Se False (non installato), testo bottone è "Install"
        return "Enable" if self.service_states.get(pkg_name, False) else "Disable"

    def open_service_popup(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input mancante", "Inserisci un nome servizio da cercare.")
            return

        try:
            matches = self.manager.find_service(query)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore nella ricerca: {e.stderr}")
            return

        if not matches:
            messagebox.showinfo("Nessun risultato", "Nessun servizio trovato.")
            return

        popup = tk.Toplevel(self)
        popup.title("Pacchetti trovati")
        popup.geometry("400x300")

        tk.Label(popup, text="Seleziona un servizio da installare").pack(pady=5)

        listbox = tk.Listbox(popup)
        for match in matches:
            listbox.insert(tk.END, match)
        listbox.pack(expand=True, fill=tk.BOTH, padx=10)

        def install_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Nessuna selezione", "Seleziona un servizio.")
                return

            pkg_name = listbox.get(selected[0])
            if pkg_name not in self.service_states:
                self.service_states[pkg_name] = True
                self.add_service_row(pkg_name)
                self.manager.to_enable.append(pkg_name)
            else:
                messagebox.showinfo("Esiste già", f"{pkg_name} è già presente.")

            popup.destroy()

        tk.Button(popup, text="Installa", command=install_selected).pack(pady=5)

    def remove_selected_service(self):
        pkg = self.selected_service
        if not pkg or pkg not in self.service_states:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un servizio.")
            return

        # Rimuovi widget dalla UI
        try:
            row = self.scrollable_frame.nametowidget(pkg)
            row.destroy()
        except KeyError:
            pass

        # Rimuovi dagli stati e dalle liste manager
        del self.service_states[pkg]
        self.manager.to_enable = [p for p in self.manager.to_enable if p != pkg]
        self.manager.to_disable = [p for p in self.manager.to_disable if p != pkg]

        self.selected_service = None

    
    def Export(self):
        filepath = filedialog.asksaveasfilename(
            title="Salva configurazione servizi",
            initialdir=os.path.join(os.path.dirname(__file__), "configs", "services"),
            defaultextension=".config",
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return  # Utente ha annullato

        self.manager.conf_export(pathlib.Path(filepath).name)
        messagebox.showinfo("Esportazione completata", f"Configurazione esportata in:\n{filepath}")
    
    def Import(self):
        filepath = filedialog.askopenfilename(
            title="Apri configurazione servizi",
            initialdir=os.path.join(os.path.dirname(__file__), "configs", "services"),
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return  # Utente ha annullato

        # Pulisci lo stato attuale
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.service_states.clear()
        self.manager.to_enable.clear()
        self.manager.to_disable.clear()
        self.selected_service = None

        # Importa la configurazione
        self.manager.conf_import_multiple([pathlib.Path(filepath).name])

        # Unisci i pacchetti da installare e disinstallare
        all_services = set(self.manager.to_enable + self.manager.to_disable)

        for pkg in all_services:
            is_installed = pkg in self.manager.to_enable
            self.service_states[pkg] = is_installed
            self.add_service_row(pkg)

        messagebox.showinfo("Importazione completata", f"Configurazione importata da:\n{filepath}")
