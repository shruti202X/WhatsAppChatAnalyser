import re
import pandas as pd
from wordcloud import WordCloud


def getStats(selected_user, df):
  if selected_user != 'Overall':
    df = df[df['user'] == selected_user]

  num_of_messages = df.shape[0]

  num_of_media_messages = 0

  words = []

  regex = "https?://[^\s]+"
  links = []

  for message in df['message']:
    if message == '<Media omitted>\n':
      num_of_media_messages += 1
    else:
      words.extend(message.lower().split())
      links.extend(re.findall(regex, message))

  f = open('./stop_hinglish.txt', 'r')
  stop_words = f.read()
  f.close()
  stop_words = re.split('\n', stop_words)

  words_series = pd.Series(
    words, name="word_count").value_counts().sort_values(ascending=False)
  words_series.drop(labels=stop_words,
                    axis='index',
                    errors='ignore',
                    inplace=True)
  words_series_df = words_series.reset_index().rename(
    columns={'index': 'word'})

  num_of_words = len(words)
  num_of_links = len(links)

  wc = WordCloud(width=800,
                 height=700,
                 min_font_size=10,
                 background_color='white').generate(" ".join(
                   words_series.index))

  return num_of_messages, num_of_words, num_of_media_messages, num_of_links, wc, words_series_df.head(
    20)


def busy_users(df):
  user_message_count = df['user'].value_counts()
  user_message_count.drop(labels=['group_notification'], inplace=True)
  top_user_message_count = user_message_count.head()

  user_percentage = round(
    (user_message_count / user_message_count.sum()) * 100, 2)
  user_percentage = user_percentage.reset_index().rename(columns={
    'index': 'User',
    'user': 'Percentage'
  })

  return top_user_message_count, user_percentage
