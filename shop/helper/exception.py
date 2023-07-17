class ShopError(Exception):
    ...


class GroupNameError(ShopError):
    ...


class GroupDoesNotExist(ShopError):
    ...


class ProductDoesNotExist(ShopError):
    ...


class ProductNameError(ShopError):
    ...


class ProductDoesExist(ShopError):
    ...


class NotNumber(ShopError):
    ...
