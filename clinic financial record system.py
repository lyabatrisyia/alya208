import tkinter as tk
from tkinter import ttk, messagebox

class EditRecordPopup:
    def __init__(self, parent, record_data, update_callback):
        self.popup = tk.Toplevel(parent)
        self.popup.title("Edit Record")

        self.record_data = record_data
        self.update_callback = update_callback

        self.label_name = tk.Label(self.popup, text="Name:", font=("Arial", 12), fg="black")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry_name = tk.Entry(self.popup, font=("Arial", 12), fg="black")
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.entry_name.insert(0, record_data["Name"])

        self.label_amount = tk.Label(self.popup, text="Amount:", font=("Arial", 12), fg="black")
        self.label_amount.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_amount = tk.Entry(self.popup, font=("Arial", 12), fg="black")
        self.entry_amount.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        if record_data["Amount"] is not None:
            self.entry_amount.insert(0, str(record_data["Amount"]))

        self.label_date = tk.Label(self.popup, text="Date:", font=("Arial", 12), fg="black")
        self.label_date.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_date = tk.Entry(self.popup, font=("Arial", 12), fg="black")
        self.entry_date.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.entry_date.insert(0, record_data["Date"])

        self.button_update = tk.Button(self.popup, text="Update Record", command=self.update_record, font=("Arial", 12), fg="black", bg="gray")
        self.button_update.grid(row=3, column=0, columnspan=2, pady=10)

    def update_record(self):
        name = self.entry_name.get()
        amount_str = self.entry_amount.get()
        date = self.entry_date.get()

        try:
            amount = float(amount_str) if amount_str else None
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for the amount.")
            return

        if name and date:
            self.record_data["Name"] = name
            self.record_data["Amount"] = amount
            self.record_data["Date"] = date

            if self.update_callback:
                self.update_callback()

            self.popup.destroy()

class ClinicFinancialRecordSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinic Financial Record System")

        self.main_frame = tk.Frame(root, bg="lightgray")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.records = []
        self.record_id_counter = 1
        self.selected_record_id = None

        self.label_name = tk.Label(self.main_frame, text="Name:", font=("Arial", 12), fg="black", bg="lightgray")
        self.label_name.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry_name = tk.Entry(self.main_frame, font=("Arial", 12), fg="black")
        self.entry_name.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_amount = tk.Label(self.main_frame, text="Amount:", font=("Arial", 12), fg="black", bg="lightgray")
        self.label_amount.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_amount = tk.Entry(self.main_frame, font=("Arial", 12), fg="black")
        self.entry_amount.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.label_date = tk.Label(self.main_frame, text="Date:", font=("Arial", 12), fg="black", bg="lightgray")
        self.label_date.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.entry_date = tk.Entry(self.main_frame, font=("Arial", 12), fg="black")
        self.entry_date.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        self.button_add = tk.Button(self.main_frame, text="Add Record", command=self.add_record, font=("Arial", 12), fg="black", bg="gray")
        self.button_add.grid(row=3, column=0, columnspan=2, pady=10)

        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Amount", "Date"), show="headings", selectmode="browse")
        self.tree.grid(row=4, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.tree.heading("ID", text="ID", anchor="center")
        self.tree.heading("Name", text="Name", anchor="center")
        self.tree.heading("Amount", text="Amount", anchor="center")
        self.tree.heading("Date", text="Date", anchor="center")

        for col in ("ID", "Name", "Amount", "Date"):
            self.tree.column(col, width=80, anchor="center")

        self.button_delete = tk.Button(self.main_frame, text="Delete Record", command=self.delete_record, font=("Arial", 12), fg="black", bg="gray")
        self.button_delete.grid(row=5, column=0, columnspan=2, pady=10)

        self.button_update = tk.Button(self.main_frame, text="Update Record", command=self.update_record, font=("Arial", 12), fg="black", bg="gray")
        self.button_update.grid(row=6, column=0, columnspan=2, pady=10)

        self.update_tree()

        self.root.bind("<F11>", self.toggle_full_screen)
        self.root.bind("<Escape>", self.exit_full_screen)
        self.root.bind("<Configure>", self.update_tree_columns)

        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(4, weight=1)

    def add_record(self):
        name = self.entry_name.get()
        amount_str = self.entry_amount.get()
        date = self.entry_date.get()

        try:
            amount = float(amount_str) if amount_str else None
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric value for the amount.")
            return

        if name and date:
            record_id = self.record_id_counter
            record = {"ID": record_id, "Name": name, "Amount": amount, "Date": date}
            self.records.append(record)
            self.record_id_counter += 1
            self.update_tree()
            self.clear_entries()

    def update_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.selected_record_id = None
            record_id = int(self.tree.item(selected_item, 'values')[0])
            selected_record = next((record for record in self.records if record["ID"] == record_id), None)

            if selected_record:
                self.selected_record_id = record_id
                edit_popup = EditRecordPopup(self.root, selected_record, self.update_tree)

    def delete_record(self):
        selected_item = self.tree.selection()
        if selected_item:
            record_id = int(self.tree.item(selected_item, 'values')[0])
            self.records = [record for record in self.records if record["ID"] != record_id]
            self.reset_record_ids()
            self.update_tree()

    def reset_record_ids(self):
        for i, record in enumerate(self.records, start=1):
            record["ID"] = i
        self.record_id_counter = len(self.records) + 1

    def update_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for record in self.records:
            self.tree.insert("", "end", values=(record["ID"], record["Name"], record["Amount"], record["Date"]))

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_amount.delete(0, tk.END)
        self.entry_date.delete(0, tk.END)

    def update_tree_columns(self, event=None):
        for col in ("ID", "Name", "Amount", "Date"):
            self.tree.column(col, width=80, anchor="center")

    def toggle_full_screen(self, event=None):
        self.root.attributes('-fullscreen', not self.root.attributes('-fullscreen'))

    def exit_full_screen(self, event=None):
        self.root.attributes('-fullscreen', False)

if __name__ == "__main__":
    root = tk.Tk()
    app = ClinicFinancialRecordSystem(root)
    root.mainloop()





