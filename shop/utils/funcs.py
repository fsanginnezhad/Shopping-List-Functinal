import logging
from difflib import SequenceMatcher
from shop.models.group import get_group_by_product_name
from shop.helper.exception import (
    ProductNameError,
    GroupDoesNotExist,
    ProductDoesNotExist,
)
from shop.helper.const import (
    BACK_COMMANDS,
    WRONG_COMMANDS,
)
from shop.models.product import (
    get_group,
    get_product_choices,
)
from shop.utils.help_funcs import (
    keep,
    title,
    clear_screen,
    decortor_exceptions,
)

logger = logging.getLogger(__name__)


@decortor_exceptions
def add_to_list(basket: dict, shopping_list: dict) -> None:
    """
    Add products from the basket to the shopping list.

    Args:
        basket (dict): The basket dictionary containing product groups and their details. # noqa E501
        shopping_list (dict): The shopping list dictionary containing product names and quantities. # noqa E501

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
        clear_screen()
        print(title('Adding to Shopping List Menu'))
        product_name = get_product_choices(basket, cart_group)
        if product_name == 'back':
            break
        if product_name == 'wrong':
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')
        numbers = input('How many of product: ').casefold()
        if numbers.isnumeric():
            numbers = int(numbers)
            number = basket[cart_group][product_name]['number']
            if number > 0 and numbers <= number:
                if product_name not in shopping_list:
                    logger.info(f'The "{product_name}" added to shopping list with "{numbers}" quantity.')  # noqa E501
                    shopping_list.update({product_name: numbers})
                elif product_name in shopping_list:
                    logger.info(f'The shopping list "{product_name}" is updated with quantity -> "{numbers}".')  # noqa E501
                    shopping_list[product_name] += numbers
                number -= numbers
                logger.info(f'There are "{number}" "{product_name}" left in the basket.')  # noqa E501
                basket[cart_group][product_name]["number"] = number
                print(f"There are '{number}' '{product_name}' left in the warehouse.")  # noqa E501
                keep()
                continue
            else:
                logger.warning(
                    f'Sorry, the "{product_name}" \
                        product has only "{number}" items in stock.'
                )
                raise ProductDoesNotExist(
                    f'Sorry, the "{product_name}" \
                        product has only "{number}" items in stock.'
                )
        elif numbers in BACK_COMMANDS:
            break
        elif numbers in WRONG_COMMANDS or numbers.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductNameError(f'Cannot use {WRONG_COMMANDS}')


def show_list(shopping_list: dict) -> None:
    """
    Display the products in the shopping list.

    Args:
        shopping_list (dict): The shopping list dictionary containing product names and quantities. # noqa E501

    Returns:
        None
    """
    clear_screen()
    print(title('Show Products In Shopping List'))
    if shopping_list:
        for index, item in enumerate(shopping_list, start=1):
            print(f"{index}: {item} {shopping_list[item]}")
    else:
        print('Shopping list is Empty.')


def get_product_shopping_list(shopping_list: list, number: int) -> str | bool:
    """
    Return the product name at the specified index in the shopping list.

    Args:
        shopping_list (list): The list of products.
        number (int): The index of the desired product (1-based indexing).

    Returns:
        str: The name of the product at the specified index, or False if the index is out of range. # noqa E501
    """
    for index, product in enumerate(shopping_list, start=1):
        if number == index:
            return product
    return False


def delete_from_list(shopping_list: list, basket: dict) -> None:
    """
    Deletes products from the shopping list and updates the basket.

    Args:
        shopping_list (list): The list of products.
        basket (dict): The dictionary representing the basket.

    Returns:
        None
    """
    message = 'Choice and use name or number product: '
    while True:
        clear_screen()
        if not shopping_list:
            show_list(shopping_list)
            keep()
            break
        show_list(shopping_list)
        product_choice = input(message).casefold()
        if product_choice in BACK_COMMANDS:
            break
        elif product_choice in WRONG_COMMANDS or product_choice.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductDoesNotExist(f'Cannot use {WRONG_COMMANDS}')
        elif product_choice.isnumeric():
            product_choice = int(product_choice)
            product_choice = get_product_shopping_list(
                shopping_list, product_choice
            )
            if not product_choice:
                logger.warning(f'The "{product_choice}" not exist in basket.')
                raise ProductDoesNotExist(
                    f'The {product_choice} not exist in basket.'
                )
            cart_group = get_group_by_product_name(product_choice, basket)
        else:
            if product_choice in shopping_list:
                cart_group = get_group_by_product_name(product_choice, basket)
            else:
                logger.warning(
                    f'The "{product_choice}" is not in shopping list.'
                )
                raise ProductDoesNotExist(
                    f'The {product_choice} is not in shopping list.\
                        Please try again'
                )
        numbers = input('How many of product to delete: ').casefold()
        if numbers.isnumeric():
            numbers = int(numbers)
            if (shopping_list[product_choice] - numbers) < 0:
                logger.warning('The number of requests to delete is greater than the number available. Please try again...')  # noqa E501
                raise ProductDoesNotExist('The number of requests to delete is greater than the number available. Please try again...')  # noqa E501
            elif (shopping_list[product_choice] - numbers) == 0:
                shopping_list.pop(product_choice)
            elif shopping_list[product_choice] > numbers:
                shopping_list[product_choice] -= numbers
                basket[cart_group][product_choice]["number"] += numbers
            else:
                logger.warning(
                    "I'm sorry. Enter just the number."
                )
                raise ProductNameError(
                    "I'm sorry. Enter just the number.Please try again..."
                )
        elif numbers in BACK_COMMANDS:
            break
        elif numbers in WRONG_COMMANDS or numbers.isspace():
            logger.error(f'Cannot use {WRONG_COMMANDS}.')
            raise ProductDoesNotExist(f'Cannot use {WRONG_COMMANDS}')


def total_counter(shopping_list: list, basket: dict, invoice: list) -> None:
    """
    Calculates the total count and price of items in the shopping list based on the basket dictionary, # noqa E501
    and adds the product details to the invoice.

    Args:
        shopping_list (list): The list of products to be counted.
        basket (dict): The dictionary containing the groupings of products and their prices. # noqa E501
        invoice (list): The invoice list to which the product details will be added. # noqa E501

    Returns:
        None

    Modifies the invoice list by adding the product details (product name, number, and price) for each item # noqa E501
    in the shopping list. The price is obtained from the basket dictionary based on the product's group. # noqa E501

    Note:
    The function assumes the existence of a helper function 'get_group_by_product_name' that takes the product name and the basket dictionary as inputs # noqa E501
    and returns the group of the product.

    """
    for product in shopping_list:
        product_name = product
        number = shopping_list[product]
        cart_group = get_group_by_product_name(product_name, basket)
        price = basket[cart_group][product_name]['price']
        discount = basket[cart_group][product_name]['discount']
        final_list(product_name, number, price, invoice, discount)


def final_list(
        product_name: str,
        number: int,
        price: int,
        invoice: list,
        discount: int | bool
) -> None:
    """
    Adds the product details (product name, number, and price) to the invoice list. # noqa E501

    Args:
        product_name (str): The name of the product.
        number (int): The number of products.
        price (int): The price per product.
        invoice (list): The invoice list containing the product details.

    Returns:
        None

    Modifies the invoice list by adding the new product details if it does not already exist in the invoice. # noqa E501
    """
    invoice_list = [product_name, number, price, discount]
    if invoice_list not in invoice:
        invoice.append(invoice_list)


def final_invoice(invoice: list, total: int) -> None:
    """
    Calculates the final invoice based on the provided invoice items and updates the total. # noqa E501

    Args:
        invoice (list): The list of invoice items. Each item is a tuple containing the product name, # noqa E501
            number of products, and price per product.
        total (int): The current total amount of the invoice.

    Returns:
        None

    Prints the detailed breakdown of each item in the invoice and the final invoice summary. # noqa E501
    """

    numbs = 0
    for item in invoice:
        product_name, number, price, discount = item
        numbs += number
        if not discount:
            final_invoice = number * price
            print(f'{product_name} -> {number} x {price:,} = {final_invoice:,}')  # noqa E501
        else:
            final_invoice = (price - ((price * discount) // 100)) * number
            print(f'{product_name} -> {number} x {price:,} - {discount}% = {final_invoice:,}')  # noqa E501
        total += final_invoice

    print('----------------------------------------------------')
    print(f'Products -> {numbs} Final Invoice -> {total:,}T')


def similarity(actual: str, expected: str) -> float:
    """
    Computes the similarity ratio between two strings.

    Args:
        actual (str): The actual string.
        expected (str): The expected string.

    Returns:
        float: The similarity ratio between 0 and 1.
    """
    return SequenceMatcher(None, actual, expected).ratio()


def search_in_list(shopping_list: dict, word: str) -> str:
    """
    Searches for a word in the shopping list and displays the search results.

    Args:
        shopping_list (dict): The dictionary representing the shopping list.
        word (str): The word to search for.

    Returns:
        str: A message indicating the search results.
    """
    print(f'Search for {word}...')
    results = [
        (product, similarity(product, word))
        for product in shopping_list
        if word.casefold() in product.casefold()
    ]
    if results:
        print(f'Found ({len(results)}) results:')
        for product, score in results:
            print(f'Product: {product}, Similarity Score: {score:.2f}')
    else:
        print('No result Found.')
