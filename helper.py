# from urlextract import URLExtract
# from wordcloud import WordCloud
# import pandas as pd
# import emoji
# from collections import Counter
# extract = URLExtract()
#
# def fetch_stats(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#     num_messages = df.shape[0]
#     words = []
#     for message in df['message']:
#         words.extend(message.split())
#     num_media_messages = df[df['message'] =='<Media omitted>\n'].shape[0]
#     links = []
#     for message in df['message']:
#         links.extend(extract.find_urls(message))
#     return num_messages, len(words),num_media_messages,len(links)
#
#
# def most_busy_users(df):
#     x = df['user'].value_counts().head()
#     df = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
#     return x,df
#
# def create_wordcloud(selected_user,df):
#     f = open('eng_words.txt', 'r')
#     english_words = f.read()
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']
#
#     def remove_english_words(message):
#         y = []
#         for word in message.lower().split():
#             if word  not in english_words:
#                 y.append(word)
#         return " ".join(y)
#     wc = WordCloud(width=500,min_font_size=10,background_color = 'white')
#     temp['message'] = temp['message'].apply(remove_english_words)
#     df_wc = wc.generate(df['message'].str.cat(sep=" "))
#     return df_wc
#
# def most_common_words(selected_user,df):
#     f=open('eng_words.txt','r')
#     english_words=f.read()
#
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#     temp = df[df['user'] != 'group_notification']
#     temp = temp[temp['message'] != '<Media omitted>\n']
#     words = []
#     for message in temp['message']:
#         for word in message.lower().split():
#             if word not in english_words:
#                 words.append(word)
#     most_common_df = pd.DataFrame(Counter(words).most_common(20))
#     return  most_common_df
# def extract_emojis(text):
#     emojis = ''.join([c for c in text if emoji.is_emoji(c)])
#     return emojis
#
# def emoji_helper(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]
#
#     emojis_per_message = df['message'].apply(extract_emojis)
#     all_emojis = [emoji for sublist in emojis_per_message for emoji in sublist]
#     emoji_counts = Counter(all_emojis)
#     emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count'])
#     emoji_df = emoji_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
#
#     return emoji_df
#

from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
import emoji
from collections import Counter

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    num_messages = df.shape[0]
    words = [word for message in df['message'] for word in message.split()]
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = [link for message in df['message'] for link in extract.find_urls(message)]
    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_user, df):
    f = open('eng_words.txt', 'r')
    english_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_english_words(message):
        return " ".join(word for word in message.lower().split() if word not in english_words)

    wc = WordCloud(width=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_english_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    f = open('eng_words.txt', 'r')
    english_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = [word for message in temp['message'] for word in message.lower().split() if word not in english_words]
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def extract_emojis(text):
    emojis = ''.join(c for c in text if emoji.is_emoji(c))
    return emojis

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis_per_message = df['message'].apply(extract_emojis)
    all_emojis = [emoji for sublist in emojis_per_message for emoji in sublist]
    emoji_counts = Counter(all_emojis)
    emoji_df = pd.DataFrame(emoji_counts.items(), columns=['Emoji', 'Count'])
    emoji_df = emoji_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return  df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()

def user_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap