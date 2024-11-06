
import tkinter as tk
from tkinter import messagebox
import pickle

# Load the data from the pickle file
def load_data():
    try:
        with open('data.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        messagebox.showerror("Data Load Error", f"Could not load data: {e}")
        return []

# Search through the data based on the input criteria
def search_data():
    author_name = author_entry.get().strip()
    paper_name = paper_entry.get().strip()
    category_name = category_entry.get().strip()
    
    # Filter results based on the provided criteria
    results = []
    for author in data:
        if author_name and author_name.lower() not in author['author_name'].lower():
            continue
        for paper in author['papers']:
            if paper_name and paper_name.lower() not in paper['name'].lower():
                continue
            if category_name and category_name.lower() not in paper['category'].lower():
                continue
            results.append((author['author_name'], paper['paper_id'], paper['name'], paper['year'], paper['category']))
    
    display_results(results)

# Display the search results in the GUI
def display_results(results):
    result_text.delete(1.0, tk.END)  # Clear previous results
    if not results:
        result_text.insert(tk.END, "No results found.\n")
    else:
        for author, paper_id, paper, year, category in results:
            result_text.insert(tk.END, f"Author: {author}\nPaper ID: {paper_id}\nPaper: {paper}\nYear: {year}\nCategory: {category}\n\n")

# Clear the results displayed
def clear_results():
    result_text.delete(1.0, tk.END)

# Create the GUI
def create_gui():
    global author_entry, paper_entry, category_entry, result_text

    root = tk.Tk()
    root.title("RESEARCH PAPER SEARCHING APPLICATION")

    # Label and Entry for Author Name
    tk.Label(root, text="Author Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    author_entry = tk.Entry(root, width=30)
    author_entry.grid(row=0, column=1, padx=10, pady=5)

    # Label and Entry for Paper Name
    tk.Label(root, text="Paper Name:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    paper_entry = tk.Entry(root, width=30)
    paper_entry.grid(row=1, column=1, padx=10, pady=5)

    # Label and Entry for Category
    tk.Label(root, text="Category:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    category_entry = tk.Entry(root, width=30)
    category_entry.grid(row=2, column=1, padx=10, pady=5)

    # Search button
    search_button = tk.Button(root, text="Search", command=search_data)
    search_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Clear button
    clear_button = tk.Button(root, text="Clear Results", command=clear_results)
    clear_button.grid(row=3, column=2, padx=10)

    # Text widget for displaying results
    result_text = tk.Text(root, width=80, height=20)
    result_text.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    # Load data from pickle
    global data
    data = load_data()

    # Focus the author entry field on start
    author_entry.focus()

    # Run the tkinter main loop
    root.mainloop()

# Run the GUI application
if __name__ == "__main__":
    create_gui()
