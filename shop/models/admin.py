from shop.models.product import product_menu
from shop.helper.const import BACK_COMMANDS
from shop.models.group import (
    empty_group_menu,
    group_menu
)
from shop.utils.help_funcs import (
    title,
    help_admin,
    clear_screen,
    help_admin_group,
)


def admin_menu(basket: dict[dict[str]]) -> None:
    messege = 'Enter your command "Group" or "Product" or "Back": '
    messege_1 = 'Enter your command "Group" or "Back": '
    while True:
        clear_screen()
        print(title('Admin Menu'))
        if basket:
            help_admin_group()
            command = input(messege).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'group':
                group_menu(basket)
            elif command == 'product':
                product_menu(basket)
        else:
            help_admin()
            command = input(messege_1).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'group':
                empty_group_menu(basket)
