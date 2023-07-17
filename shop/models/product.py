import logging
from shop.models.group import get_group
from shop.helper.exception import (
    NotNumber,
    ProductNameError,
    ProductDoesExist,
    GroupDoesNotExist,
    ProductDoesNotExist,
)
from shop.helper.const import (
    NO,
    YES,
    BACK_COMMANDS,
    WRONG_COMMANDS,
)
from shop.utils.help_funcs import (
    keep,
    title,
    help_product,
    clear_screen,
    decortor_exceptions,
)

logger = logging.getLogger(__name__)


def get_product_by_index(number: int, basket: dict) -> str | bool:
    """
    Retrieves the product name at the given index from the shopping basket.

    Args:
        number (int): The index of the product to retrieve.
        basket (dict): The dictionary representing the shopping basket.

    Returns:
        str: The product name at the given index, or False if the index is invalid. # noqa E501
    """
    for index, group in enumerate(basket, start=1):
        if index == number:
            return group
    return False


def check_exist(product: str, basket: dict, group: str) -> bool:
    """
    Checks if a product exists in a specific group/category of a shopping basket. # noqa E501

    Args:
        product (str): The product name to check.
        basket (dict): The dictionary representing the shopping basket.
        group (str): The group/category to search for the product.

    Returns:
        bool: True if the product exists in the specified group, False otherwise. # noqa E501
    """
    return product in basket[group]


def get_price_number(word: str) -> int | str | bool:
    """
    Prompts the user to enter a price and converts it to an integer.

    Returns:
        int: The validated price entered by the user.
    """
    if word == 'price':
        message = 'How much is it ? '
    elif word == 'number':
        message = 'How many to have ? '
    number = input(message)
    if number.isnumeric():
        return int(number)
    elif number in BACK_COMMANDS:
        return 'back'
    else:
        return False


def get_product_name(basket: dict, cart_group: str) -> str | bool:
    """
    Prompts the user to enter a product name to add to the shopping list.

    Args:
        basket (dict): The dictionary representing the shopping list.
        cart_group (str): The group/category of the shopping cart.

    Returns:
        str: The validated product name entered by the user.
    """
    messeage = 'Enter the product for add to shopping list: '
    product_name = input(messeage).casefold()
    if product_name in BACK_COMMANDS:
        return 'back'
    elif product_name in WRONG_COMMANDS or product_name.isspace():
        return 'wrong'
    elif product_name.isnumeric():
        return 'int'
    if check_exist(product_name, basket, cart_group):
        return product_name
    else:
        return False


def discount_product() -> int | str:
    message = 'Is there a discount for this product? (Yes/No) '
    message1 = 'How many percent discount should be applied? (1-100) '
    message2 = 'The discount percentage must be a number between 1 and 100.'
    while True:
        discount = input(message).casefold()
        if discount in BACK_COMMANDS:
            return 'back'
        elif discount in YES:
            value = input(message1)
            if value.isnumeric():
                value = int(value)
                if 1 <= value <= 100:
                    return value
                else:
                    print(message2)
                    keep()
                    continue
            else:
                return 'str'
        elif discount in NO:
            return 0


@decortor_exceptions
def added_product(basket: dict) -> None:
    """
    Add a product to the shopping basket.

    Args:
        basket (dict): A dictionary representing the shopping basket.

    Returns:
        None

    This function allows the user to add a product to the shopping basket. It prompts the user for the product details such as group, # noqa E501
    product name, price, and number. The information is then added to the basket dictionary under the corresponding group. # noqa E501
    If any required details are not provided, the function breaks out of the loop and returns. # noqa E501

    Note:
    - The missing functions used within this implementation (e.g., clear_screen, title, show_group, get_group, get_product_name, get_price, get_number, logger.debug, keep) should be implemented or replaced appropriately. # noqa E501
    """
    while True:
        cart_group = get_group(basket)
        if not cart_group:
            break
        clear_screen()
        print(title('Add Product'))
        print('\n-> Use `back` to `Product Menu`\n\n')
        show_product_group(basket, cart_group)

        product_name = get_product_name(basket, cart_group)
        if product_name == 'back':
            break
        elif product_name == 'wrong':
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        elif product_name == 'int':
            logger.warning(f'The name input "{product_name}" must be string.')
            raise ProductNameError('Cannot use int. Please try again...')
        elif not product_name:
            logger.error(f'This "{product_name}" is exist in shopping list.')
            raise ProductDoesExist(
                f'This {product_name} is exist in shopping list.'
            )

        price = get_price_number('price')
        if price == 'back':
            break
        elif not price:
            logger.error(f'Cannot use {number}.just enter int.')
            raise NotNumber(
                f'Cannot use {number}.just enter int. Please try again...'
            )

        number = get_price_number('number')
        if price == 'back':
            break
        elif not price:
            logger.error(f'Cannot use {number}.just enter int.')
            raise NotNumber(
                f'Cannot use {number}.just enter int. Please try again...'
            )

        discount = discount_product()
        if discount == 'back':
            break
        elif discount == 'str':
            logger.error('Cannot use string.just enter integer.')
            raise NotNumber('You must enter the int. Please try again...')

        basket[cart_group].update(
            {product_name: {
                'price': price,
                'number': number,
                'discount': discount
            }}
        )
        logger.debug(f'The "{product_name}" added to shopping list.')
        print(f'The `{product_name}` added to shopping list.')
        keep()


def empty_products(basket: dict) -> bool:
    """
    Check if all items in the given basket are empty.

    Args:
        basket (dict): A dictionary representing the basket with items.

    Returns:
        bool: True if all items in the basket are empty, False otherwise.
    """
    for group in basket:
        if basket[group]:
            return False
    return True


def get_of_product(number: int, basket: dict, group: str) -> str | bool:
    """
    Retrieve an item from the basket dictionary based on the provided number and group. # noqa E501

    Args:
        num (int): The number representing the index of the desired item.
        basket (dict): A dictionary containing groups of items.
        group (str): The key representing the group from which to retrieve the item. # noqa E501

    Returns:
        mixed: The item at the specified index if it exists, False otherwise.

    """

    items = basket.get(group)
    if items:
        if 1 <= number <= len(items):
            for index, product in enumerate(items, start=1):
                if index == number:
                    return product
    return False


def show_product_group(basket: dict, group: str) -> None:
    """
    Display the items in a specific group of a basket.

    Args:
        basket (dict): The dictionary representing the basket of items.
        group (str): The name of the group to display.

    Returns:
        None

    """
    items = basket[group]
    for index, product in enumerate(items, start=1):
        price = items[product]["price"]
        number = items[product]["number"]
        discount = items[product]["discount"]
        print(f'\t{index}: {product} -> Price: {price:,} Number: {number} and discount: {discount}')  # noqa E501
    logger.info(f'Show all products in {group} group')


def show_product(basket: dict) -> str:
    """
    Displays the products in the shopping basket.

    Args:
        basket (dict): A dictionary representing the shopping basket.

    Returns:
        str: The formatted string representation of the products.
    """
    output = ""
    for index, group in enumerate(basket, start=1):
        output += f'{index}: {group}\n'
        for index, product in enumerate(basket[group], start=1):
            price = basket[group][product]["price"]
            number = basket[group][product]["number"]
            discount = basket[group][product]["discount"]
            output += f'\t{index}: {product} -> Price: {price:,} number: {number} and discpunt: {discount}\n'  # noqa E501
    logger.info('Show all products with groups.')
    return output


def get_product_choices(basket: dict, cart_group: str) -> str | bool:
    """
    Displays the product choices for a given cart group and prompts the user to select a product. # noqa E501

    Args:
        basket (dict): A dictionary representing the shopping basket.
        cart_group (str): The name of the cart group in the basket.

    Returns:
        product_name: The selected product name, or False if the user chooses to go back. # noqa E501

    Raises:
        None

    """
    message = 'Please Enter the name product or number product: '
    message1 = 'The "{}" is not exist. Please try again.'
    while True:
        clear_screen()
        show_product_group(basket, cart_group)
        product_choice = input(message).casefold()
        if product_choice in BACK_COMMANDS:
            return 'back'
        elif product_choice in WRONG_COMMANDS or product_choice.isspace():
            return 'wrong'
        if product_choice.isnumeric():
            product_choice = int(product_choice)
            product_name = get_of_product(product_choice, basket, cart_group)
            if not product_name:
                print(message1.format(product_choice))
                keep()
                continue
            else:
                break
        else:
            if product_choice in basket[cart_group]:
                product_name = product_choice
                break
            else:
                print(message1.format(product_choice))
                keep()
                continue
    return product_name


def edited_name(basket: dict, cart_group: str) -> None:
    """
    Edits the name of a product in the shopping basket.

    Args:
        basket (dict): A dictionary representing the shopping basket.
        cart_group (str): The name of the cart group in the basket.

    Returns:
        None

    Raises:
        None

    """
    while True:
        product_name = get_product_choices(basket, cart_group)
        if product_name == 'back':
            break
        elif product_name == 'wrong':
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        new_product = input('Enter the new product: ').casefold()
        if new_product.isnumeric():
            logger.error(f'Cannot use "{new_product}" to add shopping list.')
            raise ProductNameError('Cannot use int to add shopping list.')
        else:
            if new_product in BACK_COMMANDS:
                break
            elif new_product in WRONG_COMMANDS or new_product.isspace():
                logger.error(f'Cannot use {WRONG_COMMANDS}.')
                raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        basket[cart_group][new_product] = basket[cart_group].pop(product_name)
        logger.debug(f'The "{product_name}" edited to {new_product}.')
        clear_screen()
        show_product_group(basket, cart_group)
        keep()
        break


def edited_price_number(basket: dict, cart_group: str, word: str) -> None:
    """
    Edit the price or number of a product in the specified group of the basket dictionary. # noqa E501

    This function prompts the user to choose a product from the specified group and enter a new value for either the price or number. If the input is valid, the corresponding value in the basket dictionary is updated with the new value. If the input is invalid, appropriate error messages are displayed. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501
        cart_group (str): The name of the group containing the product.
        word (str): The word indicating whether it is price or number that needs to be edited. # noqa E501

    Returns:
        None
    """
    message2 = 'The discount percentage must be a number between 1 and 100.'
    while True:
        product_name = get_product_choices(basket, cart_group)
        if product_name == 'back':
            break
        if product_name == 'wrong':
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        new_word = input(f'Enter the new {word}: ').casefold()
        if new_word.isnumeric():
            new_word = int(new_word)
            if word == 'discount':
                if 1 <= new_word <= 100:
                    logger.debug(
                        f'The "{product_name}" edited {word} to {new_word}.'
                    )
                else:
                    print(message2)
                    keep()
                    continue
            basket[cart_group][product_name][word] = new_word
            show_product_group(basket, cart_group)
            keep()
            break
        else:
            if new_word in BACK_COMMANDS:
                break
            else:
                logger.error('just input integer.')
                raise NotNumber('just input int. try again')


@decortor_exceptions
def edited_product(basket: dict) -> None:
    """
    Display a menu for editing a product in the basket dictionary.

    This function displays a menu for editing a product in the specified group of the `basket` dictionary. It prompts the user to choose whether to edit the name, price, or number of the product. Depending on the user's choice, the corresponding editing function is called. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        None
    """
    message = 'What do you want to edit. \
        "Name" or "Price" or "Number" or "discount"? '
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
        clear_screen()
        print(title('Edit Product Menu'))
        show_product_group(basket, cart_group)
        choice = input(message).casefold()
        if choice in BACK_COMMANDS:
            break
        elif choice in WRONG_COMMANDS or choice.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        elif choice == 'name':
            try:
                edited_name(basket, cart_group)
            except ProductNameError as e:
                raise ProductNameError(e)
        elif choice == 'price':
            try:
                edited_price_number(basket, cart_group, choice)
            except NotNumber as e:
                raise NotNumber(e)
        elif choice == 'number':
            try:
                edited_price_number(basket, cart_group, choice)
            except NotNumber as e:
                raise NotNumber(e)
        elif choice == 'discount':
            try:
                edited_price_number(basket, cart_group, choice)
            except NotNumber as e:
                raise NotNumber(e)
        else:
            logger.error(
                'must choice from "Name", "Price", "Number" or "Discount".'
            )
            raise ProductDoesNotExist(
                'must choice from "Name", "Price", "Number" or "Discount"'
            )


def product_menu(basket: dict) -> None:
    """
    Display a menu for managing products in the basket dictionary.

    This function displays a menu for managing products in the `basket` dictionary. It provides options to add, edit, or show products. The user can enter commands to perform these actions. If there are no products in the basket, only the 'add' and 'show' options are available. Otherwise, the 'edit' option is also available. # noqa E501

    Args:
        basket (dict): A dictionary representing the basket with group information. The keys are the names of the cart groups, and the values are the corresponding group information. # noqa E501

    Returns:
        None
    """
    message = 'Enter your command "Add" or "Edit" or "Show": '
    message1 = 'Enter your command "Add" or "Show": '
    while True:
        clear_screen()
        print(title('Products Menu'))
        help_product()
        if empty_products(basket):
            command = input(message1).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'add':
                added_product(basket)
            elif command == 'show':
                print(show_product(basket))
                keep()
        else:
            command = input(message).casefold()
            if command in BACK_COMMANDS:
                break
            elif command == 'add':
                added_product(basket)
            elif command == 'edit':
                edited_product(basket)
            elif command == 'show':
                print(show_product(basket))
                keep()
