"""
Graphical User Interface for Bed Spread
"""

import tkinter as tk
from tkinter import scrolledtext

from traceback import format_exc

from bedspread import __version__, front_end, evaluator
parser = front_end.Parser()
def run_code():
	result.configure(state='normal')
	result.delete("1.0", tk.END)
	text = code.get("1.0", tk.END)
	try:
		tree = parser.parse(text)
		value = evaluator.evaluate(tree)
		if isinstance(value, evaluator.Error):
			# Ideally do something smarter than...
			message = str(value)
		else:
			message = str(value)
	except Exception:
		message = format_exc()
	result.insert("1.0", message)
	result.configure(state='disabled')

def on_control_return(event):
	run_code()
	return "break"

root = tk.Tk()
tk.Label(root, text="Result").pack()
result = scrolledtext.ScrolledText(root, height=7, wrap = tk.WORD, )
result.insert("1.0", "testing 1..2..3..")
result.configure(state='disabled')
result.pack(expand=True)

tk.Label(root, text="Code Entry Area").pack()
code = scrolledtext.ScrolledText(root, height=7, wrap = tk.WORD)
code.pack()
code.bind("<Control-Return>", on_control_return)

button = tk.Button( root, text="Run Code (or press control-Enter)", command=run_code )
button.pack(fill=tk.X)

root.mainloop()

