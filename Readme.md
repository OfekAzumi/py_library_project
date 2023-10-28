
# Library Management System
This project is a simple library management system that allows you to manage books, customers, and loans.
This project is mostly intended for a librarian, made as simple as possible to be sleek, handy, and productive.

* [Getting Started](#getting-started)
* [Running the Project](#running-the-project)
* [Using the Application](#using-the-application)

## Getting Started
**To run the project, you will need to create a virtual environment and install the required dependencies and add-ons.**

### Create a virtual environment
In the terminal, run this code line to create a virtual environment:
``` bash
py -m virtualenv env 
```
### Activate the virtual environment
Now, activate the virtual environment:
``` bash
env\Scripts\activate
```
### Install the required dependencies
Lastly, make sure install the required dependencies:
``` bash
pip install -r requirements.txt
```
## Running the Project
Install the Visual Studio add-on/extension [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) in the extension tab (Ctrl+Shift+X).

**Once you have installed the dependencies, you can run the project using the following command:**

```bash
py app.py
```
***you must run the 'app.py' command to use the project, else, the data won't be transferred.***

**Then, Run the live server:**
``` bash
- Open the 'templates' folder.
- Right-click the 'index.html' file.
- Click 'Open with Live Server'.
```

Now, you can start using the application. 

> **-** An initial run will create a new database that contains no data **at all**.

## Using the Application

The application has three main pages: Books, Customers, and Loans. You can navigate to these pages using the navigation bar at the top of the page.

#### Books Page

* **View all books:** Click the "Books" button to view a list of all books in the library.
* **Filter books:** Type a book name in the text box above the list to filter the books by title.
* **Add a book:** Fill in all the fields in the form above the list and press the "New" button.
* **Edit a book:** Click on a book name to view its information in the text box. You can then change the information and press the "Update" button.
* **Delete a book:** Click on the red "Delete" button next to a book to delete it.

#### Customers Page

* **View all customers:** Click the "Customers" button to view a list of all customers in the library.
* **Filter customers:** Type a customer name in the text box above the list to filter the customers by name.
* **Add a customer:** Fill in all the fields in the form above the list and press the "New" button.
* **Edit a customer:** Click on a customer name to view its information in the text box. You can then change the information and press the "Update" button.
* **Delete a customer:** Click on the red "Delete" button next to a customer to delete it.

#### Loans Page

* **View all loans:** Click the "Loans" button to view a list of all loans, including late loans.
* **View late loans:** Click the "Late Loans" button to view a list of only late loans.
* **Add a loan:** Toggle between the books and customers in the form above the list and press the "New" button to create a new loan.
* **Delete a loan:** Click on the red "Delete" button next to a loan to delete it.
