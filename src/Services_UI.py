import pathlib
import os
import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import filedialog

from Services import ServicesLogic  # Importa la logica di gestione dei servizi

# Classe UI per la gestione dei servizi
class ServicesUI(tk.Frame):
    def __init__(self, parent, controller, config_folder, service_manager=None):
        super().__init__(parent)
        self.controller = controller
        # Usa un service manager esistente o crea uno nuovo
        self.manager = service_manager if service_manager else ServicesLogic(config_folder)

        self.service_states = {}  # Stato attuale dei servizi (abilitato/disabilitato)
        self.selected_service = None  # Servizio selezionato nella UI

        # Frame superiore (elenco servizi)
        self.top_frame = tk.LabelFrame(self, padx=10, pady=10)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Frame inferiore (barra comandi)
        self.bottom_frame = tk.LabelFrame(self, padx=10, pady=10)
        self.bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Area scrollabile nel frame superiore
        self.container = tk.Frame(self.top_frame)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.container)
        self.scrollbar = tk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Eventi per lo scroll dinamico
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

        # Entry di ricerca + bottoni
        self.search_entry = tk.Entry(self.bottom_frame)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        for label in ["Aggiungi", "Rimuovi", "Importa", "Exporta"]:
            if label == "Aggiungi":
                cmd = self.open_service_popup
            elif label == "Rimuovi":
                cmd = self.remove_selected_service
            elif label == "Importa":
                cmd = self.Import
            elif label == "Exporta":
                cmd = self.Export
            tk.Button(self.bottom_frame, text=label, command=cmd).pack(side=tk.LEFT, padx=2)

    # Scroll dinamico con mousewheel
    def _update_scroll_region(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfig(self.window_id, width=event.width)

    def _on_mousewheel(self, event):
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif event.num == 4:  # Scroll su (Linux)
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5:  # Scroll giù (Linux)
            self.canvas.yview_scroll(1, "units")

    def _bind_to_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_from_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    # Aggiunge una riga nella UI per un pacchetto/servizio
    def add_service_row(self, pkg_name):
        row = tk.Frame(self.scrollable_frame, name=pkg_name)
        row.pack(fill=tk.X, expand=True)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=0)

        # Evento di selezione
        def on_select(event, name=pkg_name):
            self.selected_service = name
            # Evidenziazione visiva
            for widget in self.scrollable_frame.winfo_children():
                widget.config(bg="#d9d9d9")
            row.config(bg="#bdbdbd")

        # Etichetta con nome pacchetto
        name_label = tk.Label(row, text=pkg_name, anchor="w")
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        name_label.bind("<Button-1>", on_select)
        row.bind("<Button-1>", on_select)

        # Bottone per toggle (Enable/Disable)
        toggle_btn = tk.Button(row)
        toggle_btn.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        toggle_btn.config(
            text=self._get_button_text(pkg_name),
            command=lambda name=pkg_name, btn=toggle_btn: self.toggle_install(name, btn)
        )

    # Attiva/disattiva un servizio
    def toggle_install(self, pkg_name, button):
        self.service_states[pkg_name] = not self.service_states[pkg_name]
        new_state = self.service_states[pkg_name]

        button.config(text=self._get_button_text(pkg_name))

        if new_state:
            if pkg_name not in self.manager.to_enable:
                self.manager.to_enable.append(pkg_name)
            if pkg_name in self.manager.to_disable:
                self.manager.to_disable.remove(pkg_name)
        else:
            if pkg_name not in self.manager.to_disable:
                self.manager.to_disable.append(pkg_name)
            if pkg_name in self.manager.to_enable:
                self.manager.to_enable.remove(pkg_name)

        self.manager.debug()  # Stampa stato per debug

    # Testo del bottone in base allo stato del servizio
    def _get_button_text(self, pkg_name):
        return "Enable" if self.service_states.get(pkg_name, False) else "Disable"

    # Finestra popup per cercare e installare servizi
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

        # Popup con risultati
        popup = tk.Toplevel(self)
        popup.title("Pacchetti trovati")
        popup.geometry("400x300")

        tk.Label(popup, text="Seleziona un servizio da aggiungere").pack(pady=5)
        listbox = tk.Listbox(popup)
        for match in matches:
            listbox.insert(tk.END, match)
        listbox.pack(expand=True, fill=tk.BOTH, padx=10)

        # Bottone per installazione
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

        tk.Button(popup, text="Aggiungi", command=install_selected).pack(pady=5)

    # Rimuove il servizio selezionato
    def remove_selected_service(self):
        pkg = self.selected_service
        if not pkg or pkg not in self.service_states:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un servizio.")
            return

        try:
            row = self.scrollable_frame.nametowidget(pkg)
            row.destroy()
        except KeyError:
            pass

        del self.service_states[pkg]
        self.manager.to_enable = [p for p in self.manager.to_enable if p != pkg]
        self.manager.to_disable = [p for p in self.manager.to_disable if p != pkg]

        self.selected_service = None

    # Esporta configurazione corrente su file
    def Export(self):
        filepath = filedialog.asksaveasfilename(
            title="Salva configurazione servizi",
            initialdir=os.path.join(os.path.dirname(__file__), "configs", "services"),
            defaultextension=".config",
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return

        self.manager.conf_export(pathlib.Path(filepath).name)
        messagebox.showinfo("Esportazione completata", f"Configurazione esportata in:\n{filepath}")

    # Importa una configurazione da file
    def Import(self):
        filepath = filedialog.askopenfilename(
            title="Apri configurazione servizi",
            initialdir=os.path.join(os.path.dirname(__file__), "configs", "services"),
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return

        # Pulisce lo stato attuale
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.service_states.clear()
        self.manager.to_enable.clear()
        self.manager.to_disable.clear()
        self.selected_service = None

        # Importa dal file selezionato
        self.manager.conf_import_multiple([pathlib.Path(filepath).name])
        all_services = set(self.manager.to_enable + self.manager.to_disable)

        for pkg in all_services:
            is_installed = pkg in self.manager.to_enable
            self.service_states[pkg] = is_installed
            self.add_service_row(pkg)

        messagebox.showinfo("Importazione completata", f"Configurazione importata da:\n{filepath}")

    # Ricarica la UI dai dati nel manager
    def refresh_from_manager(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.service_states.clear()
        self.selected_service = None

        all_services = set(self.manager.to_enable + self.manager.to_disable)

        for pkg in all_services:
            is_installed = pkg in self.manager.to_enable
            self.service_states[pkg] = is_installed
            self.add_service_row(pkg)
