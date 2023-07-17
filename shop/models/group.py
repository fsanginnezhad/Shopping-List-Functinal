import logging
from shop.helper.exception import (
    GroupNameError,
    GroupDoesNotExist,
)
from shop.helper.const import (
    BACK_COMMANDS,
    WRONG_COMMANDS,
)
from shop.utils.help_funcs import (
    keep,
    title,
    help_group,
    clear_screen,
    help_group_add,
    decortor_exceptions,
)

logger = logging.getLogger(__name__)


def get_group_by_product_name(product: str, basket: dict) -> str:
    """
    Get the group containing a specific product.

    This function searches through the groups in the `basket` dictionary and checks if the provided `product` name exists within each group. If a group contains the given product, the function returns the name of that group. # noqa E501

    Args:
        product (str): The name of the product to search for.
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        str: The name of the group that contains the specified product, or None if the product is not found in any group. # noqa E501
    """
    for group in basket:
        if product in basket[group]:
            logger.info(f'The "{product}" into "{group}" of Basket.')
            return group


def show_group(basket: dict) -> None:
    """
    Display the groups in the basket dictionary.

    This function iterates through the groups in the `basket` dictionary using the `enumerate` function and prints each group along with its corresponding index. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        None
    """
    for index, group in enumerate(basket, start=1):
        print(f'{index}: {group}')
    logger.info('Show all groups to see.')


@decortor_exceptions
def add_group(basket: dict) -> None:
    """
    Adds a new group to the basket dictionary.

    Parameters:
        basket (dict): A dictionary representing the basket.

    Returns:
        None
    """
    message = 'Enter the name group for add to list: '
    while True:
        clear_screen()
        print(title('Add Group Menu'))
        print('\n-> Use `back` to `Group Menu`\n\n')
        group_choice = input(message).casefold()
        if group_choice in BACK_COMMANDS:
            break
        elif group_choice in WRONG_COMMANDS or group_choice.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise GroupNameError(f'Cannot use {WRONG_COMMANDS}')
        elif group_choice.isnumeric():
            logger.warning(f'Cannot use "integer".')
            raise GroupNameError(f'Cannot use "integer"')
        else:
            basket[group_choice] = dict()
            print(f'The `{group_choice}` added to list.')
            logger.info(f'The "{group_choice}" added to list.')
            keep()


def get_of_group(num_of_group: int, basket: dict) -> str:
    """
    Get the group name based on the provided number.

    This function retrieves the group name from the `basket` dictionary based on the provided number. It iterates through the groups in the `basket` using the `enumerate` function and compares the `num` parameter with the index. If there is a match, the corresponding group name is returned as a string. # noqa E501

    Args:
        num (int): The group number.
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        message (str): The group name as a string if a match is found with the provided number. Otherwise, returns 'Not' to indicate that no matching group was found. # noqa E501
    """
    message = 'Not'
    for index, group in enumerate(basket, start=1):
        if num_of_group == index:
            message = group
    return message


@decortor_exceptions
def deleted_group(basket: dict) -> None:
    """
    Delete groups from the basket dictionary based on user input.

    This function allows the user to delete groups from the basket dictionary. It enters a loop that displays a menu of existing groups in the basket. The user can select a group to delete by entering the group number or group name. The selected group is removed from the basket dictionary. # noqa E501

    If the basket becomes empty after deleting a group, a message indicating an empty basket is displayed. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        None
    """
    while basket:
        clear_screen()
        print(title('Deleted Group Menu'))
        print('\n-> Use `back` to `Group Menu`\n\n')
        show_group(basket)
        cart_group = get_group(basket)
        if not cart_group:
            break
        elif cart_group == 'Not':
            logger.error(
                f'The "{cart_group}" is not in groups. Please try again.'
            )
            raise GroupDoesNotExist(
                f'The `{cart_group}` is not in groups. Please try again'
            )
        else:
            basket.pop(cart_group)
            print(f'Deleted `{cart_group}` from Basket.')
            logger.info(f'Deleted "{cart_group}" from Basket.')
            keep()
    if not basket:
        clear_screen()
        print(title('Deleted Group Menu'))
        print('The Basket is empty.')
        keep()


def check_valid_group(group: str, basket: dict) -> str:
    """
    Check if the provided group is valid within the basket dictionary.

    This function checks if the provided group is a valid selection within the basket dictionary. It first attempts to convert the `group` parameter to an integer and calls the `get_of_group` function with that integer as input. If the conversion is successful and the `get_of_group` function returns a valid group, that group is considered valid. # noqa E501

    If the conversion fails or the `get_of_group` function raises an exception, the function checks if the `group` string is a key in the `basket` dictionary. If it is, the `group` is considered valid. # noqa E501

    Args:
        group (str): The group selection provided by the user.
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        cart_group (str): The selected group as a string if it is valid. Otherwise, returns 'Not' to indicate that the group is not valid. # noqa E501
    """
    if group.isnumeric():
        cart_group = get_of_group(int(group), basket)
    else:
        if group in basket:
            cart_group = group
        else:
            cart_group = 'Not'
    return cart_group


def get_group(basket: dict) -> str | bool:
    """
    Prompt user to select a group from the basket dictionary.

    This function displays a menu for selecting a group from the basket dictionary. The user can choose a group by entering the group number or group name. The function validates the user input and returns the selected group. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        cart_group (str): The selected group as a string, or False if the user chooses to go back to the Group Menu. # noqa E501
    """
    choice = 'First, select the group number or group name: '
    while True:
        clear_screen()
        print(title('Get Group Menu'))
        print('\n-> Use `back` to `Group Menu`\n\n')
        show_group(basket)
        group_choice = input(choice).casefold()
        if group_choice in BACK_COMMANDS:
            return False
        cart_group = check_valid_group(group_choice, basket)
        return cart_group


@decortor_exceptions
def edited_group(basket: dict) -> None:
    """
    Edits groups in the basket dictionary based on user input.

    Args:
        basket (dict): A dictionary representing the basket with group information. # noqa E501

    Returns:
        None
    """
    while True:
        cart_group = get_group(basket)
        if not cart_group:
            break
        elif cart_group == 'Not':
            logger.error(
                f'The "{cart_group}" is not in groups. Please try again.'
            )
            raise GroupDoesNotExist(
                f'The `{cart_group}` is not in groups. Please try again'
            )
        new_group = input('Enter the new group: ').casefold()
        if new_group in BACK_COMMANDS:
            break
        elif new_group in WRONG_COMMANDS or new_group.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise GroupNameError(f'Cannot use {WRONG_COMMANDS}')
        elif new_group.isnumeric():
            logger.warning(f'Cannot use "integer".')
            raise GroupNameError(f'Cannot use "integer"')
        else:
            basket[new_group] = basket.pop(cart_group)
            logger.debug(f'"{cart_group}" is edited to "{new_group}"')
            show_group(basket)
            keep()


def empty_group_menu(basket: dict) -> None:
    """
    Displays a menu for managing groups and allows the user to add new groups to the basket. # noqa E501

    Parameters:
        basket (dict): A dictionary representing the basket or container for storing groups. # noqa E501

    Returns:
        None

    Raises:
        N/A

    Usage:
        empty_group_menu({"Group1": ...})  # Example usage

    """
    message = 'Enter your command "Add" group or "Back" to menu: '
    while not basket:
        # Clears the console screen
        clear_screen()
        # Prints the title of the Groups Menu
        print(title('Groups Menu'))
        # Displays help or instructions for adding a group
        help_group_add()
        # Prompts the user for input and converts it to lowercase
        command = input(message).casefold()
        if command in BACK_COMMANDS:
            # Breaks the loop and exits the function if the command is in BACK_COMMANDS # noqa E501
            break
        elif command == 'add':
            # Calls the add_group function to add a group to the basket
            add_group(basket)


def group_menu(basket: dict) -> None:
    """
    Displays a menu for managing groups.

    The function presents a menu to the user and repeatedly prompts for their input until the `basket` becomes empty. # noqa E501

    Parameters:
    - basket (dict): A dictionary representing the collection of groups.

    Returns:
    None
    """
    message = 'Enter your command "Add" or "Edit" or "Delete" or "Show": '
    while basket:
        # Clears the screen.
        clear_screen()
        # Formats and prints a header text.
        print(title('Groups Menu'))
        # Prints additional help information for the group menu.
        help_group()
        command = input(message).casefold()
        if command in BACK_COMMANDS:
            break
        elif command == 'add':
            # Adds a group to the `basket`.
            add_group(basket)
        elif command == 'edit':
            # Allows editing an existing group in the `basket`.
            edited_group(basket)
        elif command == 'delete':
            # Deletes a group from the `basket`.
            deleted_group(basket)
        elif command == 'show':
            # Shows the groups in the `basket`.
            show_group(basket)
            # Pauses execution and waits for user input.
            keep()
