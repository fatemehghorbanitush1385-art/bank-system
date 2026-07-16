# -*- coding: utf-8 -*-
from datetime import datetime

class Account:
    def __init__(self, account_number, owner, password, initial_balance=0):
        self.account_number = account_number
        self.owner = owner
        self.password = password
        self.balance = initial_balance
        self.transactions = []
        
        if initial_balance > 0:
            self.transactions.append({
                "type": "deposit",
                "amount": initial_balance,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "balance_after": self.balance
            })
    
    def verify_password(self, password):
        """رمز عبور رو بررسی کن"""
        return self.password == password
    
    def deposit(self, amount):
        """پول واریز کن"""
        if amount <= 0:
            return False, "مقدار باید بیشتر از صفر باشد."
        
        self.balance += amount
        self.transactions.append({
            "type": "deposit",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self.balance
        })
        return True, f"{amount} تومان واریز شد. موجودی جدید: {self.balance}"
    
    def withdraw(self, amount):
        """پول برداشت کن"""
        if amount <= 0:
            return False, "مقدار باید بیشتر از صفر باشد."
        
        if amount > self.balance:
            return False, "موجودی کافی نیست!"
        
        self.balance -= amount
        self.transactions.append({
            "type": "withdraw",
            "amount": amount,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "balance_after": self.balance
        })
        return True, f"{amount} تومان برداشت شد. موجودی جدید: {self.balance}"
    
    def get_balance(self):
        """موجودی رو نشون بده"""
        return self.balance
    
    def get_transactions(self):
        """تاریخچه تراکنش‌ها رو نشون بده"""
        return self.transactions
    
    def to_dict(self):
        """حساب رو به دیکشنری تبدیل کن (برای JSON)"""
        return {
            "account_number": self.account_number,
            "owner": self.owner,
            "password": self.password,
            "balance": self.balance,
            "transactions": self.transactions
        }
    def notify_transaction(self, message):
        """ارسال اطلاع‌رسانی برای تراکنش"""
        notification = f"📧 {message}"
        print(notification)
        return True
    
    def export_transactions_to_csv(self, filename):
        """صادرات تراکنش‌ها به CSV"""
        import csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Date', 'Type', 'Amount', 'Balance'])
            for trans in self.transactions:
                writer.writerow([
                    trans['date'],
                    trans['type'],
                    trans['amount'],
                    trans['balance_after']
                ])