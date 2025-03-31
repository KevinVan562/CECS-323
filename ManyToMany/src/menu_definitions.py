from menu import Menu
from option import Option

# Main menu for CRUD operations
menu_main = Menu('main', 'Please select one of the following options:', [
    Option("Add", "add(sess)"),
    Option("List", "list_objects(sess)"),
    Option("Delete", "delete(sess)"),
    Option("Commit", "sess.commit()"),
    Option("Rollback", "session_rollback(sess)"),
    Option("Exit this application", "pass")
])

# Add menu options for Employee, Date, Hour, and Schedule
add_menu = Menu('add', 'Please indicate what you want to add:', [
    Option("Employee", "add_employee(sess)"),
    Option("Date", "add_date(sess)"),
    Option("Hour", "add_hour(sess)"),
    Option("Schedule", "add_schedule(sess)"),
    Option("Exit", "pass")
])

# Delete menu options for Employee, Date, Hour, and Schedule
delete_menu = Menu('delete', 'Please indicate what you want to delete from:', [
    Option("Employee", "delete_employee(sess)"),
    Option("Date", "delete_date(sess)"),
    Option("Hour", "delete_hour(sess)"),
    Option("Schedule", "delete_schedule(sess)"),
    Option("Exit", "pass")
])

# List menu options for Employee, Date, Hour, and Schedule
list_menu = Menu('list', 'Please indicate what you want to list:', [
    Option("Employee", "list_employee(sess)"),
    Option("Date", "list_date(sess)"),
    Option("Hour", "list_hour(sess)"),
    Option("Schedule", "list_schedule(sess)"),
    Option("Exit", "pass")
])

# A menu to prompt for the amount of logging information to go to the console.
debug_select = Menu('debug select', 'Please select a debug level:', [
    Option("Informational", "logging.INFO"),
    Option("Debug", "logging.DEBUG"),
    Option("Error", "logging.ERROR")
])
