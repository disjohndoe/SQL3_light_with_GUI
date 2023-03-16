import tkinter as tk
from tkinter import ttk

# Import the create_tab1 function and other required modules
from accounts_tab import create_tab1
from gui2 import create_tab2


def main():
    root = tk.Tk()
    root.title("Main GUI")

    # Create the tabbed interface
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill=tk.BOTH)

    # Create the first tab and add it to the notebook
    tab1_frame = ttk.Frame(notebook)
    notebook.add(tab1_frame, text="Add Account")

    # Call the create_tab1 function to create the content of the first tab
    create_tab1(tab1_frame)

    # Add 2nd tab
    tab2_frame = ttk.Frame(notebook)
    notebook.add(tab2_frame, text="Tab 2")

    # Call the create_tab2 function to create the content of the second tab
    create_tab2(tab2_frame)

    # Add more tabs as needed
    # tab3_frame = ttk.Frame(notebook)
    # notebook.add(tab3_frame, text="Tab 3")
    # create_tab3(tab3_frame)
    # ...

    root.mainloop()


if __name__ == "__main__":
    main()
