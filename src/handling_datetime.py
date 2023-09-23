from datetime import datetime
import pandas as pd
from datetime import date 

def today_date_to_digits():
    # Get the current date
    current_date = datetime.now()
    
    # Convert the date to a string of digits in day month year format
    date_string = current_date.strftime("%d%m%Y")
    
    # Return the date string as a string data type
    return str(date_string)

