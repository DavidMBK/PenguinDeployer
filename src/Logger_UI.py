import tkinter as tk
from tkinter import messagebox
import webbrowser
from Logger import Login  # Importa la classe Login da un modulo esterno


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller, login):
        super().__init__(parent, bg='#d9d9d9')  # Frame principale con sfondo grigio chiaro
        self.controller = controller  # Controller per gestire i frame
        self.login = login  # Oggetto login per gestire l'autenticazione

        # Frame interno per contenere i widget di login, con dimensioni e posizione fissa
        frame = tk.Frame(self, width=350, height=350, bg="#d9d9d9", bd=0, highlightthickness=0)
        frame.place(x=290, y=70)

        # Titolo "Sign in"
        heading = tk.Label(frame, text='Sign in', fg='black', bg='#d9d9d9',
                           font=('Microsoft YaHei UI Light', 23, 'normal'))
        heading.place(x=100, y=5)

        # Campo Username - Entry con testo placeholder "Username"
        self.user = tk.Entry(
            frame,
            width=25,
            fg='black',
            border=0,
            bg='#d9d9d9',
            font=('Microsoft YaHei UI Light', 11),
            highlightthickness=0,
            relief='flat'
        )
        self.user.place(x=30, y=80)
        self.user.insert(0, 'Username')  # Inserisce testo placeholder
        # Eventi per gestire la sparizione e ricomparsa del placeholder
        self.user.bind('<FocusIn>', self.on_enter_user)
        self.user.bind('<FocusOut>', self.on_leave_user)
        # Linea decorativa sotto il campo
        tk.Frame(frame, width=295, height=1, bg='gray').place(x=25, y=107)

        # Campo Password - Entry con testo placeholder "Password"
        self.passw = tk.Entry(
            frame,
            width=25,
            fg='black',
            border=0,
            bg='#d9d9d9',
            font=('Microsoft YaHei UI Light', 11),
            highlightthickness=0,
            relief='flat',
            show='*'  # Mostra asterischi per nascondere la password
        )
        self.passw.place(x=30, y=150)
        self.passw.insert(0, 'Password')  # Inserisce placeholder
        self.passw.bind('<FocusIn>', self.on_enter_pass)
        self.passw.bind('<FocusOut>', self.on_leave_pass)
        tk.Frame(frame, width=295, height=1, bg='gray').place(x=25, y=177)

        # Pulsante Sign in che chiama il metodo try_login al click
        tk.Button(frame, width=32, pady=7, text='Sign in', bg='black', fg='#d9d9d9', border=0,
                  command=self.try_login).place(x=34, y=204)

        # Label "Love the project?"
        label = tk.Label(frame, text="Love the project?", fg='black', bg='#d9d9d9',
                         font=('Microsoft YaHei UI Light', 9, 'normal'))
        label.place(x=75, y=270)

        # Pulsante "Star now" che apre il link GitHub nel browser
        star_now = tk.Button(frame, width=6, text='Star now', border=0, bg='#d9d9d9', cursor='hand2', fg='#EAB308',
                             highlightthickness=0, relief='flat', command=self.GithubStar)
        star_now.place(x=172, y=263.5)

    def try_login(self):
        # Prende i valori inseriti dall'utente
        username = self.user.get()
        password = self.passw.get()
        
        # Controllo semplice se sono ancora i placeholder
        if username == "Username" or password == "Password":
            messagebox.showerror("Error", "Please enter username and password.")
            return

        # Usa l'oggetto login per provare ad effettuare il login
        success, msg = self.login.adminlogin(username, password)
        if success:
            messagebox.showinfo("Success", msg)
            # Se login riuscito, mostra il frame principale "Mainwindow"
            self.controller.show_frame("Mainwindow")
        else:
            messagebox.showerror("Error", msg)

    # Gestisce il placeholder del campo username quando si clicca dentro
    def on_enter_user(self, e):
        if self.user.get() == 'Username':
            self.user.delete(0, 'end')

    # Ripristina il placeholder se il campo username è vuoto
    def on_leave_user(self, e):
        if self.user.get() == '':
            self.user.insert(0, 'Username')

    # Gestisce il placeholder e la maschera password quando si clicca dentro
    def on_enter_pass(self, e):
        if self.passw.get() == 'Password':
            self.passw.delete(0, 'end')
            self.passw.config(show='*')  # Nasconde il testo con asterischi

    # Ripristina il placeholder se il campo password è vuoto e mostra il testo senza maschera
    def on_leave_pass(self, e):
        if self.passw.get() == '':
            self.passw.insert(0, 'Password')
            self.passw.config(show='')  # Mostra il testo normalmente

    # Metodo che apre il browser per mettere la "stellina" al progetto GitHub
    def GithubStar(self):
        webbrowser.open_new("https://github.com/DavidMBK/PenguinDeployer")
