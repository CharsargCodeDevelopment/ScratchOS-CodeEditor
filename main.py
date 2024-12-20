import tkinter as tk
from tkinter import filedialog, messagebox
import compiler

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.file_path = None
        self.converted_code_window = None
        self.converted_code_label = None

        # Create text widget
        self.text_area = tk.Text(self.root, wrap="word", undo=True)
        self.text_area.pack(fill="both", expand=True)

        # Track changes in the text area
        self.text_area.bind("<<Modified>>", self.update_converted_code)

        # Create menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # File menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Edit menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo)
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=lambda: self.root.focus_get().event_generate("<<Cut>>"))
        self.edit_menu.add_command(label="Copy", command=lambda: self.root.focus_get().event_generate("<<Copy>>"))
        self.edit_menu.add_command(label="Paste", command=lambda: self.root.focus_get().event_generate("<<Paste>>"))
        
        # Export menu
        self.export_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Export", menu=self.export_menu)
        self.export_menu.add_command(label="Export ScratchOS Script", command=self.export_file)
        #self.file_menu.add_command(label="New", command=self.new_file)
        #self.file_menu.add_command(label="Open", command=self.open_file)
        #self.file_menu.add_command(label="Save", command=self.save_file)
        #self.file_menu.add_command(label="Save As", command=self.save_as_file)
        #self.file_menu.add_separator()
        #self.file_menu.add_command(label="Exit", command=self.root.quit)

        # Tools menu
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Show Converted Code", command=self.show_converted_code)
        #self.root.after(100,self.UpdateConvertedCodeWindowPosition)
        self.root.bind("<Configure>", self.UpdateConvertedCodeWindowPosition)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.root.title("Simple Text Editor - New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, content)
            self.file_path = file_path
            self.root.title(f"Simple Text Editor - {file_path}")

    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            messagebox.showinfo("Save File", "File saved successfully!")
        else:
            self.save_as_file()

    def export_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            text = self.text_area.get(1.0, tk.END).strip()
            converted_code = compiler.Compile(text)
            converted_code = "␤".join(converted_code.split('\n'))
            with open(file_path, "w") as file:
                
                file.write(converted_code)
            #self.file_path = file_path
            #self.root.title(f"Simple Text Editor - {file_path}")
            messagebox.showinfo("Export File", "File exported successfully!")
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_path = file_path
            self.root.title(f"Simple Text Editor - {file_path}")
            messagebox.showinfo("Save File", "File saved successfully!")

    def show_converted_code(self):
        # Check if the window is already open
        if self.converted_code_window:
            return

        # Create a new window to display converted_code
        self.converted_code_window = tk.Toplevel(self.root)
        self.converted_code_window.title("Converted Code")
        self.converted_code_window.protocol("WM_DELETE_WINDOW", self.close_converted_code_window)

        # Create a Label to display the contents of converted_code
        self.converted_code_label = tk.Label(self.converted_code_window, text="", anchor="nw", justify="left", wraplength=500)
        self.converted_code_label.pack(fill="both", expand=True, padx=10, pady=10)
        
        #self.converted_code_window.geometry("128x128")
        self.converted_code_window.minsize(128,128)
        self.converted_code_window.bind("<Configure>", self.resizing)

        # Update the label initially
        self.update_converted_code()
        
    def resizing(self,event = None):
        self.resizing = True
        self._after_id = self.converted_code_window.after(100, self.stopresizing)
    def stopresizing(self):
        self.resizing = False

    def update_converted_code(self, event=None):
        # Get the text content from the editor
        text = self.text_area.get(1.0, tk.END).strip()
        converted_code = compiler.Compile(text)
        #converted_code = text
        # Update the label in the new window if it's open
        if self.converted_code_label:
            
            self.converted_code_label.config(text=converted_code)

        # Reset the modified flag of the text widget
        if event:
            self.text_area.edit_modified(False)
            
            
    def UpdateConvertedCodeWindowPosition(self,event = None):
        #self.set_window_position(x=10)
        #print(self.root.winfo_x(), self.root.winfo_y())
        if self.converted_code_window == None:
            #self.root.after(100,self.UpdateConvertedCodeWindowPosition)
            return
        #print(self.resizing)
        #if self.resizing == True:
            #self.root.after(100,self.UpdateConvertedCodeWindowPosition)
         #   return
        h = self.root.winfo_height()
        w = self.root.winfo_width()
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        
        h1 = self.converted_code_window.winfo_height()
        w1 = self.converted_code_window.winfo_width()
        x1 = self.converted_code_window.winfo_x()
        y1 = self.converted_code_window.winfo_y()
        
        #x1 -= w

        #self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        #print(w1)
        #if w1 == 1:
          #  w1 = 128
        #if h1 == 1:
         #   h1 = 128
        #w1 = 128
        x-=w1
        self.converted_code_window.geometry('%dx%d+%d+%d' % (w1, h1, x, y))
        #self.root.after(1,self.UpdateConvertedCodeWindowPosition)
        """
        geom = (self.root.geometry())
        geom = geom.split('+')
        """
        """
        w = geom.split('x').pop(0)
        h = geom.split('x').pop(1).split('+').pop(0)
        w = int(w)
        h = int(h)
        x_center = (ws/2) - (w/2)
        y_center = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        """
    """
    def set_window_position(self,window = None,x=0,y=0):
        
        # get screen width and height
        geom = (self.root.geometry())
        w = geom.split('x').pop(0)
        h = geom.split('x').pop(1).split('+').pop(0)
        w = int(w)
        h = int(h)
        print(w,h,geom)
        
        ws = self.root.winfo_screenwidth() # width of the screen
        hs = self.root.winfo_screenheight() # height of the screen
        x_center = (ws/2) - (w/2)
        y_center = (hs/2) - (h/2)
        x_center+= x
        x_center += y
        x = x_center
        y = y_center
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    """

    def close_converted_code_window(self):
        self.converted_code_window.destroy()
        self.converted_code_window = None
        self.converted_code_label = None


if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
