import os
from time import sleep
from datetime import datetime
from database import MemoryDatabase

if __name__ != "__main__":
    exit()

def clear_terminal():
    os.system('cls')

db = MemoryDatabase()
if db.is_empty():
    db.add_table("data", ["title", "times_completed", "last_time_completed"], [str, int, str])
db.select_table("data")

def complete_habit():
    clear_terminal()

    habits = db.get_data_by_column_names("title", "times_completed", "last_time_completed")

    for idx, habit in enumerate(habits):
        print(f"({idx}) {habit[0]} |{int(habit[1]/5)*" ●"}{habit[1]%5*" ○"} | {habit[2]}")

    habit_index = input("Enter the number of the habit you completed: ")
    try:
        habit_index = int(habit_index)
        if habit_index < 0 or habit_index >= len(habits):
            print("Invalid habit selection!")
            return
    except ValueError:
        print("Invalid input!")
        return

    habit = habits[habit_index]
    habit_title = habit[0]
    current_times_completed = habit[1]

    new_times_completed = current_times_completed + 1
    db.update_column(
        ["times_completed"], [new_times_completed], filter_fn=lambda row: row[0] == habit_title
    )

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.update_column(
        ["last_time_completed"], [current_time], filter_fn=lambda row: row[0] == habit_title
    )

    print(f"Successfully marked '{habit_title}'.")
    input("Press Enter to continue...")

def view_habits():
    clear_terminal()

    habits = db.get_data_by_column_names("title", "times_completed", "last_time_completed")
    
    for habit in habits:
        print(f"{habit[0]} |{int(habit[1]/5)*" ●"}{habit[1]%5*" ○"} | {habit[2]}")
    
    input("Press Enter to continue...")

def add_habit():
    clear_terminal()

    title = input("Enter the title of the habit: ")
    times_completed = 0 
    last_time_completed = "Never"  

    db.add_data([title, times_completed, last_time_completed])
    print(f"Successfully added new habit: {title}.")
    input("Press Enter to continue...")

def remove_habit():
    clear_terminal()

    habits = db.get_data_by_column_names("title", "times_completed", "last_time_completed")
    print("Habits to remove:")
    
    for idx, habit in enumerate(habits):
        print(f"({idx}) {habit[0]} |{int(habit[1]/5)*" ●"}{habit[1]%5*" ○"} | {habit[2]}")

    habit_index = input("Enter the number of the habit you want to remove: ")
    try:
        habit_index = int(habit_index)
        if habit_index < 0 or habit_index >= len(habits):
            print("Invalid habit selection!")
            return
    except ValueError:
        print("Invalid input!")
        return

    habit = habits[habit_index]
    habit_title = habit[0]
    db.remove_row(filter_fn=lambda row: row[0] == habit_title)

    print(f"Successfully removed '{habit_title}' from the habits list.")
    input("Press Enter to continue...")

def save():
    clear_terminal()

    db.save()
    print(f"Saved")
    input("Press Enter to continue...")

action_array = [
    {"title": "View habits", "function": view_habits},
    {"title": "Complete habits", "function": complete_habit},
    {"title": "Remove", "function": remove_habit},
    {"title": "Add", "function": add_habit},
    {"title": "Save", "function": save},
    {"title": "Exit without saving", "function": exit}
]

def start():
    clear_terminal()
    print("Welcome to the habit tracker!")
    action_number = 0
    while True:
        print("Please select the action youd like.")
        for index, item in enumerate(action_array):
            print(f"({index}) {item["title"]}")
        action_number = input("")
        try:
            action_number = int(action_number)
            if action_number < 0 or action_number >= len(action_array):
                raise Exception("Action not found")
            break
        except:
            clear_terminal()
            print("Oops! That action was not found.")

    action_array[action_number]["function"]()

while True:
    start()
