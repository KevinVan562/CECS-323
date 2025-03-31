import logging
from datetime import datetime
from pprint import pprint

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import session

from SQLAlchemyUtilities import check_unique
from sqlalchemy import select

from menu_definitions import menu_main, add_menu, delete_menu, list_menu, debug_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Student, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from employee import Employee
from date import WorkDate
from hour import Hour
from WorkSchedule import WorkSchedule
from option import Option
from menu import Menu

def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)

def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)

def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)

# Employee Class
def select_employee(sess) -> Employee:
    found: bool = False
    employee_last_name: str = ''
    employee_first_name: str = ''

    while not found:
        employee_first_name = input("Employee's first name--> ")
        employee_last_name = input("Employee's last name--> ")

        name_count: int = sess.query(Employee).filter(Employee.firstName == employee_first_name,
                                                      Employee.lastName == employee_last_name).count()
        found = name_count == 1

        if not found:
            print("No employee found by that name. Try again.")

    employee: Employee = sess.query(Employee).filter(Employee.lastName == employee_last_name,
                                                     Employee.firstName == employee_first_name).first()
    return employee

def add_employee(sess: Session):
    unique_name: bool = False
    employee_first_name: str = ''
    employee_last_name: str = ''

    while not unique_name:
        employee_first_name = input("Enter the new Employee First Name: ")
        employee_last_name = input("Enter the new Employee Last Name: ")

        name_count: int = sess.query(Employee).filter(Employee.firstName == employee_first_name,
                                                      Employee.lastName == employee_last_name).count()
        unique_name = name_count == 0
        if not unique_name:
            print(f"Employee with name {employee_first_name} {employee_last_name} already exists. Try again.")

    try:
        new_employee = Employee(firstName=employee_first_name, lastName=employee_last_name)
        sess.add(new_employee)
        sess.commit()
        print(f"Employee {new_employee.firstName} {new_employee.lastName} added successfully.")
    except IntegrityError as e:
        sess.rollback()
        print(f"Error: {e.orig}")
        print(f"Employee with first name {employee_first_name} and last name {employee_last_name} already exists")


def delete_employee(sess: Session):
    employee: Employee = select_employee(sess)
    if employee:
        sess.delete(employee)
        print(f"{employee} deleted successfully.")
        sess.commit()
    else:
        print("Employee not found.")

def list_employee(sess: Session):
    employees: [Employee] = list(sess.query(Employee).order_by(Employee.lastName, Employee.firstName))
    for employee in employees:
        print(employee)

# Date Class
def select_date(sess) -> WorkDate:
    found: bool = False
    date_input: str = ''

    while not found:
        date_input = input("Enter Date (YYYY-MM-DD): ")
        date_convert = datetime.strptime(date_input, "%Y-%m-%d").date()

        # Check if the date exists in the database
        date_count: int = sess.query(WorkDate).filter(WorkDate.shiftDate == date_convert).count()
        found = date_count == 1

        if not found:
            print(f"No date found for {date_convert}. Try again.")

    date_query: WorkDate = sess.query(WorkDate).filter(WorkDate.shiftDate == date_convert).first()
    return date_query

def add_date(sess: Session):
    unique_date: bool = False
    date_input: str = ''
    holiday_input: str = ''

    while not unique_date:
        # Loop until a valid date is entered
        while True:
            date_input = input("Enter Date (YYYY-MM-DD): ")
            try:
                date_convert = datetime.strptime(date_input, "%Y-%m-%d").date()
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD format.")

        holiday_input = input("Enter holiday name: ")

        date_count: int = sess.query(WorkDate).filter(WorkDate.shiftDate == date_convert).count()
        unique_date = date_count == 0
        if not unique_date:
            print(f"Date {date_convert} already exists. Try again.")

    try:
        new_date = WorkDate(shiftDate=date_convert, holidayFlag=holiday_input)
        sess.add(new_date)
        sess.commit()
        print(f"Date {new_date.shiftDate} added successfully.")
    except IntegrityError as e:
        sess.rollback()
        print(f"Error: {e.orig}")
        print(f"Date {date_convert} already exists.")

def delete_date(sess: Session):
    date: WorkDate = select_date(sess)

    try:
        sess.delete(date)
        sess.commit()
        print(f"Date {date.shiftDate} was successfully deleted.")
    except IntegrityError as e:
        sess.rollback()
        print(f"Error: {e.orig}")
        print("Cannot delete this date because it has dependent records.")

def list_date(sess: Session):
    dates: [WorkDate] = list(sess.query(WorkDate).order_by(WorkDate.shiftDate))
    for date in dates:
        print(date)

# Hour Class
def select_hour(sess) -> Hour:
    found: bool = False
    shift_name_input: str = ''

    while not found:
        shift_name_input = input("Enter Shift Name: ")

        # Check if the shift exists in the database
        shift_count: int = sess.query(Hour).filter(Hour.shiftName == shift_name_input).count()
        found = shift_count == 1

        if not found:
            print(f"No shift found with the name {shift_name_input}. Try again.")

    shift_query: Hour = sess.query(Hour).filter(Hour.shiftName == shift_name_input).first()
    return shift_query

def add_hour(sess: Session):
    unique_shift: bool = False
    shift_name_input: str = ''
    start_hour_input: int = 0
    end_hour_input: int = 0

    while not unique_shift:
        shift_name_input = input("Enter Shift Name: ")
        start_hour_input = int(input("Enter Start Hour: "))
        end_hour_input = int(input("Enter End Hour: "))

        shift_count: int = sess.query(Hour).filter(Hour.shiftName == shift_name_input).count()
        unique_shift = shift_count == 0
        if not unique_shift:
            print(f"Shift {shift_name_input} already exists. Try again.")

    try:
        new_shift = Hour(shiftName=shift_name_input, shiftStartHour=start_hour_input, shiftEndHour=end_hour_input)
        sess.add(new_shift)
        sess.commit()
        print(f"Shift {new_shift.shiftName} added successfully.")
    except IntegrityError as e:
        sess.rollback()
        print(f"Error: {e.orig}")
        print(f"Shift {shift_name_input} already exists.")

def delete_hour(sess: Session):
    hour: Hour = select_hour(sess)

    try:
        sess.delete(hour)
        sess.commit()
        print(f"Shift {hour.shiftName} was successfully deleted.")
    except IntegrityError as e:
        sess.rollback()
        print(f"Error: {e.orig}")
        print("Cannot delete this shift because it has dependent records.")

def list_hour(sess: Session):
    hours: [Hour] = list(sess.query(Hour).order_by(Hour.shiftName))
    for hour in hours:
        print(hour)

# WorkSchedule Class
def add_schedule(sess: Session):
    employee: Employee = select_employee(sess)
    date: WorkDate = select_date(sess)
    hour: Hour = select_hour(sess)
    work_schedule_count: int = sess.query(WorkSchedule).filter(WorkSchedule.employeeEmployeeID == employee.employeeID,
                                                               WorkSchedule.dateShiftDate == date.shiftDate,
                                                               WorkSchedule.hourShiftName == hour.shiftName).count()
    unique_name = work_schedule_count == 0

    while not unique_name:
        print(f"Schedule already exists for employee {employee.firstName} {employee.lastName}. Try again.")
        employee = select_employee(sess)
        date: WorkDate = select_date(sess)
        hour: Hour = select_hour(sess)

    new_schedule = WorkSchedule(employee=employee, date=date, hour=hour)
    sess.add(new_schedule)
    sess.commit()
    print(f"New schedule for employee {employee.firstName} {employee.lastName} "
          f"on {date.shiftDate} during the {hour.shiftName} shift added successfully.")

def delete_schedule(sess: Session):
    employee: Employee = select_employee(sess)
    date: WorkDate = select_date(sess)
    hour: Hour = select_hour(sess)
    schedule = sess.query(WorkSchedule).filter(WorkSchedule.employeeEmployeeID == employee.employeeID,
                                              WorkSchedule.dateShiftDate == date.shiftDate,
                                              WorkSchedule.hourShiftName == hour.shiftName).first()
    if not schedule:
        print("Schedule not found.")
        return

    sess.delete(schedule)
    sess.commit()
    print(f"Schedule for employee {employee.firstName} {employee.lastName},"
          f"on {date.shiftDate} during the {hour.shiftName} shift deleted successfully.")

def list_schedule(sess: Session):
    employee: Employee = select_employee(sess)

    recs = sess.query(WorkSchedule).join(WorkDate, WorkSchedule.dateShiftDate == WorkDate.shiftDate).join(
        Hour, WorkSchedule.hourShiftName == Hour.shiftName).filter(
        WorkSchedule.employeeEmployeeID == employee.employeeID).add_columns(
        WorkDate.shiftDate, Hour.shiftName).all()

    if not recs:
        print(f"No work schedules found for employee {employee.firstName} {employee.lastName}.")
        return

    for rec in recs:
        print(f"Employee name: {employee.firstName} {employee.lastName}, Date: {rec.shiftDate}, Hour: {rec.shiftName}")



def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess:    The connection to the database.
    :return:        None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())

def main():
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
if __name__ == '__main__':
    main()
