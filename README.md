# Budget Tracker App

Welcome to the Budget Tracker App! This application lets you keep track of your income and expenses and helps you to save by setting budgets and financial goals to work towards. 

## Features

- **Record Expenses And Income** : Add, categorise, date and describe expenses and income.
-  **View Expenses and Income** : View income/expenses over a range of dates, which can also be separated by category. 
-  **Set Budgets** : Determine weekly budgets for any and all expense categories, when the expense categories are viewed the user is told how well they stuck to the budget.
-  **Set Financial Goals** : Add an amount of money you wish to save, the start date of the goal and a description.
-  **View Progress Towards Financial Goals** : See how much you have saved towards your financial goals since their start dates, with encouraging messages to push the user to save more.

  
## Description

This app utilises sqlite3 tables in order to store data about the user's incomings, outgoings, budgets and financial goals, whilst using python to determine their progress towards their goals. 

When adding an income or expense the user will be asked for its name, the category of income/expense that it is, the date of the income/expense and a brief description so that it can be easily recognised later. If the user wishes to view their in/outgoings then they can choose a range of dates to view the records from and all data within this category is presented to the user as well as the total they have spent/gained over this time period. After, the user can then choose to update/delete a record, rename/delete a category or simply carry on. The user can also view all incoming/outgoing in a certain category within a date range.  

The user is able to set and view weekly budgets for each category. When the user views their expenses by category, the category's weekly budget will be divided by 7 and multiplied by the number of days in the viewing date range. If the user is within the relative budget for that time period they will be praised for keeping within the budget, but if they are over budget they will be warned.

The financial goals are target profits to be reached. The goal will have a start date, an amount and a description (such as 'New Washing Machine'). When the progress of these goals is to be viewed, the app will then go through all of the data from the start of the earliest financial goal, until either the next start of financial goal or todays date, whichever comes first. Then, it will determine the profit within that time period, and if the profit is greater than the goal amount, the goal will be shown as completed. However, if there is another goal before todays date, the process will continue but with the next group of profits now being shared between the unfinished goals. This will continue until today's date is reached. Each goal's progression is calculated and then shown to the user along with an encouraging message.
