**# Book Manager**



**Laboratory project for the course "Professional Python".**



**## Description**



**Book Manager is a console Python application for managing a collection of books.**



**For each book the program stores:**



**\* title;**

**\* author;**

**\* publication year;**

**\* number of pages.**



**The program supports:**



**\* adding a book;**

**\* searching books by author;**

**\* filtering books by publication year;**

**\* finding the largest book;**

**\* calculating the average number of pages;**

**\* sorting books by number of pages.**



**## Requirements**



**Python 3.11+**



**## Installation**



**Create a virtual environment:**



**```text**

**python -m venv .venv**

**```**



**Activate the virtual environment.**



**Install the project:**



**```text**

**python -m pip install -e .**

**```**



**## Run**



**Run as a module:**



**```text**

**python -m book\_manager.main**

**```**



**or use the console command:**



**```text**

**book-manager**

**```**



**## Project structure**



**```text**

**src/book\_manager/models.py**

**```**



**Data model for books.**



**```text**

**src/book\_manager/services.py**

**```**



**Business logic of the application.**



**```text**

**src/book\_manager/main.py**

**```**



**Application entry point and console menu.**



**## Example**



**```text**

**BOOK MANAGER**

**=============================================**

**1. Show all books**

**2. Add book**

**3. Find books by author**

**4. Filter books by year**

**5. Find the largest book**

**6. Calculate average number of pages**

**7. Sort books by pages**

**8. Exit**

**=============================================**



**Select command: 5**



**Largest book:**

**Title: 1984**

**Author: George Orwell**

**Year: 1949**

**Pages: 328**

**```**



**## Author**



**Student: Boichuk Karyna**



**Group: FEP-33**



