import tkinter as tk
from tkinter import messagebox
import os
import pickle
from features import extract_features
import pandas as pd
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


class PhishingWebsiteChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Phishing Website Checker")
        self.root.geometry("600x400")
        self.websites = []  # List to hold websites
        self.models = []
        self.load_models()
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        title_label = tk.Label(
            self.root,
            text="Phishing Website Checker",
            font=("Arial", 16, "bold"),
            fg="blue",
        )
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        self.website_entry = tk.Entry(input_frame, width=50)
        self.website_entry.pack(side=tk.LEFT, padx=5)

        add_button = tk.Button(input_frame, text="Add Website", command=self.add_website)
        add_button.pack(side=tk.LEFT, padx=5)

        # Website List
        self.website_listbox = tk.Listbox(self.root, width=70, height=10)
        self.website_listbox.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        check_button = tk.Button(button_frame, text="Check Websites", command=self.check_websites)
        check_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(button_frame, text="Clear Websites", command=self.clear_websites)
        clear_button.pack(side=tk.LEFT, padx=5)

        exit_button = tk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.LEFT, padx=5)

        # Output Frame
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10)

        self.output_text = tk.Text(output_frame, width=70, height=10, state=tk.DISABLED)
        self.output_text.pack()

    def load_models(self):
        """Load all .h5 models from the directory."""
        path = 'C:/Users/user/PycharmProjects/phishing_websites/models'
        if not os.path.exists(path):
            messagebox.showerror("Error", f"Model directory not found: {path}")
            return

        all_files = os.listdir(path)
        self.models = [os.path.join(path, model) for model in all_files if model.endswith('.h5')]

        if not self.models:
            messagebox.showerror("Error", "No models found in the directory!")
        else:
            messagebox.showinfo("Models Loaded", f"Loaded {len(self.models)} models.")

    def add_website(self):
        """Add website to the list."""
        website = self.website_entry.get().strip()
        if website:
            self.websites.append(website)
            self.website_listbox.insert(tk.END, website)
            self.website_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a website!")

    def clear_websites(self):
        """Clear the list of websites."""
        self.websites.clear()
        self.website_listbox.delete(0, tk.END)
        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.configure(state=tk.DISABLED)

    def check_websites(self):
        """Check websites against the loaded models."""
        if not self.websites:
            messagebox.showwarning("Warning", "No websites to check!")
            return

        all_features = [extract_features(url) for url in self.websites]
        url_df = pd.DataFrame(all_features)

        self.output_text.configure(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)

        for model_path in self.models:
            model_name = os.path.basename(model_path).replace('.h5', '').replace('_', ' ')
            self.output_text.insert(tk.END, f"\nPredictions using {model_name}:\n")

            try:
                with open(model_path, 'rb') as file:
                    classifier = pickle.load(file)

                predictions = classifier.predict(url_df)
                for url, prediction in zip(self.websites, predictions):
                    if prediction == 'good':
                        self.output_text.insert(tk.END, f"{url}: Benign URL\n")
                    else:
                        self.output_text.insert(tk.END, f"{url}: Phishing URL\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Error with model {model_name}: {e}\n")

        self.output_text.configure(state=tk.DISABLED)


# Run the GUI application
if __name__ == "__main__":
    root = tk.Tk()
    app = PhishingWebsiteChecker(root)
    root.mainloop()

