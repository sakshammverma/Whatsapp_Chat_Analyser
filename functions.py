from urlextract import URLExtract
extractor = URLExtract()
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]

    # Number of messages
    num_messages = df.shape[0]

    # Number of words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    # Number of media files
    no_of_media = df[df['Message'] == '<Media omitted>\n'].shape[0]

    #no of links
    links=[]
    for message in df['Message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), no_of_media,len(links)

#busy people



def busy_peoples(selected_users,df):
    x_axis = df['User'].value_counts().head()
    df=round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'User':'Name','count':'Percent'})
    return x_axis,df


def word_cloud(selected_user,df):
    f = open('stop.txt', 'r')
    stop = f.read()
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    temp= df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500, height=500, background_color='white',min_font_size=12)
    df_wc=wc.generate(temp['Message'].str.cat(sep=' '))
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop.txt','r')
    stop=f.read()
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    temp=df[df['User']!='group_notification']
    temp= temp[temp['Message'] != '<Media omitted>\n']

    words=[]
    for messages in temp['Message']:
        for word in messages.lower().split():
            if word not in stop:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(40))



def emoji_helper(selected_user,df):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]
    emojis=[]
    for messages in df['Message']:
        emojis.extend([c for c in messages if c in emoji.EMOJI_DATA])

    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df






