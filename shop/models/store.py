from shop.helper.type_hint import Invoice
from shop.helper.const import (
    BACK_COMMANDS,
    WRONG_COMMANDS,
)
from shop.utils.help_funcs import (
    keep,
    title,
    help_store,
    clear_screen,
    help_store_empty,
)
from shop.utils.funcs import (
    show_list,
    add_to_list,
    total_counter,
    final_invoice,
    search_in_list,
    delete_from_list,
)


def store_menu(basket: dict, shopping_list: dict, total: int):
    """
    Displays the store menu and handles user commands for managing a shopping list. # noqa E501

    Args:
        basket (dict): The dictionary representing the shopping basket.
        shopping_list (dict): The dictionary representing the shopping list.
        total (int): The total count.

    Returns:
        None
    """
    message = 'Enter your command "Add" or "show" or "Total": '
    message1 = 'Enter your command "Add" or "show" or "Delete" or "Search" or "Total": '  # noqa E501
    while True:
        invoice: Invoice = list()
        clear_screen()
        print(title('Store Menu'))
        if shopping_list:
            help_store()
            command = input(message1).casefold()
            if command in BACK_COMMANDS:
                break
            elif command in WRONG_COMMANDS:
                print('This is a mistake. try again')
                keep()
                continue
            elif command == 'add':
                add_to_list(basket, shopping_list)
            elif command == 'show':
                show_list(shopping_list)
                keep()
            elif command == 'delete':
                delete_from_list(shopping_list, basket)
            elif command == 'total':
                total_counter(shopping_list, basket, invoice)
                clear_screen()
                print(title('Total Invoice'))
                final_invoice(invoice, total)
                keep()
            elif command == 'search':
                command = input('Enter your word for search: ')
                search_in_list(shopping_list, command)
                keep()
        else:
            help_store_empty()
            command = input(message).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'add':
                add_to_list(basket, shopping_list)
            elif command == 'show':
                show_list(shopping_list)
                keep()
            elif command == 'total':
                total_counter(shopping_list, basket, invoice)
                clear_screen()
                print(title('Total Invoice'))
                final_invoice(invoice, total)
                keep()
