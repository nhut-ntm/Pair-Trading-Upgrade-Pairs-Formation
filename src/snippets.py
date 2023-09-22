from datetime import datetime


def today_date_to_digits():
    # Get the current date
    current_date = datetime.now()
    
    # Convert the date to a string of digits
    date_string = current_date.strftime("%Y%m%d")
    
    # Return the date string as a string data type
    return str(date_string)

