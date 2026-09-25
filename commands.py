from pathlib import Path
import tkinter as tk


root = tk.Tk()
root.title("Commands")
root.geometry("700x400")

search_text = tk.StringVar()
something = tk.Entry(root, textvariable=search_text, width=60)
something.pack()
something.focus()

text = tk.Text(root)
text.pack(fill=tk.BOTH, expand=True)
text.config(state="disabled")
text.tag_configure("desc", font=("Consolas", 8, "italic"))
text.tag_configure("command", font=("Consolas", 9, "bold"))
text.tag_bind("icon", "<Enter>", lambda e: text.config(cursor="hand2"))
text.tag_bind("icon", "<Leave>", lambda e: text.config(cursor=""))


def copy_command(event):
    index = text.index(f"@{event.x},{event.y}")
    line_start = text.index(f"{index} linestart")
    start, end = text.tag_nextrange("command", line_start)
    command_text = text.get(start, end)
    root.clipboard_clear()
    root.clipboard_append(command_text)

    icon_start, icon_end = text.tag_prevrange("icon", f"{start}")
    text.tag_add("flash", icon_start, icon_end)
    text.tag_configure("flash", background="gray")
    root.after(200, lambda: text.tag_remove("flash", icon_start, icon_end))

text.tag_bind("icon", "<Button-1>", copy_command)

cheatsheet = Path(__file__).parent / "cheatsheet.txt"

with open(cheatsheet) as f:
    commands = f.readlines()


def on_typing(*args):
 
    query = search_text.get()
    text.config(state="normal")
    text.delete("1.0", tk.END)
    for cmd in commands:
        parts = cmd.split("|")
        if query in parts[0]:
            text.insert(tk.END, "📋 ", "icon")
            text.insert(tk.END, parts[0], "command")
            text.insert(tk.END, parts[1], "desc")
    text.config(state="disabled")
search_text.trace_add("write", on_typing)
root.mainloop()
