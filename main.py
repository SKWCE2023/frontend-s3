import tkinter as tk
from tkinter import ttk, PhotoImage
from login import LoginFrame

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Shubhs")
        self.root.geometry("800x600")
        self.root.minsize("800","600")
        self.root.configure(bg="white")
        self.style = ttk.Style()
        self.style.configure("TFrame", background="white")
        self.style.configure("TLabel", background="white", font=('Helvetica', 12))
        self.style.configure("TCheckbutton", background="white", font=('Helvetica', 8))
        self.style.configure('TButton', font=('Helvetica', 12), borderwidth = '4', ipadx=15, ipady=15)
        self.style.map('TButton', foreground = [('active', '!disabled', 'green')])
        LoginFrame(self.root, False, False, False)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    img = PhotoImage(file='assets/images/Logo.png')
    root.iconphoto(False, img)
    root.mainloop()
