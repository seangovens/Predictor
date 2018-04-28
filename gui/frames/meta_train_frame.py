from tkinter import Frame
from tkinter import Entry
from tkinter import Label
from tkinter import Button
from tkinter import StringVar
from tkinter import filedialog
from tkinter import PhotoImage
from tkinter import messagebox
from trainer.file_data import FileData
from trainer.meta_learner import MetaLearner


class MetaTrainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.load_image = PhotoImage(file="images/load.png")
        self.folder_path = StringVar()
        self.population_entry = None
        self.generations_entry = None
        self.construct()

        self.pack(expand=True)

    def start_training(self):
        try:
            ml = MetaLearner(int(self.population_entry.get()),
                             int(self.generations_entry.get()),
                             FileData.file_to_data(self.folder_path.get(),
                                                   max_lines=MetaLearner.MAX_DATA))
            ml.run()
            messagebox.showinfo("Finished",
                                "Best parameters saved to best_model.p")
        except:
            messagebox.showerror("Error", "Please select a valid data set.")

    def construct(self):
        self.construct_load_box()
        bottom_frame = Frame(self)

        population_label = Label(bottom_frame, text="Population size:")
        self.population_entry = Entry(bottom_frame, width=10)
        self.population_entry.insert(0, "10")
        population_label.grid(row=0, column=0, padx=10)
        self.population_entry.grid(row=0, column=1, padx=10)

        generations_label = Label(bottom_frame, text="Generations:")
        self.generations_entry = Entry(bottom_frame, width=10)
        self.generations_entry.insert(0, "10")
        generations_label.grid(row=0, column=2, padx=10)
        self.generations_entry.grid(row=0, column=3, padx=10)

        start_button = Button(bottom_frame, text="START", bg="#98fb98",
                              width=12, command=self.start_training)
        cancel_button = Button(bottom_frame, text="CANCEL", bg="#ff9292",
                               width=12)
        start_button.grid(row=1, column=4, padx=2, pady=10)
        cancel_button.grid(row=1, column=5, padx=2, pady=10)

        bottom_frame.pack(side="bottom", pady=45)

    def construct_load_box(self):
        top_frame = Frame(self)
        path_entry = Label(top_frame, textvariable=self.folder_path)
        path_entry.grid(row=0, column=0, padx=10)

        load_button = Button(top_frame, image=self.load_image,
                             command=self.load_routine)
        load_button.grid(row=0, column=1, padx=10)

        top_frame.pack(side="top", pady=45)

    def load_routine(self):
        filename = filedialog.askopenfilename()
        self.folder_path.set(filename)
