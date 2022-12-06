import datetime
import info_handler as ih
from restore import Restore


def restore_options(restore_id:str, date_input:str):
    
    return_list = []
    return_list.append(restore_id)
    try:
        # User date input
        print(date_input)
        if date_input == 'today':
            # needs to be converted into a string of the specific format
            date_var = datetime.date.today().strftime("%Y-%m-%d-%H-%M-%S")
            # creates a datetime object supporting the correct format
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
            date_var = date_var.replace(hour=23, minute=59, second=59)
        elif date_input == 'yesterday':
            # calculates the date for yesterday
            date_var = datetime.date.today() + datetime.timedelta(-1)
            date_var = datetime.datetime.strftime("%Y-%m-%d-%H-%M-%S")
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
            date_var = date_var.replace(hour=23, minute=59, second=59)
        elif date_input == 'now':
            # procedure for now
            date_var = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
        elif ih.validate_date_format(date_input, "%Y-%m-%d-%H-%M-%S"):
            # if datetime is given in the correct format
            date_var = datetime.datetime.strptime(date_input, "%Y-%m-%d-%H-%M-%S")
        elif ih.validate_date_format(date_input, "%Y-%m-%d-%H-%M"):
            # without the second timestamp
            date_var = datetime.datetime.strptime(date_input, "%Y-%m-%d-%H-%M")
            date_var = date_var.strftime("%Y-%m-%d-%H-%M-%S")
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
            date_var = date_var.replace(second=59)
        elif ih.validate_date_format(date_input, "%Y-%m-%d-%H"):
            # without second and minute
            date_var = datetime.datetime.strptime(date_input, "%Y-%m-%d-%H")
            date_var = date_var.strftime("%Y-%m-%d-%H-%M-%S")
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
            date_var = date_var.replace(minute=59, second=59)
        elif ih.validate_date_format(date_input, "%Y-%m-%d"):
            # without hour, minute and second
            date_var = datetime.datetime.strptime(date_input, "%Y-%m-%d")
            date_var = date_var.strftime("%Y-%m-%d-%H-%M-%S")
            date_var = datetime.datetime.strptime(date_var, "%Y-%m-%d-%H-%M-%S")
            date_var = date_var.replace(hour=23, minute=59, second=59)
        else:
            print("No valid format. Use YYYY-mm-DD-HH-MM-SS")
        return_list.append(date_var)
        
    except:
        print("No valid format. Use YYYY-mm-DD-HH-MM-SS")
    return return_list