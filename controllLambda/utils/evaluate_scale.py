

def evaluate_scale(message_number):
    try:
        if(int(round(int(message_number) / 5,0)) == 0 and message_number!= 0 ):
            return 1
        else:
            return int(round(int(message_number) / 5,0))
    except ValueError:
        raise ValueError("Got no Number")


