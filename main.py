from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfile
import subprocess
import os


# class ArgumentEntry(Entry):
#     def __init__(self, master=None, index=None):
#         super().__init__(Entry)
#         self.master = master
#         self.v = StringVar()
#         self.do_delete = False
#         self.text = Label(self.master,
#                           text="Arg {}".format(index),
#                           bg=self.master["bg"],
#                           fg="gray90")
#         self.entry = Entry(self.master,
#                            width=10,
#                            bg=self.master["bg"],
#                            fg="gray90",
#                            textvariable=self.v)
#         self.delete_btn = Button(self.master,
#                                  width=3,
#                                  text="-",
#                                  bg=self.master["bg"],
#                                  fg="gray90",
#                                  command=self.set_delete)
#
#     def set_delete(self):
#         self.do_delete = True


class App(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.winX = 800
        self.winY = 400
        self.win_bg = "gray21"
        # self.master.geometry("{}x{}".format(self.winX, self.winY))
        self.master.title("PHP Argument Executer (Beta)")
        self.master.iconbitmap("icon.ico")
        self.master.configure(bg=self.win_bg)
        self.padding = 10

        self.title_font = ("Calibri", 16, "underline")
        self.text_fg = "gray90"
        self.canvas_bg = "gray30"
        self.dir_name = "C:/"
        self.filename = ""

        # Path Canvas
        self.canvas_path = Canvas(self.master,
                                  bg=self.canvas_bg,
                                  highlightthickness=0,
                                  width=self.winX - 20,
                                  height=60)

        self.path_title = Label(self.canvas_path,
                                text="Path:",
                                font=self.title_font,
                                bg=self.canvas_bg,
                                fg=self.text_fg)

        self.path_lbl = Label(self.canvas_path,
                              text="File Path:",
                              bg=self.canvas_bg,
                              fg=self.text_fg)

        self.path_ent = Entry(self.canvas_path,
                              width=56,
                              bg=self.canvas_bg,
                              fg=self.text_fg)

        self.path_btn = Button(self.canvas_path,
                               width=10,
                               text="Select...",
                               bg=self.canvas_bg,
                               fg=self.text_fg,
                               command=self.get_dir)

        self.path_script = Label(self.canvas_path,
                                 text="Filename: ",
                                 bg=self.canvas_bg,
                                 fg=self.text_fg)

        # Arguments Canvas
        self.canvas_arg = Canvas(self.master,
                                 bg=self.canvas_bg,
                                 highlightthickness=0,
                                 width=self.winX - 20,
                                 height=100)

        self.arg_title = Label(self.canvas_arg,
                               text="Arguments:",
                               font=self.title_font,
                               bg=self.canvas_bg,
                               fg=self.text_fg)

        self.arg_lbl = Label(self.canvas_arg,
                             text="Arguments: ",
                             bg=self.canvas_bg,
                             fg=self.text_fg)

        self.arg_var = StringVar()
        self.arg_ent = Entry(self.canvas_arg,
                             width=66,
                             textvariable=self.arg_var,
                             bg=self.canvas_bg,
                             fg=self.text_fg)
        self.arg_ent.insert(END, "argv1 argv2 argv3")

        self.arg_info = Label(self.canvas_arg,
                              text="* Leave a space between arguments",
                              bg=self.canvas_bg,
                              fg=self.text_fg)

        # Output Canvas
        self.canvas_out = Canvas(self.master,
                                 bg=self.canvas_bg,
                                 highlightthickness=0,
                                 width=self.winX - 20,
                                 height=300)

        self.out_title = Label(self.canvas_out,
                               text="Output:",
                               font=self.title_font,
                               bg=self.canvas_bg,
                               fg=self.text_fg)
        self.out_box = ScrolledText(self.canvas_out,
                                    height=15,
                                    width=91,
                                    bg="gray18",
                                    fg=self.text_fg)
        self.exec_btn = Button(self.canvas_out,
                               width=10,
                               text="Execute",
                               bg=self.canvas_bg,
                               fg=self.text_fg,
                               command=self.execute)
        self.out_error = Label(self.canvas_out,
                               bg=self.canvas_bg,
                               fg="firebrick3")

        self.place()
        self.update()

    def place(self):
        # Path Canvas
        self.canvas_path.grid(padx=self.padding, pady=self.padding)
        self.path_title.place(x=6, y=0)
        self.path_lbl.place(x=140, y=30, anchor="e")
        self.path_ent.place(x=150, y=30, anchor="w")
        self.path_btn.place(x=500, y=30, anchor="w")
        self.path_script.place(x=650, y=30, anchor="center")

        # Arguments Canvas
        self.canvas_arg.grid(row=1, padx=self.padding, pady=self.padding)
        self.arg_title.place(x=6, y=0)
        self.arg_lbl.place(x=140, y=50, anchor="e")
        self.arg_ent.place(x=150, y=50, anchor="w")
        self.arg_info.place(x=560, y=50, anchor="w")

        # Output Canvas
        self.canvas_out.grid(row=2, padx=self.padding, pady=self.padding)
        self.out_title.place(x=6, y=0)
        self.out_box.place(x=16, y=40)
        self.exec_btn.place(x=self.winX - 40, y=20, anchor="e")
        self.out_error.place(x=150, y=20, anchor="w")

    def update(self):
        self.path_script.configure(text="Filename: " + self.filename)

    def get_dir(self):
        file = askopenfile(filetypes=[('PHP Files', '*.php')],
                           initialdir=self.dir_name)
        if file is not None:
            self.dir_name = file.name
            self.path_ent.delete(0, END)
            self.path_ent.insert(END, self.dir_name)
            self.filename = os.path.basename(self.dir_name)
            self.update()

    def execute(self):
        args = self.arg_var.get().split(' ')

        command = ['C:/xampp/php/php.exe', '{}'.format(self.dir_name)]

        for arg in args:
            command.append(arg)

        try:
            result = subprocess.run(
                command,  # program and arguments
                stdout=subprocess.PIPE,  # capture stdout
                check=True  # raise exception if program fails
            )

            output = result.stdout.decode("utf-8")

            self.out_box.delete("1.0", "end")

            self.out_box.insert(END, output)
        except subprocess.CalledProcessError:
            self.out_error['text'] = "ERROR: No file has been selected. Please select a file path."
            self.after(4000, self.clear_error)

    def clear_error(self):
        self.out_error['text'] = ""


def main():
    root = Tk()
    app = App(root)
    app.mainloop()


if __name__ == '__main__':
    main()
