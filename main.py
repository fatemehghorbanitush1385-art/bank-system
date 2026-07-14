# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from utils.bank import Bank

class BankApp:
    def __init__(self, root):
        self.root = root
        self.bank = Bank()
        self.current_account = None
        
        root.title("سیستم مدیریت حساب بانکی")
        root.geometry("700x600")
        root.configure(bg="#f5f5f5")
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Tahoma", 11), padding=6)
        
        self.show_login_screen()
    
    def show_login_screen(self):
        """صفحه ورود رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        
        tk.Label(frame, text="سیستم بانکی", font=("Tahoma", 20, "bold"), 
                 bg="#f5f5f5").pack(pady=20)
        
        tk.Label(frame, text="شماره حساب:", font=("Tahoma", 12), bg="#f5f5f5").pack()
        account_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        account_entry.pack(pady=5, padx=20, fill="x")
        
        tk.Label(frame, text="رمز عبور:", font=("Tahoma", 12), bg="#f5f5f5").pack()
        password_entry = tk.Entry(frame, font=("Tahoma", 11), show="*", justify="right")
        password_entry.pack(pady=5, padx=20, fill="x")
        
        def login():
            account_num = account_entry.get().strip()
            password = password_entry.get().strip()
            
            if not account_num or not password:
                messagebox.showwarning("خطا", "لطفاً همه فیلدها را پر کنید.")
                return
            
            account = self.bank.get_account(account_num)
            if not account or not account.verify_password(password):
                messagebox.showerror("خطا", "شماره حساب یا رمز عبور غلط است!")
                return
            
            self.current_account = account
            self.show_main_menu()
        
        def register():
            self.show_register_screen()
        
        ttk.Button(frame, text="ورود", command=login).pack(pady=10)
        ttk.Button(frame, text="ثبت‌نام", command=register).pack(pady=5)
    
    def show_register_screen(self):
        """صفحه ثبت‌نام رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True, padx=20)
        
        tk.Label(frame, text="ثبت‌نام حساب جدید", font=("Tahoma", 18, "bold"), 
                 bg="#f5f5f5").pack(pady=20)
        
        tk.Label(frame, text="شماره حساب:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        acc_num_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        acc_num_entry.pack(pady=5, fill="x")
        
        tk.Label(frame, text="نام صاحب حساب:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        owner_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        owner_entry.pack(pady=5, fill="x")
        
        tk.Label(frame, text="رمز عبور:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        pass_entry = tk.Entry(frame, font=("Tahoma", 11), show="*", justify="right")
        pass_entry.pack(pady=5, fill="x")
        
        def register():
            acc_num = acc_num_entry.get().strip()
            owner = owner_entry.get().strip()
            password = pass_entry.get().strip()
            
            if not acc_num or not owner or not password:
                messagebox.showwarning("خطا", "لطفاً همه فیلدها را پر کنید.")
                return
            
            success, msg = self.bank.create_account(acc_num, owner, password)
            messagebox.showinfo("نتیجه", msg)
            
            if success:
                self.show_login_screen()
        
        ttk.Button(frame, text="ثبت‌نام", command=register).pack(pady=10)
        ttk.Button(frame, text="بازگشت", command=self.show_login_screen).pack(pady=5)
    
    def show_main_menu(self):
        """منوی اصلی رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True)
        
        tk.Label(frame, text=f"خوش‌آمدید {self.current_account.owner}", 
                 font=("Tahoma", 16, "bold"), bg="#f5f5f5").pack(pady=20)
        
        tk.Label(frame, text=f"موجودی: {self.current_account.get_balance()} تومان", 
                 font=("Tahoma", 14), bg="#f5f5f5").pack(pady=10)
        
        ttk.Button(frame, text="واریز پول", 
                   command=self.show_deposit).pack(pady=5, padx=20, fill="x")
        ttk.Button(frame, text="برداشت پول", 
                   command=self.show_withdraw).pack(pady=5, padx=20, fill="x")
        ttk.Button(frame, text="انتقال پول", 
                   command=self.show_transfer).pack(pady=5, padx=20, fill="x")
        ttk.Button(frame, text="تاریخچه تراکنش‌ها", 
                   command=self.show_transactions).pack(pady=5, padx=20, fill="x")
        ttk.Button(frame, text="خروج", 
                   command=self.logout).pack(pady=5, padx=20, fill="x")
    
    def show_deposit(self):
        """صفحه واریز رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True, padx=20)
        
        tk.Label(frame, text="واریز پول", font=("Tahoma", 16, "bold"), 
                 bg="#f5f5f5").pack(pady=20)
        
        tk.Label(frame, text="مقدار:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        amount_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        amount_entry.pack(pady=5, fill="x")
        
        def deposit():
            try:
                amount = int(amount_entry.get().strip())
                success, msg = self.current_account.deposit(amount)
                messagebox.showinfo("نتیجه", msg)
                self.bank._save_accounts()
                if success:
                    self.show_main_menu()
            except ValueError:
                messagebox.showerror("خطا", "مقدار باید عدد باشد!")
        
        ttk.Button(frame, text="واریز", command=deposit).pack(pady=10)
        ttk.Button(frame, text="بازگشت", command=self.show_main_menu).pack(pady=5)
    
    def show_withdraw(self):
        """صفحه برداشت رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True, padx=20)
        
        tk.Label(frame, text="برداشت پول", font=("Tahoma", 16, "bold"), 
                 bg="#f5f5f5").pack(pady=20)
        
        tk.Label(frame, text="مقدار:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        amount_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        amount_entry.pack(pady=5, fill="x")
        
        def withdraw():
            try:
                amount = int(amount_entry.get().strip())
                success, msg = self.current_account.withdraw(amount)
                messagebox.showinfo("نتیجه", msg)
        
                self.bank._save_accounts()
                if success:
                    self.show_main_menu()
            except ValueError:
                messagebox.showerror("خطا", "مقدار باید عدد باشد!")
        
        ttk.Button(frame, text="برداشت", command=withdraw).pack(pady=10)
        ttk.Button(frame, text="بازگشت", command=self.show_main_menu).pack(pady=5)
    
    def show_transfer(self):
        """صفحه انتقال رو نشون بده"""
        self.clear_window()
        
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(expand=True, padx=20)
        
        tk.Label(frame, text="انتقال پول", font=("Tahoma", 16, "bold"), 
                 bg="#f5f5f5").pack(pady=20)
        tk.Label(frame, text="شماره حساب دریافت‌کننده:", font=("Tahoma", 11), 
                 bg="#f5f5f5").pack()
        to_acc_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        to_acc_entry.pack(pady=5, fill="x")
        
        tk.Label(frame, text="مقدار:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        amount_entry = tk.Entry(frame, font=("Tahoma", 11), justify="right")
        amount_entry.pack(pady=5, fill="x")
        
        tk.Label(frame, text="رمز عبور:", font=("Tahoma", 11), bg="#f5f5f5").pack()
        pass_entry = tk.Entry(frame, font=("Tahoma", 11), show="*", justify="right")
        pass_entry.pack(pady=5, fill="x")
        
        def transfer():
            try:
                to_acc = to_acc_entry.get().strip()
                amount = int(amount_entry.get().strip())
                password = pass_entry.get().strip()
                
                success, msg = self.bank.transfer(
                    self.current_account.account_number,
                    to_acc,
                    amount,
                    password
                )
                messagebox.showinfo("نتیجه", msg)
                if success:
                    self.show_main_menu()
            except ValueError:
                messagebox.showerror("خطا", "مقدار باید عدد باشد!")
        
        ttk.Button(frame, text="انتقال", command=transfer).pack(pady=10)
        ttk.Button(frame, text="بازگشت", command=self.show_main_menu).pack(pady=5)
    
    def show_transactions(self):
        """تاریخچه تراکنش‌ها رو نشون بده"""
        self.clear_window()
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        ttk.Button(frame, text="بازگشت", command=self.show_main_menu).pack(pady=10)
        
        tk.Label(frame, text="تاریخچه تراکنش‌ها", font=("Tahoma", 16, "bold"), 
                 bg="#f5f5f5").pack(pady=10)
        
        text = tk.Text(frame, font=("Tahoma", 10), height=15, width=60, 
                       justify="right", padx=10, pady=10)
        text.pack(fill="both", expand=True)
        
        transactions = self.current_account.get_transactions()
        if not transactions:
            text.insert("1.0", "هیچ تراکنشی موجود نیست.")
        else:
            for trans in transactions:
                line = f"{trans['date']} | {trans['type']} | {trans['amount']} تومان | موجودی: {trans['balance_after']}\n"
                text.insert("end", line)
        
        text.config(state="disabled")
        
        ttk.Button(frame, text="بازگشت", command=self.show_main_menu).pack(pady=10)
    
    def logout(self):
        """خروج کردن"""
        self.current_account = None
        self.show_login_screen()
    
    def clear_window(self):
        """پنجره رو پاک کن"""
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()