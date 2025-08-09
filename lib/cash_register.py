# lib/cash_register.py

class CashRegister:
    def __init__(self, discount=0):
        """
        Initialize a CashRegister.

        :param discount: optional integer percent discount (e.g. 20 for 20%)
        """
        self.discount = discount
        self.total = 0.0
        self.items = []
        # Track last transaction so it can be voided
        self._last_transaction_amount = 0.0
        self._last_transaction_title = None
        self._last_transaction_quantity = 0

    def add_item(self, title, price, quantity=1):
        """
        Add an item to the register.

        :param title: str, item name
        :param price: numeric, price per single item
        :param quantity: int, how many of this item to add (defaults to 1)
        """
        # compute this transaction
        amount = price * quantity

        # update last transaction info
        self._last_transaction_amount = amount
        self._last_transaction_title = title
        self._last_transaction_quantity = quantity

        # update total and items list
        self.total += amount
        for _ in range(quantity):
            self.items.append(title)

    def apply_discount(self):
        """
        Apply the instance discount to the current total.

        Prints a success message with the updated total if a discount exists,
        otherwise prints an error message.
        """
        if not self.discount:
            print("There is no discount to apply.")
            return

        # apply percent discount
        self.total = self.total * (100 - self.discount) / 100.0

        # Format the printed total to drop .0 for whole numbers
        if float(self.total).is_integer():
            total_str = str(int(self.total))
        else:
            # two decimal places is reasonable
            total_str = f"{self.total:.2f}"

        print(f"After the discount, the total comes to ${total_str}.")

    def void_last_transaction(self):
        """
        Remove the last transaction's effect from total and items.

        If there are no items/transactions, set total to 0.0.
        """
        # subtract the last transaction amount
        self.total -= self._last_transaction_amount

        # remove the last transaction's items from the items list
        if self._last_transaction_title and self._last_transaction_quantity > 0:
            # remove up to last_transaction_quantity occurrences from the end
            qty = self._last_transaction_quantity
            # safer removal from end to preserve earlier duplicates
            removed = 0
            for _ in range(qty):
                # try to remove last occurrence of that title
                for i in range(len(self.items) - 1, -1, -1):
                    if self.items[i] == self._last_transaction_title:
                        self.items.pop(i)
                        removed += 1
                        break

        # ensure total doesn't become a negative tiny float due to floating math
        if abs(self.total) < 1e-9:
            self.total = 0.0

        # reset last transaction info
        self._last_transaction_amount = 0.0
        self._last_transaction_title = None
        self._last_transaction_quantity = 0
