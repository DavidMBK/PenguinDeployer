import tkinter as tk
from tkinter import messagebox
import subprocess

from packages import PackagesLogic  # importa la classe logica

class PackagesUI(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill=tk.BOTH, expand=True)

        self.package_states = {}

        self.manager = PackagesLogic()

        # Top frame
        top_frame = tk.LabelFrame(self, padx=10, pady=10)
        top_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        # Bottom frame
        bottom_frame = tk.LabelFrame(self, padx=10, pady=10)
        bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        # Scrollable area
        container = tk.Frame(top_frame)
        container.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container)
        self.scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.window_id = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollable_frame.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        self.scrollable_frame.bind("<Enter>", self._bind_to_mousewheel)
        self.scrollable_frame.bind("<Leave>", self._unbind_from_mousewheel)

        self.populate_packages()

        # Bottom controls
        self.search_entry = tk.Entry(bottom_frame)
        self.search_entry.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        for label in ["Aggiungi", "Rimuovi", "Import", "Export"]:
            cmd = self.open_package_popup if label == "Aggiungi" else self.placeholder_action
            tk.Button(bottom_frame, text=label, command=cmd).pack(side=tk.LEFT, padx=2)

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

    def populate_packages(self):
        for i in range(30):
            pkg_name = f"Pacchetto_{i}"
            self.package_states[pkg_name] = False
            self.add_package_row(pkg_name)

    def add_package_row(self, pkg_name):
        row = tk.Frame(self.scrollable_frame)
        row.pack(fill=tk.X, expand=True)
        row.grid_columnconfigure(0, weight=1)
        row.grid_columnconfigure(1, weight=0)

        name_label = tk.Label(row, text=pkg_name, anchor="w")
        name_label.grid(row=0, column=0, sticky="w", padx=10, pady=2)

        toggle_btn = tk.Button(
            row,
            text=self._get_button_text(pkg_name),
            command=lambda name=pkg_name, btn=None: self.toggle_install(name, btn)
        )
        toggle_btn.grid(row=0, column=1, sticky="e", padx=10, pady=2)
        toggle_btn.config(command=lambda name=pkg_name, btn=toggle_btn: self.toggle_install(name, btn))

    def toggle_install(self, pkg_name, button):
        self.package_states[pkg_name] = not self.package_states[pkg_name]
        button.config(text=self._get_button_text(pkg_name))
        action = "install" if self.package_states[pkg_name] else "uninstall"
        print(f"{pkg_name}: {action}")

    def _get_button_text(self, pkg_name):
        # Nota: mostra "Install" se è False (non installato), quindi il testo è l'azione da fare
        return "Install" if not self.package_states[pkg_name] else "Uninstall"

    def open_package_popup(self):
        query = self.search_entry.get().strip()
        if not query:
            messagebox.showwarning("Input mancante", "Inserisci un nome pacchetto da cercare.")
            return

        try:
            result = subprocess.run(
                ["apt-cache", "search", "--names-only", query],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            matches = [line.split(" - ")[0] for line in result.stdout.strip().split("\n") if line]
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
            else:
                messagebox.showinfo("Esiste già", f"{pkg_name} è già presente.")

            popup.destroy()

        tk.Button(popup, text="Installa", command=install_selected).pack(pady=5)