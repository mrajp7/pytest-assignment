from datetime import datetime

def get_datetime_from_iso(value:str):
    try:
        date = datetime.fromisoformat(value)
    except:
        date = False
    
    return date