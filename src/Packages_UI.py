import tkinter as tk
from tkinter import messagebox
import subprocess
from tkinter import filedialog


from Packages import PackagesLogic  # importa la classe logica

class PackagesUI(tk.Frame):
    def __init__(self, parent, controller, pack):
        super().__init__(parent)
        self.controller = controller

        self.package_states = {}
        self.manager = pack
        self.selected_package = None  # Pacchetto selezionato

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
                cmd = self.open_package_popup
            elif label == "Rimuovi":
                cmd = self.remove_selected_package
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



    def add_package_row(self, pkg_name):
        row = tk.Frame(self.scrollable_frame, name=pkg_name)
        row.pack(fill=tk.X, expand=True)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=0)

        def on_select(event, name=pkg_name):
            self.selected_package = name
            # Evidenzia la riga selezionata
            for widget in self.scrollable_frame.winfo_children():
                widget.config(bg="#d9d9d9")
            row.config(bg="#bdbdbd")  # colore evidenziato

        name_label = tk.Label(row, text=pkg_name, anchor="w")
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)
        name_label.bind("<Button-1>", on_select)
        row.bind("<Button-1>", on_select)

        toggle_btn = tk.Button(
            row,
            text=self._get_button_text(pkg_name),
            command=lambda name=pkg_name, btn=None: self.toggle_install(name, btn)
        )
        toggle_btn.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        toggle_btn.config(command=lambda name=pkg_name, btn=toggle_btn: self.toggle_install(name, btn))

    def toggle_install(self, pkg_name, button):
        self.package_states[pkg_name] = not self.package_states[pkg_name]
        new_state = self.package_states[pkg_name]

        button.config(text=self._get_button_text(pkg_name))
        action = "install" if new_state else "uninstall"

        if new_state:
            # Aggiunto alla lista to_install
            if pkg_name not in self.manager.to_install:
                self.manager.to_install.append(pkg_name)
            # Rimosso dalla lista to_uninstall, se presente
            if pkg_name in self.manager.to_uninstall:
                self.manager.to_uninstall.remove(pkg_name)
        else:
            # Aggiunto alla lista to_uninstall
            if pkg_name not in self.manager.to_uninstall:
                self.manager.to_uninstall.append(pkg_name)
            # Rimosso dalla lista to_install, se presente
            if pkg_name in self.manager.to_install:
                self.manager.to_install.remove(pkg_name)

        # DEBUG:
        self.manager.prova()

    def _get_button_text(self, pkg_name):
        # Se False (non installato), testo bottone è "Install"
        return "Install" if self.package_states.get(pkg_name, False) else "Uninstall"

    def open_package_popup(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input mancante", "Inserisci un nome pacchetto da cercare.")
            return

        try:
            matches = self.manager.find_package(query)

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore nella ricerca: {e.stderr}")
            return

        if not matches:
            messagebox.showinfo("Nessun risultato", "Nessun pacchetto trovato.")
            return

        popup = tk.Toplevel(self)
        popup.title("Pacchetti trovati")
        popup.geometry("400x300")

        tk.Label(popup, text="Seleziona un pacchetto da installare").pack(pady=5)

        listbox = tk.Listbox(popup)
        for match in matches:
            listbox.insert(tk.END, match)
        listbox.pack(expand=True, fill=tk.BOTH, padx=10)

        def install_selected():
            selected = listbox.curselection()
            if not selected:
                messagebox.showwarning("Nessuna selezione", "Seleziona un pacchetto.")
                return

            pkg_name = listbox.get(selected[0])
            if pkg_name not in self.package_states:
                self.package_states[pkg_name] = True
                self.add_package_row(pkg_name)
                self.manager.to_install.append(pkg_name)
            else:
                messagebox.showinfo("Esiste già", f"{pkg_name} è già presente.")

            popup.destroy()

        tk.Button(popup, text="Installa", command=install_selected).pack(pady=5)

    def remove_selected_package(self):
        pkg = self.selected_package
        if not pkg or pkg not in self.package_states:
            messagebox.showwarning("Nessuna selezione", "Seleziona prima un pacchetto.")
            return

        # Rimuovi widget dalla UI
        for widget in self.scrollable_frame.winfo_children():
            if widget.winfo_name() == pkg:
                widget.destroy()
                break

        # Rimuovi dagli stati e dalle liste manager
        del self.package_states[pkg]
        self.manager.to_install = [p for p in self.manager.to_install if p != pkg]
        self.manager.to_uninstall = [p for p in self.manager.to_uninstall if p != pkg]

        self.selected_package = None
    
    def Export(self):
        filepath = filedialog.asksaveasfilename(
            title="Salva configurazione pacchetti",
            defaultextension=".config",
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return  # Utente ha annullato

        self.manager.conf_export(filepath)
        messagebox.showinfo("Esportazione completata", f"Configurazione esportata in:\n{filepath}")

    def Import(self):
        filepath = filedialog.askopenfilename(
            title="Apri configurazione pacchetti",
            filetypes=[("File configurazione", "*.config"), ("Tutti i file", "*.*")]
        )
        if not filepath:
            return  # Utente ha annullato

        # Pulisci lo stato attuale
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.package_states.clear()
        self.manager.to_install.clear()
        self.manager.to_uninstall.clear()
        self.selected_package = None

        # Importa la configurazione
        self.manager.conf_import(filepath)

        # Unisci i pacchetti da installare e disinstallare
        all_packages = set(self.manager.to_install + self.manager.to_uninstall)

        for pkg in all_packages:
            is_installed = pkg in self.manager.to_install
            self.package_states[pkg] = is_installed
            self.add_package_row(pkg)

        messagebox.showinfo("Importazione completata", f"Configurazione importata da:\n{filepath}")
