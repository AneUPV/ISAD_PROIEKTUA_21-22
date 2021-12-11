import tkinter as tk
from tkinter import ttk

class ScrollContainer(ttk.Frame):

    def __init__(self, container, w=None, h=None, *args, **kwargs):

        super().__init__(container, *args, **kwargs)
        container.bind("<MouseWheel>", self._on_mousewheel) # bind on the parent window

        # Create a main frame

        self.main_frame = tk.Frame(container)
        self.main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=1)  # expand frame to the size of the container


        # create a canvas
        self.my_canvas = tk.Canvas(self.main_frame)
        self.my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # add h and v scrollbar to canvas

        self.my_vscrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.my_vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.my_hscrollbar = ttk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.my_canvas.xview)
        self.my_hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        # configure canvas
        self.my_canvas.configure(yscrollcommand=self.my_vscrollbar.set, xscrollcommand=self.my_hscrollbar.set)
        self.my_canvas.bind('<Configure>', lambda e: self.my_canvas.configure(scrollregion=self.my_canvas.bbox('all')))

        # create another frame inside the canvas
        self.second_frame = tk.Frame(self.my_canvas)

        # add that new frame to a window in the canvas
        self.my_canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

    def _on_mousewheel(self, event):

        self.my_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        #self.my_canvas.yview_scroll(-event.delta, "units")

    def update_layout(self):
        # All pending events, callbacks, etc. are processed in a non-blocking manner
        self.second_frame.update_idletasks()
        # We reconfigure the canvas' scrollregion to fit all of its widgets
        self.my_canvas.configure(scrollregion=self.my_canvas.bbox('all'))
        # reset the scroll
        #self.my_canvas.yview('moveto', '1.0')
        # fit the frame to the size of its inner widgets (grid_size)
        self.size = self.second_frame.grid_size()
