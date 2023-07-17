import os
import logging
import functools
from getpass import getpass
from shop.helper.exception import (
    NotNumber,
    GroupNameError,
    ProductDoesExist,
    ProductNameError,
    GroupDoesNotExist,
    ProductDoesNotExist,
)

logger = logging.getLogger(__name__)


def title(title: str = '-') -> str:
    return f'---{title}---------------------------------------------------------------------'  # noqa E501


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def decortor_exceptions(func):
    @functools.wraps(func)
    def exception(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except GroupNameError as e:
            show_error(e)
        except GroupDoesNotExist as e:
            show_error(e)
        except ProductDoesExist as e:
            show_error(e)
        except ProductNameError as e:
            show_error(e)
        except NotNumber as e:
            show_error(e)
        except ProductDoesNotExist as e:
            show_error(e)
        except Exception as e:
            show_error('500! please contact administrator')
    return exception


def keep() -> None:
    getpass('\nPress ENTER to continue...')


def show_error(message):
    print(f'Error: {message}!')
    keep()


def show_help() -> str:
    print('''
    1. Use "Admin" to add groups and products to the warehouse.
    2. Use the "Store" to buy products from the warehouse.
    ''')


def help_admin() -> None:
    print('''
    By default, there is no group in the application, and as you can see, you cannot add a product until you have a group. # noqa E501
    You must first add grouping to the application.

    Use "Group" to add and "Back" to return to main menu.
    ''')


def help_admin_group() -> None:
    print('''
    1. If you want to go to the groups menu, use "Group".
    2. If you want to go to the product menu, use the "Product".
    3. If you want to go to the main menu, use "Back".
    ''')


def help_group_add() -> None:
    print('''
    1. If you want to add grouping, use "Add".
    2. If you want to go to the previous menu, use "Back".
    ''')


def help_group() -> None:
    print('''
    1. If you want to add grouping, use "Add".
    2. If you want to modify the grouping, use "Edit".
    3. If you want to deleted the grouping, use "Delete".
    4. If you want to see the list of groups, use the "Show".
    5. If you want to go to the previous menu, use "Back".
    ''')


def help_product() -> None:
    print('''
    1. If you want to add products to the warehouse, use "Add".
    2. If you want to modify warehouse products, use "Edit".
    3. If you want to see the list of products along with the grouping, use the "Show". # noqa E501
    4. If you want to go to the previous menu, use "Back".
    ''')


def help_product_empty() -> None:
    print('''
    1. If you want to add products to the warehouse, use "Add".
    3. If you want to see the list of products along with the grouping, use the "Show". # noqa E501
    4. If you want to go to the previous menu, use "Back".
    ''')


def help_store() -> None:
    print('''
                <<< Welcome to the Store >>>

    1. Use "Add" to make a shopping list from the warehouse.
    2. Use "Show" to view the shopping list.
    3. Use "Delete" to remove the product from the shopping list.
    4. Use "Search" to check if a product is in the shopping list or not.
    5. Use "Total" to view the payable amount.
    6. Use "Back" to return to the main menu.
    ''')


def help_store_empty() -> None:
    print('''
                <<< Welcome to the Store >>>

    1. Use "Add" to make a shopping list from the warehouse.
    2. Use "Show" to view the shopping list.
    3. Use "Total" to view the payable amount.
    4. Use "Back" to return to the main menu.
    ''')
