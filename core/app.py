import logging
from conf.log import *
from shop.models.admin import admin_menu
from shop.models.store import store_menu
from shop.helper.const import EXIT_COMMANDS
from shop.helper.type_hint import (
    Total,
    Basket,
    ShoppingList,
)
from shop.utils.help_funcs import (
    title,
    show_help,
    clear_screen,
)

logger = logging.getLogger(__name__)


def main():
    basket: Basket = {
        'fruits': {
            'apple': {
                'price': 15_000,
                'number': 10,
                'discount': 0
            },
            'banana': {
                'price': 90_000,
                'number': 10,
                'discount': 0
            },
            'mango': {
                'price': 45_000,
                'number': 10,
                'discount': 0
            },
        },
        'drinks': {
            'water': {
                'price': 10_000,
                'number': 10,
                'discount': 0
            },
            'soda': {
                'price': 20_000,
                'number': 10,
                'discount': 0
            },
            'wine': {
                'price': 80_000,
                'number': 10,
                'discount': 0
            },
        },
        'foods': {
            'spagetty': {
                'price': 95_000,
                'number': 10,
                'discount': 0
            },
            'pizza': {
                'price': 110_000,
                'number': 10,
                'discount': 0
            },
            'hotdog': {
                'price': 80_000,
                'number': 10,
                'discount': 0
            },
        }
    }
    # basket: Basket = dict()
    shopping_list: ShoppingList = dict()
    total: Total = 0
    while True:
        message = 'Enter your command "Admin" or "Store": '
        clear_screen()
        print(title('Main Menu'))
        show_help()
        command = input(message).casefold()
        if command in EXIT_COMMANDS:
            break
        elif command == 'admin':
            admin_menu(basket)
        elif command == 'store':
            store_menu(basket, shopping_list, total)
