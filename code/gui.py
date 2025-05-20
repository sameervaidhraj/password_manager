import tkinter as tk
from tkinter import messagebox, simpledialog
from manager import PasswordManager

class PasswordManagerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Password Manager")
        self.manager = None
        self.initialize_gui()

    def initialize_gui(self):
        """Initialize GUI components."""
        # Login Section
        tk.Label(self.master, text="Master Password:").grid(row=0, column=0, padx=10, pady=10)
        self.master_password_entry = tk.Entry(self.master, show="*")
        self.master_password_entry.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Login", command=self.login).grid(row=0, column=2, padx=10, pady=10)

        # Forgot Password Option
        tk.Button(self.master, text="Forgot Password?", command=self.forgot_password).grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Password Actions Section
        self.action_frame = None

    def login(self):
        """Login functionality."""
        master_password = self.master_password_entry.get()
        try:
            self.manager = PasswordManager(master_password)
            self.show_actions()
        except ValueError as e:
            messagebox.showerror("Login Failed", f"Login failed: {str(e)}")

    def show_actions(self):
        """Display actions after login."""
        if self.action_frame:
            self.action_frame.destroy()

        self.action_frame = tk.Text(self.master, height=10, width=50)
        self.action_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        tk.Button(self.master, text="Add Password", command=self.add_password_gui).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(self.master, text="View Passwords", command=self.view_passwords_gui).grid(row=3, column=1, padx=10, pady=10)
        tk.Button(self.master, text="Delete Password", command=self.delete_password_gui).grid(row=3, column=2, padx=10, pady=10)

    def add_password_gui(self):
        """GUI to add new password entry."""
        self.add_frame = tk.Frame(self.master)
        self.add_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        tk.Label(self.add_frame, text="Site:").grid(row=0, column=0, padx=10, pady=10)
        self.site_entry = tk.Entry(self.add_frame)
        self.site_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.add_frame, text="Username:").grid(row=1, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.add_frame)
        self.username_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.add_frame, text="Password:").grid(row=2, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.add_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.add_frame, text="Confirm Password:").grid(row=3, column=0, padx=10, pady=10)
        self.confirm_password_entry = tk.Entry(self.add_frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.add_frame, text="Save", command=self.save_password).grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def save_password(self):
        """Save the password entry after confirming both passwords match."""
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Check if passwords match
        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please try again.")
            return  # Prevent saving if passwords don't match

        # Proceed to save the password if both passwords match
        site = self.site_entry.get()
        username = self.username_entry.get()

        self.manager.add_password(site, username, password)
        self.action_frame.insert(tk.END, f"Added password for {site} (Username: {username})\n")
        self.add_frame.destroy()

    def view_passwords_gui(self):
        """View stored passwords."""
        self.action_frame.delete(1.0, tk.END)
        for encrypted_site, data in self.manager.data.items():
            site = self.manager.decrypt_data(encrypted_site)
            decrypted_username = self.manager.decrypt_data(data['username'])
            decrypted_password = self.manager.decrypt_data(data['password'])
            self.action_frame.insert(tk.END, f"Site: {site}\n")
            self.action_frame.insert(tk.END, f"  Username: {decrypted_username}\n")
            self.action_frame.insert(tk.END, f"  Password: {decrypted_password}\n\n")

    def delete_password_gui(self):
        """Delete a password entry."""
        self.delete_frame = tk.Frame(self.master)
        self.delete_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

        tk.Label(self.delete_frame, text="Enter site to delete:").grid(row=0, column=0, padx=10, pady=10)
        self.site_to_delete_entry = tk.Entry(self.delete_frame)
        self.site_to_delete_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.delete_frame, text="Delete", command=self.delete_password).grid(row=0, column=2, padx=10, pady=10)

    def delete_password(self):
        """Delete a password."""
        site = self.site_to_delete_entry.get()
        self.manager.delete_password(site)
        self.action_frame.insert(tk.END, f"Deleted password for {site}\n")
        self.delete_frame.destroy()

    def forgot_password(self):
        """Allow user to reset the master password."""
        old_password = simpledialog.askstring("Forgot Password", "Enter your old master password:", show="*")
        if old_password and old_password == self.manager.master_password:
            new_password = simpledialog.askstring("New Password", "Enter your new master password:", show="*")
            self.manager.reset_master_password(old_password, new_password)
        else:
            messagebox.showerror("Error", "Incorrect old master password.")


if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordManagerGUI(root)
    root.mainloop()
