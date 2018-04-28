from tkinter import Frame
from tkinter import Entry
from tkinter import Label
from tkinter import Checkbutton
from tkinter import IntVar
from tkinter import Button
from tkinter import StringVar
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import END
import math
import pickle
import dill
from trainer.file_data import FileData
from trainer.learner import Learner
from trainer.meta_learner import MetaLearner


class TrainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.l = None

        self.load_image = PhotoImage(file="images/load.png")
        self.meta_image = PhotoImage(file="images/recurse.png")
        self.folder_path = StringVar()
        self.meta_path = StringVar()
        self.k_control = IntVar(value=0)
        self.prog_control = IntVar(value=0)

        self.construct()
        self.pack(expand=True)

    def construct(self):
        self.construct_load_box()
        self.construct_input_boxes()

    def load_routine(self):
        filename = filedialog.askopenfilename()
        self.folder_path.set(filename)

        try:
            fd = FileData.file_to_data(self.folder_path.get())
            self.l = Learner(int(self.chrom_entry.get()),
                            int(self.head_entry.get()),
                            int(self.gene_entry.get()), fd)
        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "Invalid data file. Use the LOAD command.")

    def set_text(self, box, text):
        box.delete(0, END)
        box.insert(0, text)

    def meta_routine(self):
        filename = filedialog.askopenfilename()
        self.meta_path.set(filename)
        messagebox.showinfo("Finished",
                            "Loaded parameters from {}".format(
                                self.meta_path.get()))

        try:
            fd = FileData.file_to_data(self.folder_path.get())
            with open(self.meta_path.get(), "rb") as file:
                params = pickle.load(file)

            self.set_text(self.chrom_entry,
                          math.floor(params[MetaLearner.N_CHROM]))
            self.set_text(self.head_entry,
                          math.floor(params[MetaLearner.HEAD_LEN]))
            self.set_text(self.gene_entry,
                          math.floor(params[MetaLearner.N_GENE]))
            self.l = Learner(int(self.chrom_entry.get()),
                             int(self.head_entry.get()),
                             int(self.gene_entry.get()), fd)
            self.l.set_params(params)
        except:
            messagebox.showerror("Error",
                                 "Invalid data file. Use the LOAD command.")

    def construct_load_box(self):
        top_frame = Frame(self)
        path_entry = Label(top_frame, textvariable=self.folder_path)
        path_entry.grid(row=0, column=0, padx=10)

        load_button = Button(top_frame, image=self.load_image,
                             command=self.load_routine)
        load_button.grid(row=0, column=1, padx=10)
        recurse_button = Button(top_frame, image=self.meta_image,
                                command=self.meta_routine)
        recurse_button.grid(row=0, column=2, padx=10)

        top_frame.pack(side="top", pady=45)

    def start_training(self):
        if len(self.folder_path.get()) < 1 or self.l is None:
            messagebox.showerror("Error", "File path not provided. Use LOAD "
                                         "command")
            return

        try:
            max_cycles = int(self.cycle_entry.get())
            if self.k_control.get() == 1:
                fd = FileData.file_to_data(self.folder_path.get())
                self.l.k_fold_validation(fd,
                                         cycles=max_cycles,
                                         k=int(self.k_fold_entry.get()))
            else:
                self.l.learn(max_cycles=max_cycles)

            f_name = "fittest.p"
            with open(f_name, "wb") as out:
                best_chrom = self.l.best_pop.best
                dill.dump(best_chrom, out)

            messagebox.showinfo("Finished",
                                "Best population saved to fittest.p")
            self.update()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")

    def construct_input_boxes(self):
        bottom_frame = Frame(self)
        chrom_title = Label(bottom_frame, text="Chromosomes:")
        self.chrom_entry = Entry(bottom_frame, width=10)
        self.chrom_entry.insert(0, "30")
        chrom_title.grid(row=0, column=0, padx=10)
        self.chrom_entry.grid(row=0, column=1, padx=10)

        head_title = Label(bottom_frame, text="Head length:")
        self.head_entry = Entry(bottom_frame, width=10)
        self.head_entry.insert(0, "8")
        head_title.grid(row=0, column=2, padx=10)
        self.head_entry.grid(row=0, column=3, padx=10)

        gene_title = Label(bottom_frame, text="Number of Genes:")
        self.gene_entry = Entry(bottom_frame, width=10)
        self.gene_entry.insert(0, "4")
        gene_title.grid(row=0, column=4, padx=10)
        self.gene_entry.grid(row=0, column=5, padx=10)

        cycle_title = Label(bottom_frame, text="Number of Cycles:")
        self.cycle_entry = Entry(bottom_frame, width=10)
        self.cycle_entry.insert(0, "500")
        cycle_title.grid(row=1, column=0, padx=10, pady=10)
        self.cycle_entry.grid(row=1, column=1, padx=10, pady=10)

        k_fold_title = Checkbutton(bottom_frame, text="K-fold Validation:",
                                   variable=self.k_control)
        self.k_fold_entry = Entry(bottom_frame, width=10)
        self.k_fold_entry.insert(0, "10")
        k_fold_title.grid(row=1, column=2, padx=10, pady=10)
        self.k_fold_entry.grid(row=1, column=3, padx=10, pady=10)

        start_button = Button(bottom_frame, text="START", bg="#98fb98",
                              width=12, command=self.start_training)
        cancel_button = Button(bottom_frame, text="CANCEL", bg="#ff9292",
                               width=12)
        start_button.grid(row=1, column=4, padx=2, pady=10)
        cancel_button.grid(row=1, column=5, padx=2, pady=10)

        bottom_frame.pack(side="bottom", pady=40)
