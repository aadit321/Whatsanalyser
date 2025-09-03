import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{2}\/\d{2}\/\d{2},\s\d{1,2}:\d{2}(?:\s(?:am|pm))\s-\s'
    messages = re.split(pattern,data)[1:]
    dates = re.findall(pattern,data,re.MULTILINE)
    df = pd.DataFrame({'User_message':messages,'Message_data':dates})
    df["Message_data"] = (df["Message_data"].str.replace("\u202f", " ", regex=False).str.replace("-", "", regex=False).str.strip())
    df["Message_data"] = pd.to_datetime(df["Message_data"],format=r"%d/%m/%y, %I:%M %p",errors="coerce")
    users = []
    messages = []
    for message in df['User_message']:
        entry = re.split(':',message)
        if entry[1:]:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notifiction')
            messages.append("group Discreption notification")
    df['User'] = users
    df['messager'] = messages
    df = df.drop(['User_message'],axis=1)
    df['Year'] = df['Message_data'].dt.year
    df['mounth'] = df['Message_data'].dt.month_name()
    df['day'] = df['Message_data'].dt.day
    df['hour'] = df['Message_data'].dt.hour
    df['minute'] = df['Message_data'].dt.minute
    df["month_num"] = df["Message_data"].dt.month
    
    df.drop(['Message_data'],axis = True)
    df['messager'] = df['messager'].str.strip()

    return df