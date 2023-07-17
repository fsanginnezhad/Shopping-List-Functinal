from typing import NewType

Total = NewType('Total', int())
ShoppingList = NewType('ShoppingList', dict)
Invoice = NewType('Invoice', list)
Number = NewType('Number', int)
Price = NewType('Price', int)
Product = NewType('Product', dict({str: Number, str: Price}))
Group = NewType('Group', dict({str: Product}))
Basket = NewType('Basket', dict({str: Group}))
