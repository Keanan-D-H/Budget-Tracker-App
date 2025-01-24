###Expense_Budget_Tracker_app.py###
"""
Keanan Hinchliffe, 13/09/2024

A program to create an expense and budget tracker app using SQLite. 
Please ensure the income_expense_goals.csv is in your workspace if you
wish to populate the tables.
"""
# IMPORT LIBRARIES
import sqlite3
import datetime
import csv
from operator import itemgetter


# FUNCTION DEFINITIONS

def check_number(number, number_type): 
    """
    check_number tries to change an input to an int or a float, if it can't
    it will ask for input until it can.

    Parameters: number : str
                    A string which should be an integer value.
                number_type : str
                    Either "int" or "float" to determine if item should 
                    be of type int or float respectively

    Returns:    number : int/float
                    A user chosen value which is either an integer or a float. 
    """
    if number_type == "int":
        while type(number) != int:
            try:
                number = int(number)

            except:  
                number = input("That is not an integer. Please input again.\n")

    elif number_type == "float":
        while type(number) != float:
            try:
                number = float(number)
            except:
                number = input("That is not a number. Please input again.\n")
    return number


def check_character_length(string, char_limit):
    """
    check_character_length checks the character length of a string and 
    if it is longer than the character limit, the user is asked to input
    a new string.

    Parameters  :   string : str
                        The string to be checked. 
                    char_limit : int
                        The character limit the string should adhere to.
    
    Returns     :   string : str
                        A string which has a character length below the 
                        character limit.
    """
    while len(string) > char_limit:
        string = input(f"There is a character limit of {char_limit}."
              + "Please input again.\n")
        
    return string


def check_in_range(number, upper_value, lower_value):
    """
    check_in_range checks if an int is within a given range and will ask
    for a new input until it falls within the range.

    Parameters: number : str 
                    The string to be converted to an integer and checked if it
                    is in the allowed range
                upper_value : int 
                    The highest value 'item' can be
                lower_value : int 
                    The lowest value 'item' can be

    Returns:    number : int 
                    A user chosen integer within range.
    """
    while True:

        number = check_number(number, "int")

        if number > upper_value or number < lower_value:
        
            number = input(f"Please input an integer between {lower_value}"
                     + f" and {upper_value}.\n")
            
        else :
            return number


def check_yes_no(answer):
    """
    Checks if the inputted string is either a yes or a no and asks for an
    input until it is then returns the result.

    Parameters: answer : str
                    A string which should either be yes or no

    Returns:    answer.lower() : str 
                    Either "yes" or "no"        
    """
    while answer.lower() !='yes' and answer.lower() != 'no':
        answer = input ('Please only put in \'yes\' or \'no\':\n')

    return answer.lower()


def budget_for_category_over_date(category, start_date, end_date):
    """
    budget_for_category over date finds the weekly budget of a category 
    from the Budget table and then finds out what the budget would be 
    for that catgeory between the determined start and end date.
    
    Parameters  :   category : str
                        The name of the category which has the budget.
                    start_date : datetime.date
                        The start date of the 'Expenses' table search.
                    end_date : datetime.date
                        The end date of the 'Expenses' table search. 

    Returns     :   budget_over_date : float | NoneType
                        Either how much the budget is for the category over
                        the date range, or None if no budget has been set 
                        for that category.     
    """

    cursor.execute('''SELECT budget FROM Budget WHERE category = ?''', 
                   (category,))
    budget_tuple = cursor.fetchone()
    db.commit()

    if budget_tuple != None:
        (budget,) = budget_tuple
        no_of_days = (end_date - start_date)
        no_of_days = no_of_days.days

        budget_over_date = budget * (no_of_days) / 7
        budget_over_date = round(budget_over_date,2)
    
    else:
        budget_over_date = None
    
    return budget_over_date


def display_as_table(table_name, record_list):
    """
    display_as_table displays data from record_list as a table to the user.
    The headings of the table corresepond with the table the data represents.
    If the record_list contains multiple records (in a list of lists format)
    then it goes through each record and prints them. 


    Parameters  :   table_name : str
                        The name of the table which the data represents.
                    record_list : list
                        Either a list of records or a single record which 
                        is in the format [date, amount, category,
                        description, id] for the 'Income' and 'Expenses' 
                        tables, [category, budget] for the Budget table
                        or [date, amount, description, id] for the Goals
                        table. 

    Returns     :
    """
    print("\n")

    # Income and Expenses tables. 
    if table_name == "Income" or table_name == "Expenses":
        print('{:^8}|{:^14}|{:^12}|{:^16}|{:^36}'.format("I.D.","Date",
                                    "Amount (£)", "Category","Description"))
        print("---------------------------------------------------------"
            + "-----------------------------")
        
        if type(record_list[0]) == tuple or type(record_list[0]) == list:
            for record in record_list:
                
                date = str(record[0])
                amount =  f"{record[1]:.2f}"
                category = record[2]
                description = record[3]
                id_ = str(record[4])

                print('{:^8}|{:^14}|{:^12}|{:^16}|{:^36}'.format(id_, date, 
                                            amount, category,description))
        
        else:
            date = str(record_list[0])
            amount =  f"{record_list[1]:.2f}"
            category = record_list[2]
            description = record_list[3]
            id_ = str(record_list[4])

            print('{:^8}|{:^14}|{:^12}|{:^16}|{:^36}'.format(id_, date, 
                                            amount, category,description))


    # Budget table.
    elif table_name == "Budget":
        print('{:^16}|{:^16}'.format("Category","Budget (£)"))
        print("---------------------------------")
        
        if type(record_list[0]) == tuple or type(record_list[0]) == list:
            for record in record_list:
                 
                category = record[0]
                budget =  f"{record[1]:.2f}"

                print('{:^16}|{:^16}'.format(category, budget))
        
        else:
            category = record_list[0]
            budget =  f"{record_list[1]:.2f}"

            print('{:^16}|{:^16}'.format(category, budget))
            
    # Goals table.
    elif table_name == "Goals":
        print('{:^8}|{:^12}|{:^12}|{:^36}'.format("I.D.", "Start Date", 
                                                "Amount (£)", "Description"))
        print("---------------------------------------------------------"
              + "------")
        
        if type(record_list[0]) == tuple or type(record_list[0]) == list:

            for record in record_list:
                date = str(record[0])
                amount =  f"{record[1]:.2f}"
                description = record[2]
                id_ = str(record[3])

                print('{:^8}|{:^12}|{:^12}|{:^36}'.format(id_, date, amount, 
                                                        description))
        
        else:
            date = str(record_list[0])
            amount =  f"{record_list[1]:.2f}"
            description = record_list[2]
            id_ = str(record_list[3])

            print('{:^8}|{:^12}|{:^12}|{:^36}'.format(id_, date, amount,
                                                        description))   
    print("\n")
    return
       

def add_to_table(table_name, record_data, multiple):
    """
    add_to_table takes the data from the record_data list and adds it to 
    the table determined by table_name. Then the id of each new record is
    found by selecting the largest id from the table after all the records
    are added and then reducing and adding it to each record according to
    when it was added to the table. It also informs the user that 
    the record has been inserted into the table utilising the
    display_as_table function. 

    Parameters  :   table_name : str
                        The name of the table which the record will be 
                        added to.
                    record_data : list
                        A list containing a record of a Income, an Expense or
                        a Goal or a list of multiple records, each record as 
                        their own list. For an income or expense a record  
                        list is formatted as [date,amount,category,
                        description], for a budget it will be [category,budget]
                        and for a goal it will be [date,amount,description]
                    multiple : str
                        Either "yes" or "no", which indicates multiple 
                        records or a single record respectively.

    Returns     :    
    """
    # Income and Expenses tables.
    if table_name == "Income" or table_name == "Expenses":

        if multiple == "yes":

            cursor.executemany(f''' INSERT INTO {table_name}(date, amount, 
                        category, description) VALUES(?,?,?,?)''',
                        record_data)
            db.commit()

            cursor.execute(f'''SELECT MAX(id) FROM {table_name}''')
            (max_id,) = cursor.fetchone()
            db.commit()
            
            counter = 1

            for record in record_data:
                record.append(max_id - (len(record_data) - counter))
                counter += 1
        
        elif multiple == "no":
            cursor.execute(f''' INSERT INTO {table_name}(date, amount, 
                        category, description) VALUES(?,?,?,?)''',
                        record_data)
            db.commit()

            cursor.execute(f'''SELECT MAX(id) FROM {table_name}''')
            (max_id,) = cursor.fetchone()
            db.commit()

            record_data.append(max_id)

        # The data which will be used in display_as_table.
        inform_user_records = record_data


    # Budget table.
    elif table_name == "Budget":
        # As we only want to allow one budget for any one category,
        # we use the 'IGNORE' keyword here so only the first budget.
        if multiple == "yes":
            cursor.executemany(f''' INSERT or IGNORE INTO 
            Budget(category, budget) VALUES(?,?)''', record_data)
            db.commit()


        elif multiple == "no":
            cursor.execute(f''' INSERT or IGNORE INTO
            Budget(category, budget) VALUES(?,?,?,?)''', record_data)
            db.commit()      

        # As we may ignore values we only want to inform the user we have
        # added a record to the table if it is actually in the table.
        # find all the records in the table and check them against the 
        # records we tried to add.
        cursor.execute('''SELECT * FROM Budget''')
        budget_records = cursor.fetchall()
        db.commit()
        inform_user_records = []

        for record in record_data: 
            if tuple(record) in budget_records:
                inform_user_records.append(record)


    # Goals table. 
    elif table_name == "Goals":

        if multiple == "yes":

            cursor.executemany(f''' INSERT INTO Goals(date, amount, 
                        description) VALUES(?,?,?)''',record_data)
            db.commit()

            cursor.execute(f'''SELECT MAX(id) FROM {table_name}''')
            (max_id,) = cursor.fetchone()
            db.commit()
            
            counter = 1

            for record in record_data:
                record.append(max_id - (len(record_data) - counter))
                counter += 1
        
        elif multiple == "no":
            cursor.execute(f''' INSERT INTO Goals(date, amount, 
                        description) VALUES(?,?,?)''', record_data)
            db.commit()

            cursor.execute(f'''SELECT MAX(id) FROM {table_name}''')
            (max_id,) = cursor.fetchone()
            db.commit()

            record_data.append(max_id)
        
        inform_user_records = record_data

    # Display the data added to the tables to the user.
    if len(inform_user_records) != 0:
        print(f"\nThe following data has been added to the {table_name} "
              + "table:")  
        display_as_table(table_name,inform_user_records)
    

def ask_for_amount_in_pounds():
    """
    ask_for_amount_in_pounds asks the user to input an monetary amount. It
    then checks if the user has inputted a valid number which is to no more 
    than two decimal places. If the number inputted value is not valid it 
    will ask the user to input a valid number. Once a valid number has been 
    inputted it will ask the user if they are happy with their input. If 
    they aren't they will be asked to input the correct amount. Once they 
    are happy it will return the user's chosen amount. 


    Parameters: 

    Returns: amount_float : float
                A user chosen amount of money.     
    """

    amount = input("\nPlease input the amount (£): \n")

    while True: 
        amount_float = check_number(amount, "float")
        amount_float = check_in_range(amount, 999999.99, 0)
        rounded_amount = round(amount_float,2)

        if amount_float == rounded_amount:
            is_correct = input(f"\nIs £{amount_float:.2f} the correct"
                               + " amount?\n")
            is_correct = check_yes_no(is_correct)

            if is_correct == 'no': 
                amount = input("\nPlease insert the correct amount (£):\n")
                
            else:
                return amount_float

        else:
            amount= input("Please only input an amount to 2 decimal" +
                          " places (£):\n")
            

def ask_for_date():
    """
    ask_for_date asks the user if they want to use the current date, if so 
    it returns the current date. If the user wants to input a date, 
    ask_for_date asks the user for a day, a month and a year. It then checks 
    if the inputs could be an true date. ask_for_date checks with the user if
    they have inputted the date they desired. 

    Parameters: -

    Returns: start_date : str
                    The date the user wishes to input.     
    """
    while True:

        today_or_not = input("\nWould you like to use today's date?\n")
        today_or_not = check_yes_no(today_or_not)

        if today_or_not == 'yes':
            start_date = str(datetime.date.today())
            return start_date

        year = input("\nEnter the year (YYYY):\n")
        year = check_in_range(year,2025, 2020)

        month = input("\nEnter the month (MM):\n")
        month = check_in_range(month, 12, 1)

        day = input("\nEnter the day (DD):\n")
        day = check_in_range(day, 31, 1)
        
        try: 

            start_date = datetime.date(year, month, day)
            print(f"\n\n{start_date}\n")
            is_correct = input("Is the date above the correct date "
                               + "(YYYY-MM-DD)?\n")

            if check_yes_no(is_correct) == 'yes':
                return str(start_date)

        except ValueError: 
            print("Unfortunately this is not a valid date. Please try "
                  + "again.\n")


def retrieve_categories(table_name, show_or_not):
    """
    retrieve_categories finds all the categories found in the table. If
    the categories are to be shown, the 'Misc' category is not retrieved
    as the 'Misc' category will be shown whether it is in the table or not.

    Parameters  :   table_name : str
                        The name of the table from which the categories 
                        will be retrieved.
                    show_or_not : str
                        A show_or_not of "show" will mean the 'Misc' 
                        category will be omitted. 
    
    Returns     :   categories : list
                        A list of the categories in tuples in the table. 
    
    """

    if show_or_not == "show":
        cursor.execute(f''' SELECT DISTINCT category from {table_name}
                        WHERE category != ? ORDER BY category''', ('Misc',))
        categories = cursor.fetchall()
        db.commit()
    
    else:
        cursor.execute(f'''SELECT DISTINCT category from {table_name}
                        ORDER BY category''')
        categories = cursor.fetchall()
        db.commit()

    return categories


def show_categories(table_name, menu_choice, delete_category = None):
    """
    show_categories collects all the distinct entries in the category 
    column in the chosen table and presents them to the user. The user
    then chooses which category they would like to select. The Misc 
    category is presented whether there is a Misc category in the table 
    or not. It is also either presented last or second from last if there
    is the option to add a new category. If the user is adding a new
    record to the table then they are given the choice to add a new 
    category. The function then returns all the categories in a list 
    oredered as they were presented as well as the choice of the user. 

    Parameters  :   table_name
                        The name of the table to be searched.
                    menu_choice
                        The menu choice from the main code which determines
                        if the user can add a new category
                    delete_category : str | NoneType
                        If this function is used for deleting a category
                        Misc will be omitted from the offering as Misc 
                        is what deleted categories are converted to.


    Returns     :   category_list
                        The list of categories in the order they were 
                        presented followed by the user's choice of category 
                        in the form of a number : int.    
    """

    counter = 1
    category_list = []

    categories = retrieve_categories(table_name, "show")

    print(f"\nPlease choose one of the following categories: ")

    for category_tuple in categories:
        
        (category,) = (category_tuple)
        if category != "Misc":
            print(f"{counter}. {category}")
            category_list.append(category)
            counter += 1

    if delete_category == None:
        print(f"{counter}. Misc")
        category_list.append("Misc")
    
    if menu_choice == "1" or menu_choice == "4" or menu_choice == "9":

        counter += 1
        print(f"{counter}. Add a new category")
        category_list.append("Add a new category")

    category_choice = check_in_range(input("\n"),counter,1)

    category_list.append(category_choice)


    return category_list
    

def ask_for_category(table_name, menu_choice, delete_category = None):
    """
    ask_for_category uses the show_categories function to ask the user which
    they want. If the user wishes to add a new category it asks them 
    what they would like it to be called. It then checks if that name is
    taken by one of the other categories. If it is, it will ask the user 
    if they wish to use this name, in which case it does, or if they would
    like to rename it, in which case they are asked again to name it. If 
    the user opted for one of the pre-existing categories, that category 
    is chosen and retuned.

    Parameters :    table_name : str
                        The name of the table the category will be used for.
                    menu_choice : str
                        The menu option chosen in the main code.
                    delete_category : str | NoneType
                        This will be filled when ask_for_category is used
                        to delete a category so that show_category does 
                        not show Misc as an option. 
    
    Returns :       category_choice : str
                        The category the user wishes to add.

    """
    if delete_category == None:
        category_list = show_categories(table_name, menu_choice)

    else:
        category_list = show_categories(table_name, menu_choice,"delete")

    # The index of the chosen category = the final list value - 1. 
    if category_list[category_list[-1] - 1] == "Add a new category" : 
        
        while True:

            new_category = input("\nPlease input the new category name:\n")
            new_category = check_character_length(new_category, 15)
            # Remove blank space, single and double quotation marks. 
            new_category = new_category.strip().strip("\'").strip("\"").title()

            if new_category not in category_list and new_category != "Misc":
                is_correct = input(f"\nIs \'{new_category}\' correctly"+
                                   " inputted?\n")
                is_correct = check_yes_no(is_correct)

                if is_correct == "yes":
                    category_choice = new_category
                    break

                else:
                    continue
            
            else: 
                print(f"Unfortunately \'{new_category}\' is already a "+
                      "category.")
                use_category = input(f"\nWould you like to use {new_category}"
                                     + "?\n")
                use_category = check_yes_no(use_category)

                # If the user wishes to use the 
                if use_category == "yes":
                    category_choice = new_category
                    break

                else:
                    print("\nWe will now ask you to rename the category.")

    else: 
        category_choice = category_list[category_list[-1] - 1]
    
    return category_choice


def retrieve_income_expense(table_name, start_date, end_date, 
                        category = None):
    """
    retrieve_income_expense fetches all the records which take place between
    two dates and returns them. If there is a specific category, it will only
    fetch records which have that category label.

    Parameters  :   table_name : str
                        The name of the table which the records will be 
                        fetched from. 
                    start_date : datetime
                        The earliest date a fetched record can be from.
                    end_date : datetime
                        The lastest date a fetched record can be from.
                    category : str
                        The name of the category which they are searching by.


    Returns     :   records : list
                        A list of tuples containing the (date, amount, 
                        category, description) from each fetched record. 
    """
    if category == None:
        cursor.execute(f'''
        SELECT date, amount, category, description, id FROM {table_name}
        WHERE date BETWEEN ? and ? 
        ORDER BY date, category''', (start_date, end_date))
        records = cursor.fetchall()
        db.commit()

    else: 
        cursor.execute(f'''
        SELECT date, amount, category, description, id FROM {table_name}
        WHERE category = ?  AND date BETWEEN ? AND ?
        ORDER BY date, category''',
        (category, start_date, end_date))
        records = cursor.fetchall()
        db.commit()

    return records


def ask_for_description():
    """
    ask_for_description asks the user to input a description for a given 
    record. 

    Parameters  :   

    Returns     :   description : str
                        The description of record.
    """
    while True:
        
        description = input("\nPlease provide a brief description:\n")
        description = check_character_length(description, 35)

        print(f"\n\"{description}\"")
        is_correct = input(f"Is the description above correct?\n")

        is_correct = check_yes_no(is_correct)

        if is_correct == "yes":
            return description

        else: 
            continue


def ask_for_record_data(table_name, menu_choice): 
    """
    ask_for_record_data uses the ask_for_date, ask_for_amount_in_pounds, 
    ask_for_category, ask_for_description functions to get the date, amount,
    category and description of a new record from the user. 

    Parameters  :   table_name : str
                        The name of the table the information is used for.
                        Either 'Income' or 'Expenses'. 
                    menu_choice : str
                        The menu choice chosen in the main code. 

    Returns     :   record_data : list
                        A list containing the record of an income, expense
                        or a goal. If the record is from an income or expense
                        the list is in the format [date, amount, category, 
                        description], if the record is for a budget the 
                        record_data is in the format [category, amount]
                        and if the record is for a goal the format is 
                        [date, amount, description]
    """
    
    if table_name == "Expenses" or table_name == "Income":
        date = ask_for_date()
        amount = ask_for_amount_in_pounds()
        category = ask_for_category(table_name, menu_choice)
        description = ask_for_description()
    
        record_data = [date, amount, category, description]
    

    elif table_name == "Budget":

        print("\nWe will now ask you which category you would like to set" 
              +  "a budget for.")
        category = ask_for_category("Expenses", menu_choice)

        print(f"\nWe will now ask you the weekly budget for \'{category}\'.")
        budget = ask_for_amount_in_pounds()

        record_data = [category, budget]


    elif table_name == "Goals":
        print("We will now ask you to enter the date this goal starts.")
        date = ask_for_date()
        print("\nNow we will ask what your goal amount is.")
        amount = ask_for_amount_in_pounds()
        description = ask_for_description()

        record_data = [date, amount, description]

    return record_data


def ask_for_date_range ():
    """"
    ask_for_date_range asks the user the time range in which they
    would like to view the records and starting from what date. 

    Parameters  :

    Returns     :   date_range : list
                        A list consisting of the start_date of the search 
                        and the end_date of the search   
    """

    print("\nWe will now ask you the earliest date you would like to start "
          + "viewing from")
    start_date = ask_for_date()
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
   


    no_of_days = input("""\nPlease input the number of days in which you would
like to look over. Please pick a number of days between 1 and 30.\n""")
        
    no_of_days = check_in_range(no_of_days,30,1)   
    
    # We take 1 away as we will use the BETWEEN operator which is inclusive.
    end_date = start_date + datetime.timedelta(days = no_of_days -1)

    date_range = [start_date, end_date]

    return date_range


def calculate_total(record_list):
    """
    calculate_total calculates the total amount in a list of records
    where the amount of each record is at index 1. 

    Parameters  :   record_list : list
                        A list of records where each record has their amount 
                        at index 1
    
    Returns     :   total : float
                        The amounts of each recored summed together.   
    """

    total = 0 

    for record in record_list:
        total += record[1]
    
    return total


def display_total(table_name, record_list, date_range, category = None): 
    """
    display_total finds the total of all the amounts in a collected list of 
    records and displays the result to the user. 
    
    Parameters  :   table_name : str
                        The name of the table the data was fetched from. 
                    record_list : list
                        A list containing records with each record being 
                        in the format [date, amount, category, description].
                    date_range : list
                        A list containing the start and end dates which the 
                        records take place over. 

    Returns     :   
    """
    total = calculate_total(record_list)

    if table_name == "Income":
        print(f"\nBetween {date_range[0]} and {date_range[1]} you have earned"
            + f" a total of £{total:.2f}")
        
        if category != None:
            print (f"in the \'{category}\' category.")
        
        
    elif table_name == "Expenses":
        print(f"Between {date_range[0]} and {date_range[1]} you have spent"
              + f" a total of £{total:.2f}.")
        
        if category != None: 
            budget = budget_for_category_over_date(category,date_range[0],
                                                   date_range[1])
            if budget != None and budget > total:
                print(f"Well done! This is under the \'{category}\' budget"
                    + f" between {date_range[0]} \nand {date_range[1]}"
                    + f" of £{budget:.2f}.")
            
            elif budget != None and budget <= total:
                print("Unfortunately the budget over this time for " 
                      + f"\'{category}\' is £{budget:.2f}."
                      + "\nWe must try and spend less!")
        

def view_records (table_name, menu_choice):
    """
    view_records asks the user to provide a period of time which they like
    to view the records of, using the ask_for_date_range function. If the 
    user has chosent to view by category they wll be asked which category 
    they would like to view. Then all the relevant records are fetched using 
    the retrieve_income_expense function and displayed using the 
    display_as_table function. 

    Parameters  :   table_name : str
                        The name of the table the user has selected to view.
                    menu_choice : str
                        The menu choice of the user in the main code.
    
    Returns     :   
    """
    date_range = ask_for_date_range()

    # The category is necessary when viewing by category or viewing the budget. 
    if menu_choice == "3" or menu_choice == "6" :
    
        category = ask_for_category(table_name,menu_choice)
    
    else :
        category = None
    
    records = retrieve_income_expense(table_name, date_range[0],
                                       date_range[1], category)
    
    if len(records) == 0:
        print(f"Unfortunately, there are no records between {date_range[0]}"
              + f" and {date_range[1]}")
        return
    
    display_as_table(table_name, records)

    display_total(table_name,records,date_range, category)
    return


def retrieve_by_id(table_name, id_):
    """
    retrieve_by_id searches a table for a record with a certain ID and 
    returns the record if one is found. 
    
    Parameter:  id_ : int 
                    The ID number of the book to be searched for


    Returns:    id_record : list / NoneType
                    The record of the book with the ID provided or 
                    None if there is no record with the ID 
    """

    cursor.execute(f'''SELECT date, amount, category, description, id
                   FROM {table_name} WHERE id = (?) ''', (id_,))
    id_record = cursor.fetchone()
    db.commit()

    return id_record 


def ask_for_id(table_name):
        """
        ask_for_id asks the user to provide the I.D. of a record they wish
        to edit. The record will be searched for with the retrieve_by_id 
        function If they provide an I.D. of a record which is not in the 
        the table, they will be asked if they want to submit another I.D.. 
        If a record is found with the user inputted I.D., the record
        will be displayed to them using the display_as_table function and 
        they will be asked if this is the record they wish to edit. If the
        user wishes to edit the found record, that record is returned, if 
        they don't wish to edit a record None will be returned. 

        Parameters  :   table_name : str
                            The name of the table in which the record is to
                            be searched for. 
        
        Returns     :   id_record : list
                            A list containing a record which the user wishes
                            to edit
                        None
                            It returns None if the user does not wish to 
                            edit a record. 
        """
        while True:
            id_ =  input("\nPlease input the I.D\n")
            id_ = check_number(id_, "int")
            id_record = retrieve_by_id(table_name, id_)

            if id_record == None:
                print("\nUnfortunately there is no record with this I.D.")
                try_again = input("\nWould you like to try a different I.D.?"
                                  +"\n")
                try_again = check_yes_no(try_again)

            else:
                display_as_table(table_name, id_record)

                correct_record = input("\nIs the record above, the record"
                                       + " you wish to edit?\n")
                correct_record = check_yes_no(correct_record)

                if correct_record == "no":
                    try_again = input("Would you like to try a different"
                                      +" I.D.?\n")
                    try_again = check_yes_no(try_again)

                elif correct_record == "yes": 
                    return id_record 
            
            if try_again == "yes":
                continue

            elif try_again == "no" :
                print("\nNo information has been altered.\n")
                return None


def rename_delete_category(table_name, rename_or_delete):
    """
    rename_delete_category asks the user to chose the category name they 
    wish to change and then updates the table so that all the records 
    within that category are within the new category. If the user has 
    chosen to rename the category they can choose the category's new name
    but if they have chosen to delete a category then the category will
    default to "Misc". 

    Parameters  :   table_name  
                        The name of the table in which the chosen category
                        will be changed.
                    rename_or_delete
                        Either "rename" or "delete". The choice whether 
                        the user will rename or delete the category. 

    Returns     :
    """

    print("\nWe will now ask you to choose which category you wish to"
          +" update.")
    # Here we have chosen to set the function ask_for_category 's menu_choice
    # as "2" so that the user can not make a new category up.

    if rename_or_delete == "rename":
        original_category = ask_for_category(table_name, "2")

        print("\nNow we will ask you for what you would like to change the"
            + " category to?")
        # Here we have set the function ask_for_category's menu_choice as "4"
        # so that the user has the option to make up a new category name.
        new_category = ask_for_category(table_name, "4")

    elif rename_or_delete == "delete":
        original_category = ask_for_category(table_name, "2", "delete")

        new_category = "Misc"

    cursor.execute(f'''
        UPDATE {table_name} SET category = ? WHERE category = ?''' 
        ,(new_category, original_category))
    db.commit()

    print(f"\nAll records in the \'{original_category}\' are now in the \'"
          + f"{new_category}\' category.\n")


def delete_record (table_name):
    """
    delete_record finds the record which the user wants to delete and then
    deletes it from the corresponding table. It then informs the user that
    the record has been deleted. 

    Parameters  :   table_name
                        The name of the table the user wishes to delete a 
                        record from. 

    Returns     :       
    """
    original_record = ask_for_id(table_name)

    if original_record != None:

        id_ = original_record[-1]

        cursor.execute(f'''DELETE FROM {table_name} WHERE id = ?''',(id_,))
        db.commit()

        print(f"The following record has been deleted from the {table_name}"
              + " table:")
        print("")
        display_as_table(table_name, original_record)


def update_record (table_name):
    """
    update_record asks the user for a record to change by using the as_for_id
    function. Once the record is found the user is then asked to update 
    each column. With the new column data, the record is updated and the
    user is informed of this and displayed the change using the 
    display_as_table function. 

    Parameters  :   table_name : str
                        The name of the table where the record resides. 

    Returns     :       
    """
    original_record = ask_for_id(table_name)

    if original_record != None:

        id_ = original_record[-1]

        print("\nWe will now ask you to put in the correct information.")

        if table_name == "Expenses" or table_name == "Income":

            # The menu_choice for ask_for_record_data is chosen to be "4" to 
            # allow the user to add a new category if they wish to. 
            new_record = ask_for_record_data(table_name, "4")
            new_record.append(id_)

            cursor.execute(f'''UPDATE {table_name} 
SET date = ?, amount = ?, category = ?, description = ? 
WHERE  id = ? ''', (new_record))
            db.commit()
            
            print("This record has now been changed to:")
            display_as_table(table_name, new_record)

        elif table_name == "Goals":
            ""
    return


def edit_table(table_name):
    """
    edit_table asks the user if they wish to update a record, delete a 
    record, rename a category, delete a category or carry on without 
    doing any of them. The functions update_record, delete_record and 
    rename_delete_category are used to fulfil the users choice. 

    Parameters  :   table_name
                        The name of the table which the user's choice will
                        be used on. 

    Returns     :
    """

    while True:

        edit_choice = input("""\nPlease choose whether you would like to:
1. Update a record
2. Delete a record
3. Rename a category
4. Delete a category 
5. None of the above.\n\n""")
        
        if edit_choice == "1" :
            update_record(table_name)
            return

        elif edit_choice == "2":
            delete_record(table_name)
            return
            
        elif edit_choice == "3":
            rename_delete_category(table_name, "rename")
            return

        elif edit_choice == "4":
            print("\nWhen we delete a category, the records within that"
                  + " category move to the Misc category. ")
            rename_delete_category(table_name, "delete")
            return

        elif edit_choice == "5":
            return
        else: 
            print("Please only input \"1\", \"2\", \"3\" or \"4\"")


def display_goal_progress(original_goal_records, current_progress_records):
    """
    display_goal_progress calculates how far the user has gotten in achieving
    their goals. It takes the current progress and compares it to the original
    goal. Depending on the progress, the function gives a message to the user
    detailing their progress.

    Parameters  :   original_goal_records : list
                        A list containing all the original records of the 
                        goals. The records are in the format [date, amount,
                        description, id].
                    current_progress_records : list
                        A list containing all the progress of the goals to
                        today. The records are in the format [date, amount,
                        description, id].

    Returns     :
    """    
    current_progress_id_list = []
    
    for record in range(len(current_progress_records)):
        progress_id = current_progress_records[record][3]
        current_progress_id_list.append(progress_id)

    for i in range(len(original_goal_records)):
        # The I.D. is used to find the index of this goal
        # in the current_progress_records list.
        original_id = original_goal_records[i][3]
        record_index = current_progress_id_list.index(original_id)

        date_ = original_goal_records[i][0]
        original_amount = original_goal_records[i][1]
        description = original_goal_records[i][2]

        current_amount = current_progress_records[record_index][1]

        # Find the amount 
        amount_difference = abs(original_amount - current_amount)
        difference_percentage = (amount_difference/original_amount) * 100
        difference_percentage = round(difference_percentage,1)

        # Convert the amounts to str to 2 decimal places. 
        original_amount_str =  f"{original_amount:.2f}"
        current_amount_str = f"{current_amount:.2f}"
        amount_difference_str = f"{amount_difference:.2f}"
            


        print("\n\nGoal Description:\n-----------------\n")
        print("\'" + description + "\'\n")
        
        # Inform the user how their goal is going
        if original_amount < current_amount:

            print("Unfortunately it seems as though you have been spending"
                + f" too much!\nThis goal was set on {date_} with a goal"
                + f" of £{original_amount_str} but today the \ngoal is now £"
                + f"{current_amount_str}. Don't worry, you can \nget back on"
                + "track!")
            
        elif difference_percentage == 0:

            print("We are just getting started!\nLet\'s get to saving!\n"
                + f"This goal was set on {date_} to save £"
                + f"{original_amount_str}.\nWe haven't saved any yet, but I "
                + "believe in you!") 


        elif difference_percentage < 50:

            print("We are off to a really strong start!\nThis goals was set "
                + f"on {date_} and you have already \nmanaged to "
                + f"save £{amount_difference_str} of £{original_amount_str}."
                + f"\nThat\'s {difference_percentage}% of the way there!\n")
            
        elif difference_percentage >= 50 and difference_percentage < 100: 
            print("Incredible!\nWe are almost there!\nThis goal was set on"
                  + f"{date_} and you have managed \nto save a whopping "
                  + f"{difference_percentage}%.\nThat's right you have saved"
                  + f"£{amount_difference_str} of £{original_amount_str}."
                  + "\nThe end is in sight!")
            
        elif difference_percentage == 100:
            print("Holy Moly!!!!!\nYou\'ve only gone and done it!\nYou have"
                + f"saved the full £{original_amount_str}.\nI bet that feels"
                + "good!")
    

        


# MAIN CODE
try: 

    # Create or open a file called 'budget_app_db' with a SQLite3 Database.       
    db = sqlite3.connect('budget_app_db')
    cursor = db.cursor()

    # Create a table called 'Income' if it doesn't exist.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS 
        Income( id INTEGER PRIMARY KEY, date DATE, amount REAL, 
            category TEXT DEFAULT "Misc" NOT NULL, description TEXT)
                ''')
    db.commit()

    # Create  a table called 'Expenses' if it doesn't exist.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        Expenses( id INTEGER PRIMARY KEY,  date DATE,  amount REAL, 
            category TEXT DEFAULT "Misc" NOT NULL, description TEXT)
                   ''')
    db.commit()


    # Create a table called 'Budget" if it doesn't exist
    # The Budget table will hold the weekly budget for the categories in 
    # Expenses. 
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        Budget( category TEXT PRIMARY KEY, budget REAL)
''')
    db.commit()

    # Create a table called "Goals" if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS
        Goals( date DATE, amount REAL, description TEXT,  
                   id INTEGER PRIMARY KEY)
''')
    db.commit()

except Exception as e: 

    # Roll back any change if something goes wrong.
    db.rollback()
    raise e


print("\nAs this is a demo app, we recommend populating the tables with "
      + "example data.")
populate_tables = input("Would you like to populate the tables?\n")
populate_tables = check_yes_no(populate_tables)


if populate_tables == "yes":

    income_record_list = []
    expense_record_list = []
    budget_record_list = []
    goals_record_list = []

    try:
        # Open "Income_expense_goals" 
        with open("Income_expense_goals.csv", 'r') as file:
            csvreader = csv.reader(file)

            for read_in_record in csvreader:
                # For each table the second column is a number and so 
                # we must convert this to a float for each record.
                read_in_record[1] = float(read_in_record[1])

                if read_in_record[-1] == "Income":
                    read_in_income = read_in_record[:-1]
                    income_record_list.append(read_in_income)
                    

                elif read_in_record[-1] == "Expenses" : 
                    read_in_expense = read_in_record[:-1]
                    expense_record_list.append(read_in_expense)
                    
                elif read_in_record[-1] == "Budget":
                    read_in_budget = read_in_record[:-1]
                    budget_record_list.append(read_in_budget)


                elif read_in_record[-1] == "Goals":
                    read_in_goals = read_in_record[:-1]
                    goals_record_list.append(read_in_goals)

        add_to_table("Income", income_record_list, "yes")
        add_to_table("Expenses", expense_record_list, "yes")
        add_to_table("Budget",budget_record_list,"yes")
        add_to_table("Goals", goals_record_list,"yes")
    
    except FileNotFoundError:
        print("\n\nUnfortunately Income_expense_goals.csv could not be found."
            + "\nPlease eansure it is in your work space if you wish to\n"
            + "populate the database.\n\n")
        
    
while True:

    menu = input("""
What operation would you like to perform:

1. Add expense 
2. View expenses
3. View expenses by category 
4. Add income
5. View income 
6. View income by category
7. Set budget for a category 
8. View budget for a category
9. Set financial goals
10. View progress towards finacial goals 
11. Quit
\n""")
    
    # Add Expense
    if menu == "1":

        new_expense = ask_for_record_data("Expenses", menu)
        add_to_table("Expenses", new_expense, "no")


    # View Expenses
    elif menu == "2":

        view_records('Expenses', menu)
        edit_table("Expenses")


    # View Expenses By Category 
    elif menu == "3":
        
        print("We will now ask you to tell us when you would like to start"
              + "\nyou\'re search.")
        view_records("Expenses", menu)


    # Add income
    elif menu == "4":

        new_income = ask_for_record_data("Income", menu)
        add_to_table("Income", new_income, "no")


    # View Income 
    elif menu == "5":

        view_records("Income", menu)
        edit_table("Income")


    # View Income by category
    elif menu == "6":

        view_records("Income", menu)


    #Set budget for a category
    elif menu == "7":

        [category, budget] = ask_for_record_data("Budget", menu)

        budget_categories = retrieve_categories("Budget", "not")

        # If the user's chosen category is already in the Budget table 
        # then update that budget, otherwise insert a new budget. 
        if (category,) in budget_categories:
            cursor.execute('''UPDATE Budget SET budget = ? 
                           WHERE category = ? ''', (budget, category))
            db.commit()
            
        else:
            cursor.execute('''INSERT INTO Budget(category, budget)
                           VALUES (?,?)''', (category, budget))
            db.commit()
        
        print(f"\'{category}\' now has a weekly budget of £"
              + f"{budget:.2f}.")


    # View budget for a category
    elif menu == "8":

        cursor.execute('''SELECT * FROM Budget ORDER BY category''')
        budget_records = cursor.fetchall()
        db.commit()

        print("Here are all of the budgets you have set.")
        display_as_table("Budget", budget_records)


    #Set financial goals
    elif menu == "9":
        
        goal_record_data = ask_for_record_data("Goals", menu)
        add_to_table("Goals", goal_record_data, "no")

        
    # View progress towards financial goals
    elif menu == "10":

        # Fetching all the goal records from the Goals table.
        cursor.execute('''SELECT * FROM Goals ORDER BY DATE''')
        goal_records_tuple = cursor.fetchall()
        db.commit()

        # Getting all the distinct dates in order.
        cursor.execute('''SELECT DISTINCT date FROM Goals ORDER BY date''')
        goal_dates_distinct_tuple = cursor.fetchall()
        db.commit()

        # A list of the distinct start dates of the goals
        goal_dates_distinct = []
        # A list of the records for each goal.
        goal_records = []
        # A copy of the goal_records list containing the original goal records
        goal_records_original = []
        # A list of the indivual goal dates. 
        goal_dates_actual = []
        # A list of the individual goal amounts which will .
        goal_amounts = []
        # A list of the profit the user has generated between the goal dates.
        profit_between_dates = []
        # The number of goals which start at each distinct date
        records_per_date = []
        
        today = datetime.date.today()
        counter = 0

        # Converting the records and dates to lists instead of tuples.
        for record in goal_records_tuple:
            record = list(record)
            record[0] = datetime.datetime.strptime(record[0], 
                                                       "%Y-%m-%d").date()
            goal_records.append(record)
            goal_records_original.append(record)

        
        for date_ in goal_dates_distinct_tuple:
            (date_distinct,) = date_
            date_distinct = datetime.datetime.strptime(date_distinct, 
                                                      "%Y-%m-%d").date()
            goal_dates_distinct.append(date_distinct)


        for record in goal_records:
            record = list(record)
            date = record[0]
            amount = record[1]

            goal_dates_actual.append(date)
            goal_amounts.append(amount)



        for date in goal_dates_distinct:

            # If the goals start_date is today or before carry on
            if  goal_dates_distinct[counter] <= today: 
                # if the current date is not the last in the list and the 
                # next date is before today 
                if  (len(goal_dates_distinct) >= (counter + 2) and 
                    goal_dates_distinct[counter + 1] <= today):
                        
                        # We must takeaway a day from the end date as
                        # retrieve_income_expense is inclusive when searching
                        expenses = retrieve_income_expense("Expenses",
                                goal_dates_distinct[counter], 
                                (goal_dates_distinct[counter+1] -
                                datetime.timedelta(days=1)))
                        
                        incomes = retrieve_income_expense("Income", 
                                    goal_dates_distinct[counter], 
                                    (goal_dates_distinct[counter + 1] - 
                                     datetime.timedelta(days=1)))
                
                else :
                    expenses = retrieve_income_expense("Expenses", 
                                    goal_dates_distinct[counter], today)
                    incomes = retrieve_income_expense("Income", 
                                    goal_dates_distinct[counter], today)
                
                expense_total = calculate_total(expenses)
                income_total = calculate_total(incomes)
                # Find the profit to be added
                profit = income_total - expense_total
                profit_between_dates.append(profit)

            else:
                break
            counter += 1 

        cumulative_no_records = 0 

        for date_distinct in goal_dates_distinct: 
            
            no_of_records = goal_dates_actual.count(date_distinct)
            cumulative_no_records += no_of_records
            date_with_number = [date_distinct,cumulative_no_records]
            records_per_date.append(date_with_number)    


        counter  = 0 
        # Go through the date and number in records_per_date
        for entry, date_or_number in enumerate(records_per_date):

            # Sort the records by amount ascending order
            goal_records =sorted(goal_records, key = itemgetter(1))
            # The number of records left with unachieved goals
            no_of_records = records_per_date[entry][1]
            date = records_per_date[entry][0]
            
            for i, column in enumerate(goal_records):

                # If the current goal has the same or before the date as 
                # the current date
                if goal_records[i][0] <= date :

                    # If the current goal has ended take away their share
                    # of profit.
                    if goal_records[i][1] == 0:
                        no_of_records -= 1

            # If there is no goals that need the profit then no profit
            # is needed.
            if no_of_records == 0:
                share_of_profit = 0
                        
            else:
                # Divide the profit by the number of goals which will share it
                share_of_profit = (profit_between_dates[entry] / 
                                    no_of_records)
                
            for i, column in enumerate(goal_records):
                
                if goal_records[i][0] <= date :
                        
                    # If the goal is completed nothing happens to it
                    if goal_records[i][1] == 0:
                        continue
                    
                    # Else if the goal amount left is less than the profit then 
                    # the goal is completed and set to 0.
                    elif goal_records[i][1] <= share_of_profit:
                        # If there are more records after this adjust the
                        # next record's share of profit.
                        if no_of_records != 1:
                            # share = ((n-1)share_old + difference) / (n-1) 
                            n = no_of_records
                            difference = share_of_profit - goal_records[i][1]
                            profit_left = (n-1) * share_of_profit + difference

                            share_of_profit = profit_left / (n-1)

                        # Set the goal to accomplished
                        goal_records[i][1] = 0
                        no_of_records -= 1
                    
                    # Else the goal amount is reduced by the share of the
                    # profits
                    else:   
                        goal_records[i][1] -= share_of_profit

                    
            # If the code isn't on the final entry, then remove the completed 
            # records from the next records_per_date entry.
            if entry != len(records_per_date) - 1:
                no_records_completed = (records_per_date[entry][1]
                                         - no_of_records)
                records_per_date[entry+1][1] -= no_records_completed

        # Collect the original goal records.        
        cursor.execute('''SELECT * FROM Goals ORDER BY DATE''')
        goal_records_original = cursor.fetchall()
        db.commit()

        display_goal_progress(goal_records_original, goal_records)

    # Quit
    elif menu == "11":

        db.close()
        exit()
    

    else :

        print("""\nYour input has not been recognised.
Please input the number of the corresponding operation.""")

