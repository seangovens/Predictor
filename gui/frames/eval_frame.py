from tkinter import Frame
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import StringVar
from gui.trees.artist import Artist
import dill
from scrape.rt_scraper import RTScraper
from trainer.file_data import FileData


class EvalFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.scrape = RTScraper()
        self.rating_image = PhotoImage(file="images/unknown.png")
        self.upload_image = PhotoImage(file="images/upload.png")
        self.refresh_image = PhotoImage(file="images/refresh.png")
        self.folder_path = StringVar(value="fittest.p")
        #with open("fittest.p", "rb") as in_file:
        #    self.chrom = dill.load(in_file)
        self.chrom = None
        self.refresh_chrom("fittest.p")

        self.artist = Artist()

        self.search_frame = Frame(self)
        self.right_frame = Frame(self.search_frame)
        self.left_frame = Frame(self.search_frame)
        self.top_frame = Frame(self)

        self.score_label = Label(master=self.left_frame,
                                 text="{:.0f}%".format(0),
                                 font=("Courier", 38))

        self.construct()
        self.pack(expand=True)

    def search_func(self):
        title = " ".join([self.title_entry.get(), self.year_entry.get()])\
            .strip()
        mov = self.scrape.get_movie(title)
        if mov is None:
            title = self.title_entry.get()
            mov = self.scrape.get_movie(title)

        guess = self.chrom(FileData.mov_to_data(self.scrape, title, mov))
        if guess >= 60:
            self.construct_guess("images/fresh.png", guess)
        else:
            self.construct_guess("images/rotten.png", guess)

    def construct(self):
        self.title_entry = Entry(self.right_frame, width=30)
        search_button = Button(self.right_frame, text="SEARCH", width=12,
                               command=self.search_func)
        self.year_entry = Entry(self.right_frame, width=5)
        title_label = Label(self.right_frame, text="Title:")
        year_label = Label(self.right_frame, text="Release year (optional):")

        title_label.grid(row=0, column=0, padx=5, sticky="e")
        self.title_entry.grid(row=0, column=1, sticky="w")
        search_button.grid(row=0, column=2, padx=5)

        year_label.grid(row=1, column=0, padx=5, pady=7, sticky="e")
        self.year_entry.grid(row=1, column=1, sticky="w")

        self.construct_guess("images/unknown.png", 0)
        self.construct_top()

        self.left_frame.grid(row=0, column=0)
        self.right_frame.grid(row=0, column=1)
        self.top_frame.pack(side="top", pady=20)
        self.search_frame.pack(side="bottom")

    def construct_guess(self, img_name, score):
        self.rating_image = PhotoImage(file=img_name)
        image_label = Label(master=self.left_frame, image=self.rating_image)
        self.score_label.destroy()
        self.score_label = Label(master=self.left_frame,
                                 text="{:.0f}%".format(score),
                                 font=("Courier", 38))

        image_label.grid(row=0, column=0, pady=70, sticky="e")
        self.score_label.grid(row=0, column=1, padx=10, pady=70, sticky="w")

    def load_routine(self):
        filename = filedialog.askopenfilename()
        self.folder_path.set(filename.split("/")[-1])
        self.refresh_chrom(filename)

    def refresh_chrom(self, in_file):
        with open(in_file, "rb") as in_file:
            self.chrom = dill.load(in_file)

    def upload_chrom(self):
        self.artist.draw_tree(list(map(repr, self.chrom.genes)))

    def construct_top(self):
        upload_button = Button(master=self.top_frame, image=self.upload_image,
                               command=self.upload_chrom)
        refresh_button = Button(master=self.top_frame, image=self.refresh_image,
                                command=self.load_routine)
        path_label = Label(master=self.top_frame, textvariable=self.folder_path)
        load_label = Label(master=self.top_frame, text="Loaded:")

        load_label.grid(row=1, column=0, pady=10, sticky="e")
        path_label.grid(row=1, column=1, pady=10, sticky="w")
        upload_button.grid(row=0, column=0, padx=35)
        refresh_button.grid(row=0, column=1, padx=35)
