from tkinter import *
from tkinter import messagebox
import webbrowser
from logger import Login

root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg='#fff')
root.resizable(False,False)

# Funzione Login
def try_login():
    username = user.get()
    password = passw.get()

    if username == "Username" or password == "Password":
        messagebox.showerror("Error", "Please enter username and password.")
        return

    # Implementare cambio di frame etc...
    success, msg = login.adminlogin(username,password)
    if success: 
          messagebox.showinfo("Success", msg)
    else: 
          messagebox.showerror("Error", msg)

# Funzione prettamente grafica per rimuovere e aggiornare la barra. 
def on_enter_user(e):
        if user.get() == 'Username':
            user.delete(0,'end')

def on_leave_user(e):
        name = user.get()
        if name == '':
            user.insert(0,'Username')

def on_enter_pass(e):
        if passw.get() == 'Password':
            passw.delete(0,'end')

def on_leave_pass(e):
        name = passw.get()
        if name == '':
            passw.insert(0,'Password')
            
def GithubStar():
    webbrowser.open_new("https://github.com/DavidMBK/PenguinDeployer")

# Parte Immagine a sinistra

img = PhotoImage(file='src/imagines/login.png')
Label(root,image=img,bg='white').place(x=50,y=50)

frame = Frame(root, width=350, height=350, bg="white", bd=0, highlightthickness=0)

frame.place(x=480, y=70)

heading=Label(frame, text='Sign in', fg='#57a1f8', bg='white',font=('Microsoft YaHei UI Light',23,'normal'))
heading.place(x=100 , y=5)

# Parte Username

user = Entry(
    frame,
    width=25,
    fg='black',
    border=0,
    bg='white',
    font=('Microsoft YaHei UI Light', 11),
    highlightthickness=0,
    relief='flat'
)
user.place(x=30, y=80)
user.insert(0,'Username')
user.bind('<FocusIn>',on_enter_user)
user.bind('<FocusOut>',on_leave_user)

Frame(frame, width=295, height=1, bg='gray').place(x=25, y=107)

# Parte Password

passw = Entry(
    frame,
    width=25,
    fg='black',
    border=0,
    bg='white',
    font=('Microsoft YaHei UI Light', 11),
    highlightthickness=0,
    relief='flat'
)
passw.place(x=30, y=150)
passw.insert(0,'Password')
passw.bind('<FocusIn>',on_enter_pass)
passw.bind('<FocusOut>',on_leave_pass)

Frame(frame, width=295, height=1, bg='gray').place(x=25, y=177)

# buttone 

login = Login()

Button(frame,width=32,pady=7,text='Sign in',bg='#57a1f8',fg='white',border=0, command=try_login).place(x=34,y=204)

# Star now

label = Label(frame, text="Love the project?",fg='black',bg='white',font=('Microsoft YaHei UI Light',9,'normal'))
label.place(x=75,y=270)

star_now = Button(frame, width=6, text='Star now',border=0,bg='white',cursor='hand2',fg='#EAB308', highlightthickness=0,relief='flat', command=GithubStar)
star_now.place(x=172,y=263.5)

root.mainloop()

