import re
import pandas as pd


def preprocess(data):
  pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
  messages = re.split(pattern, data)[1:]
  dates = re.findall(pattern, data)
  df = pd.DataFrame({'user_message': messages, 'message_date': dates})
  df['message_date'] = pd.to_datetime(df['message_date'],
                                      format='%d/%m/%Y, %I:%M %p - ',
                                      errors='coerce')
  df.rename(columns={'message_date': 'date'}, inplace=True)
  user = []
  message = []
  for msg in df['user_message']:
    entry = re.split('([\w\W]+?):\s', msg)
    if (entry[1:]):
      user.append(entry[1])
      message.append(':'.join(entry[2:]))
    else:
      user.append('group_notification')
      message.append(entry[0])

  df['user'] = user
  df['message'] = message

  df.drop(columns=['user_message'], inplace=True)
  df['year'] = df['date'].dt.year
  df['month'] = df['date'].dt.month_name()
  df['day'] = df['date'].dt.day
  df['hour'] = df['date'].dt.hour
  df['minute'] = df['date'].dt.minute

  df.drop(columns=['date'], inplace=True)

  return df
