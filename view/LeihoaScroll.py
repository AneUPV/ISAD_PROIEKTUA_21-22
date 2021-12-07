import tkinter as tk

from view import ScrollContainer

class LeihoaScroll():
	def __init__(self):
		self.window = tk.Tk()
		self.window.geometry('300x300')
		self.window.title("Strava Hasiera")

		scroll = ScrollContainer(self.window)

		# Leioa erabiltzeko erabiliko den frame-a
		self.main_frame = scroll.second_frame


		for i in range(20):
			for j in range(20):
				lbl = tk.Label(self.main_frame, text=f" | {i} - {j} | ")
				lbl.grid(row=i, column=j)

		self.window.mainloop()
		
