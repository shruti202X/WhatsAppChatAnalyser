import streamlit as st
import matplotlib.pyplot as plt
import preprocessor
import helper

st.sidebar.title("Whatsapp Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:

  bytes_data = uploaded_file.getvalue()
  data = bytes_data.decode("utf-8")

  df = preprocessor.preprocess(data)
  st.dataframe(df)

  user_list = df['user'].unique().tolist()
  user_list.remove('group_notification')
  user_list.insert(0, 'Overall')

  selected_user = st.sidebar.selectbox("Show analysis of:", user_list)

  if st.sidebar.button("Show Analysis"):

    num_of_messages, num_of_words, num_of_media_messages, num_of_links, wc, words_series_df = helper.getStats(
      selected_user, df)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.header("Total Messages")
      st.title(num_of_messages)
    with col2:
      st.header("Total Words")
      st.title(num_of_words)
    with col3:
      st.header("Media Shared")
      st.title(num_of_media_messages)
    with col4:
      st.header("Links Shared")
      st.title(num_of_links)

    st.divider()

    if selected_user == "Overall":

      st.header("Busiest Users")

      top_user_message_count, user_percentage = helper.busy_users(df)

      cell21, cell22 = st.columns(2)
      with cell21:
        fig, ax = plt.subplots()
        ax.bar(top_user_message_count.index,
               top_user_message_count.values,
               color='#669999')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
      with cell22:
        st.dataframe(user_percentage)
      st.divider()

    # wordcloud
    st.header("Word Cloud")
    fig, ax = plt.subplots()
    ax.imshow(wc)
    st.pyplot(fig)
    st.divider()

    #most common words
    st.header("Most Common Words")
    fig, ax = plt.subplots()
    ax.barh(words_series_df['word_count'],
            words_series_df['count'],
            color='#669999')
    st.pyplot(fig)
    st.divider()
else:
  st.header("Please upload a whatsapp export chat file.")
