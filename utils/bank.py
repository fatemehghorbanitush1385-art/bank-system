# -*- coding: utf-8 -*-
import json
import os
from utils.account import Account

class Bank:
    def __init__(self, filename="accounts.json"):
        self.filename = filename
        self.accounts = {}
        self._load_accounts()
    
    def _load_accounts(self):
        """حساب‌ها رو از JSON بخون"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    for acc_data in data:
                        acc = Account(
                            acc_data["account_number"],
                            acc_data["owner"],
                            acc_data["password"],
                            0
                        )
                        acc.balance = acc_data["balance"]
                        acc.transactions = acc_data["transactions"]
                        self.accounts[acc_data["account_number"]] = acc
            except (json.JSONDecodeError, OSError):
                pass
    
    def _save_accounts(self):
        """حساب‌ها رو توی JSON ذخیره کن"""
        with open(self.filename, "w", encoding="utf-8") as f:
            data = [acc.to_dict() for acc in self.accounts.values()]
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def create_account(self, account_number, owner, password):
        """حساب جدید بساز"""
        if account_number in self.accounts:
            return False, "این شماره حساب قبلاً وجود دارد!"
        
        account = Account(account_number, owner, password)
        self.accounts[account_number] = account
        self._save_accounts()
        return True, f"حساب {owner} با شماره {account_number} ساخته شد."
    
    def get_account(self, account_number):
        """حساب رو پیدا کن"""
        return self.accounts.get(account_number)
    
    def account_exists(self, account_number):
        """بررسی کن حساب وجود داره"""
        return account_number in self.accounts
    
    def transfer(self, from_account, to_account, amount, password):
        """انتقال پول بین حساب‌ها"""
        if from_account not in self.accounts:
            return False, "حساب فرستنده وجود ندارد!"
        
        if to_account not in self.accounts:
            return False, "حساب دریافت‌کننده وجود ندارد!"
        
        sender = self.accounts[from_account]
        
        if not sender.verify_password(password):
            return False, "رمز عبور غلط است!"
        
        success, msg = sender.withdraw(amount)
        if not success:
            return False, msg
        
        receiver = self.accounts[to_account]
        receiver.deposit(amount)
        
        self._save_accounts()
        return True, f"{amount} تومان از حساب شما به {receiver.owner} انتقال یافت."