from tkinter import *
from tkinter import ttk
from gui.frames.train_frame import TrainFrame
from gui.frames.eval_frame import EvalFrame
from gui.frames.meta_train_frame import MetaTrainFrame


class Base:
    def __init__(self):
        window = Tk()
        window.geometry("750x400")
        window.minsize(750, 400)
        window.title("GEP Movie Score Predictor")

        self.tabs = ttk.Notebook(master=window)
        meta_train_frame = MetaTrainFrame(self.tabs)
        train_frame = TrainFrame(self.tabs)
        eval_frame = EvalFrame(self.tabs)
        self.construct_tabs(meta_train_frame, train_frame, eval_frame)
        self.tabs.pack(expand=True, fill=BOTH)

        window.mainloop()

    def construct_tabs(self, mt, train, eval):
        self.tabs.add(mt, text="Meta Training")
        self.tabs.add(train, text="Training")
        self.tabs.add(eval, text="Evaluate")
