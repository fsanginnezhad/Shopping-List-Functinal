# Shopping List Project

This is a Python project that implements a shopping list application. The application allows users to create a new shopping list, add products to it, remove products from it, and display the list of products in the basket. The application also allows an admin user to manage, add, edit, and delete groups and products. Users can select and buy products for their product basket with a final payable invoice presented at the end.

## Project Structure

The project is organized into several folders and files, which are described below:

- `conf/`:
  - `log.py`: This file manages and sets the configuration log for the project.

- `core/`:
  - `app.py`: This file contains the main logic for the application. It handles user inputs, calls the necessary functions from the `utils` folder, and displays the output to the user.

- `shop/`:
  - `utils/`: This folder contains all the functions used in the app. Functions such as adding products to the basket, removing products, and displaying the final invoice are defined here.

  - `models/`: This folder contains the product basket models, groupings, and products with their details. Additionally, it contains the admin model for managing, adding, editing, and deleting groups and products.

  - `helper/`: This folder defines constant variables for the project, such as product prices and tax rates.

- `run.py`: This is the main file that runs the program. Every command is sent to the desired file, and the program executes the corresponding function.

## How to Run the Program

To run the program, follow these steps:

1. Clone the repository from GitHub: `git clone https://github.com/fsanginnezhad/Shopping-List-Functional.git`.

2. Navigate to the project directory: `cd Shopping-List-Functional`

3. Run the program: `python run.py`

## Usage

When you run the program, you will be prompted to enter a command. Here is an overview of the available commands:

- `add`: Adds a product to the shopping list. You will be prompted to enter the product name, quantity, and price.

- `remove`: Removes a product from the shopping list. You will be prompted to enter the product name.

- `edit`: Edit a product from the shopping list. you will be prompted to enter the product name.

- `show`: Displays the list of products in the shopping basket, along with the subtotal, tax, and total payable amount.

If you are an admin user, you can use the following additional commands:

- `add_group`: Adds a new product group.

- `edit_group`: Edits an existing product group.

- `delete_group`: Deletes an existing product group.

- `add_product`: Adds a new product to an existing group.

- `edit_product`: Edits an existing product.

- `delete_product`: Deletes an existing product.

## preview

![Capture](https://github.com/fsanginnezhad/Shopping-List-Functinal/assets/73942999/041bc099-8281-465a-b0ed-5649e4414847)

## Credits

This project was created by `Farshad Sanginnezhad`. If you have any questions or feedback, please feel free to contact me.
