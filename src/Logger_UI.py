import tkinter as tk
from tkinter import messagebox
import webbrowser
from logger import Login

class LoginFrame(tk.Frame): # Impostare tk.Frame per avere il tk.raise per cambiare schermata nel main.
    
    def __init__(self,parent, controller, nconfigfolder):
        super().__init__(parent, bg='white')
        self.controller = controller
        self.login = Login()
    
        # Parte Immagine a sinistra

        #self.img = tk.PhotoImage(file='src/images/login.png')
        #tk.Label(self,image=self.img,bg='white').place(x=50,y=50)

        frame = tk.Frame(self, width=350, height=350, bg="white", bd=0, highlightthickness=0)

        frame.place(x=480, y=70)

        heading=tk.Label(frame, text='Sign in', fg='#57a1f8', bg='white',font=('Microsoft YaHei UI Light',23,'normal'))
        heading.place(x=100 , y=5)

        # Parte Username

        self.user = tk.Entry(
            frame,
            width=25,
            fg='black',
            border=0,
            bg='white',
            font=('Microsoft YaHei UI Light', 11),
            highlightthickness=0,
            relief='flat'
        )
        self.user.place(x=30, y=80)
        self.user.insert(0,'Username')
        self.user.bind('<FocusIn>',self.on_enter_user)
        self.user.bind('<FocusOut>',self.on_leave_user)

        tk.Frame(frame, width=295, height=1, bg='gray').place(x=25, y=107)

        # Parte Password

        self.passw = tk.Entry(
            frame,
            width=25,
            fg='black',
            border=0,
            bg='white',
            font=('Microsoft YaHei UI Light', 11),
            highlightthickness=0,
            relief='flat',
            show=''
        )
        self.passw.place(x=30, y=150)
        self.passw.insert(0,'Password')
        self.passw.bind('<FocusIn>',self.on_enter_pass)
        self.passw.bind('<FocusOut>',self.on_leave_pass)

        tk.Frame(frame, width=295, height=1, bg='gray').place(x=25, y=177)

        # buttone 

        login = Login()

        tk.Button(frame,width=32,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0, command=self.try_login).place(x=34,y=204)

        # Star now

        label = tk.Label(frame, text="Love the project?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9,'normal'))
        label.place(x=75,y=270)

        star_now = tk.Button(frame, width=6, text='Star now',border=0,bg='white',cursor='hand2',fg='#EAB308', highlightthickness=0,relief='flat', command=self.GithubStar)
        star_now.place(x=172,y=263.5)
    
    # Funzione Login
    def try_login(self):
        username = self.user.get()
        password = self.passw.get()
        if username == "Username" or password == "Password":
            messagebox.showerror("Error", "Please enter username and password.")
            return

        # Implementare cambio di frame etc...
        success, msg = self.login.adminlogin(username,password)
        if success: 
            messagebox.showinfo("Success", msg)
            self.controller.show_frame("Mainwindow")
        else: 
            messagebox.showerror("Error", msg)

    # Funzione prettamente grafica per rimuovere e aggiornare la barra. 
    def on_enter_user(self, e):
            if self.user.get() == 'Username':
                self.user.delete(0,'end')

    def on_leave_user(self, e):
            if self.user.get() == '':
                self.user.insert(0,'Username')

    def on_enter_pass(self, e):
            if self.passw.get() == 'Password':
                self.passw.delete(0,'end')
                self.passw.config(show='*')

    def on_leave_pass(self, e):
            if self.passw.get() == '':
                self.passw.insert(0,'Password')
                self.passw.config(show='')
                
    def GithubStar(self):
        webbrowser.open_new("https://github.com/DavidMBK/PenguinDeployer")


