import re
import pandas as pd

def preprocess(data_frame):
    pattern = '\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\u202f?[ap]m\s-\s'
    messages = re.split(pattern, data_frame)[1:]
    clean_text = re.sub(r'\u202f', ' ', data_frame)
    pattern = r'\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    dates = re.findall(pattern, clean_text)

    df = pd.DataFrame({'User_Message': messages, 'Message_Dates': dates})
    # df['Message_Dates'] = pd.to_datetime(df['Message_Dates'], format='%d/%m/%Y, %H:%M -  ')
    df['Message_Dates'] = pd.to_datetime(df['Message_Dates'],
                                         format='%d/%m/%y, %I:%M %p - ')  # Changed the format string to match the date format and added %p directive for am/pm
    df.rename(columns={'Message_Dates': 'Date'}, inplace=True)

    users = []
    message = []
    for messages in df['User_Message']:
        entry = re.split('([\w\W]+?):\s', messages)
        if entry[1:]:
            users.append(entry[1])
            message.append(entry[2])
        else:
            users.append('group_notification')
            message.append(entry[0])


    df['User'] = users
    df['Message'] = message
    df.drop(columns=['User_Message'], inplace=True)

    df['month'] = df['Date'].dt.month_name()
    df['day'] = df['Date'].dt.day
    df['year'] = df['Date'].dt.year
    df['hour'] = df['Date'].dt.hour
    df['minute'] = df['Date'].dt.minute

    return df