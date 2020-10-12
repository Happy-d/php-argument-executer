from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfile
import subprocess
import os


version = "beta-v1.0.2"

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


class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # determine the ratio of old width/height to new width/height
        w_scale = float(event.width)/self.width
        h_scale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all", 0, 0, w_scale, h_scale)


class App(Frame):

    def __init__(self, master=None, build=None):
        super().__init__(master)
        self.master = master
        self.winX = 800
        self.winY = 600
        self.win_bg = "gray21"
        # self.master.geometry("{}x{}".format(self.winX, self.winY))
        self.master.title("PHP Argument Executer ({})".format(build))
        self.master.iconbitmap("icon.ico")
        self.master.configure(bg=self.win_bg)
        self.padding = 10
        self.output = ""    # Output for text box
        self.output_colour = ""    # Text Colour for output

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

        self.path_var = StringVar()

        self.path_ent = Entry(self.canvas_path,
                              width=56,
                              textvariable=self.path_var,
                              bg=self.canvas_bg,
                              fg=self.text_fg)

        self.path_btn = Button(self.canvas_path,
                               width=10,
                               text="Select...",
                               bg=self.canvas_bg,
                               fg=self.text_fg,
                               command=self.get_dir)

        self.path_script = Label(self.canvas_path,
                                 bg=self.canvas_bg,
                                 fg=self.text_fg)
        self.master.bind('<KeyRelease>', lambda event=None: self.update())

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
                             width=80,
                             textvariable=self.arg_var,
                             bg=self.canvas_bg,
                             fg=self.text_fg)
        self.arg_ent.insert(END, "argv1~argv2~argv3")

        self.arg_info = Label(self.canvas_arg,
                              text="* Make sure to leave a '~' between arguments",
                              bg=self.canvas_bg,
                              fg=self.text_fg)
        self.arg_clear = Button(self.canvas_arg,
                                width=8,
                                text="Clear",
                                bg=self.canvas_bg,
                                fg=self.text_fg,
                                command=self.clear_args)

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
        self.pop_btn = Button(self.canvas_out,
                              width=8,
                              text="Pop Out",
                              bg=self.canvas_bg,
                              fg=self.text_fg,
                              command=self.pop_out)
        # self.out_error = Text(self.canvas_out,
        #                       height=1,
        #                       width=50,
        #                       highlightthickness=0,
        #                       bg=self.canvas_bg,
        #                       fg="firebrick3")

        self.place()
        self.update()

    def place(self):
        # Path Canvas
        self.canvas_path.grid(padx=self.padding, pady=self.padding)
        self.path_title.place(x=6, y=0)
        self.path_lbl.place(x=140, y=30, anchor="e")
        self.path_ent.place(x=150, y=30, anchor="w")
        self.path_btn.place(x=500, y=30, anchor="w")
        self.path_script.place(x=680, y=30, anchor="center")

        # Arguments Canvas
        self.canvas_arg.grid(row=1, padx=self.padding, pady=self.padding)
        self.arg_title.place(x=6, y=0)
        self.arg_lbl.place(x=140, y=50, anchor="e")
        self.arg_ent.place(x=150, y=50, anchor="w")
        self.arg_info.place(x=150, y=75, anchor="w")
        self.arg_clear.place(x=645, y=50, anchor="w")

        # Output Canvas
        self.canvas_out.grid(row=2, padx=self.padding, pady=self.padding)
        self.out_title.place(x=6, y=0)
        self.out_box.place(x=16, y=40)
        self.exec_btn.place(x=self.winX - 40, y=20, anchor="e")
        self.pop_btn.place(x=self.winX - 125, y=20, anchor="e")
        # self.out_error.place(x=150, y=20, anchor="w")

    def update(self):
        self.dir_name = self.path_var.get()
        self.filename = os.path.basename(self.dir_name)
        self.path_script.configure(text=self.filename)

    def get_dir(self):
        file = askopenfile(filetypes=[('PHP Files', '*.php')],
                           initialdir=self.dir_name)
        if file is not None:
            self.dir_name = file.name
            self.path_ent.delete(0, END)
            self.path_ent.insert(END, self.dir_name)
            self.update()

    def execute(self):
        self.out_box.delete("1.0", "end")

        args = self.arg_var.get().split('~')

        command = ['C:/xampp/php/php.exe', '{}'.format(self.dir_name)]

        for arg in args:
            command.append(arg)

        try:
            self.output_colour = "white"
            result = subprocess.run(
                command,  # program and arguments
                stdout=subprocess.PIPE,  # capture stdout
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                check=True  # raise exception if program fails
            )

            self.output = result.stdout.decode("utf-8")
        except subprocess.CalledProcessError as error:
            self.output_colour = "firebrick3"
            if self.dir_name == "":
                hint = "(Try selecting a path)"
            else:
                hint = ""

            self.output = "ERROR: {}\n\n{}".format(error, hint)

        self.out_box.configure(fg=self.output_colour)

        self.out_box.delete("1.0", "end")

        self.out_box.insert(END, self.output)

    def clear_args(self):
        self.arg_ent.delete(0, END)

    def pop_out(self):
        self.canvas_out.grid_forget()
        PopOut(self)

    def pop_in(self):
        self.canvas_out.grid(row=2, padx=self.padding, pady=self.padding)


class PopOut(Toplevel):
    def __init__(self, app=None):
        Toplevel.__init__(self)
        self.windowX = 800
        self.windowY = 300
        self.geometry('{}x{}'.format(self.windowX, self.windowY))
        self.iconbitmap("icon.ico")
        self.title("PHP Argument Executer (Output)")
        self.configure(bg="gray21")
        self.app = app
        self.protocol("WM_DELETE_WINDOW", self.pop_in)

        # Output window
        self.canvas_out = Canvas(self,
                                 bg=self.app.canvas_bg,
                                 highlightthickness=0,
                                 width=self.windowX - 20,
                                 height=self.windowY - 20)

        self.box_canvas = Canvas(self.canvas_out,
                                 bg="white",
                                 highlightthickness=0,
                                 width=self.windowX - 52,
                                 height=self.windowY - 76)

        self.out_title = Label(self.canvas_out,
                               text="Output:",
                               font=self.app.title_font,
                               bg=self.app.canvas_bg,
                               fg=self.app.text_fg)

        self.out_box = ScrolledText(self.box_canvas,
                                    height=self.windowY / 22,
                                    width=91,
                                    bg="gray18",
                                    fg=self.app.text_fg)

        self.exec_btn = Button(self.canvas_out,
                               width=10,
                               text="Execute",
                               bg=self.app.canvas_bg,
                               fg=self.app.text_fg,
                               command=self.execute)
        self.pop_btn = Button(self.canvas_out,
                              width=8,
                              text="Pop In",
                              bg=self.app.canvas_bg,
                              fg=self.app.text_fg,
                              command=self.pop_in)
        self.canvas_out.bind('<Configure>', self.resize)

        self.place()

    def place(self):
        self.canvas_out.pack(fill="both", expand=True, padx=10, pady=10)
        self.out_title.place(x=6, y=0)
        self.box_canvas.pack(fill="both", expand=True, padx=10, pady=(40, 10))
        self.out_box.pack(fill="both", expand=True)
        self.exec_btn.place(x=self.windowX - 20, y=20, anchor="e")
        self.pop_btn.place(x=self.windowX - 125, y=20, anchor="e")

    def execute(self):
        self.app.execute()

        self.out_box.configure(fg=self.app.output_colour)

        self.out_box.delete("1.0", "end")

        self.out_box.insert(END, self.app.output)

    def resize(self, event=None):
        w, h = event.width, event.height
        self.exec_btn.place(x=w - 20, y=20, anchor="e")
        self.pop_btn.place(x=w - 105, y=20, anchor="e")
        self.canvas_out.configure(width=w, height=h)
        self.box_canvas.configure(width=w - 52, height=h - 76)

    def pop_in(self):
        self.app.pop_in()
        self.destroy()


def main():
    root = Tk()
    app = App(root, version)
    app.mainloop()


if __name__ == '__main__':
    main()
