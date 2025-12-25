from typing import ClassVar, Self


type Balance = int | float


class BankAccount:
    owner: str
    number: str | int
    balance: Balance
    created_accounts: ClassVar[list[Self]] = []

    def __init__(self, owner: str, number: str | int, balance: Balance = 0) -> None:
        self.owner = owner
        self.number = number

        try:
            balance = float(balance)
        except ValueError as e:
            raise ValueError("Invalid balance value") from e

        if balance < 0:
            raise ValueError("Balance must be positive")

        self.balance = balance
        BankAccount.created_accounts.append(self)

    def deposit(self, amount: Balance) -> None:
        self.balance += amount

    def withdraw(self, amount: Balance) -> None:
        if amount > self.balance:
            raise ValueError("Not enough balance")

        self.balance -= amount

    def transfer_to(self, other_account: Self, amount: Balance) -> None:
        self.withdraw(amount=amount)
        other_account.deposit(amount=amount)

    def info(self) -> str:
        info = f"Owner: {self.owner}, Number: {self.number}, Balance: {self.balance}"
        return info

    @classmethod
    def get_accounts_created(cls) -> int:
        return len(cls.created_accounts)
