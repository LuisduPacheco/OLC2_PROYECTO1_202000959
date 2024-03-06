import tkinter as tk
from client.gui_app import Frame


def main():
    root = tk.Tk()
    root.title('---- OCLScript - Compilers 2 ----')
    # root.iconbitmap('img/algorithm.ico')
    root.resizable(None, None)

    # Frame
    app = Frame(root=root)

    # Main loop
    root.mainloop()


if __name__ == '__main__':
    main()
