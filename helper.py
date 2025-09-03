from urlextract import URLExtract
from wordcloud import WordCloud
import neattext.functions as nfx
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(Selected_user,df):

    if Selected_user == "Overall":
        return df.shape[0]
    else:
        return df[df['User']==Selected_user].shape[0]
    
def words_count(Selected_user,df):
    words = []
    if Selected_user == "Overall":
        for message in df['messager']:
            words.extend(message.split())
        return len(words)
    else:
        for message in df[df['User']==Selected_user]["messager"]:
            words.extend(message.split())
        return len(words)

def media_shared(Selected_user,df):
    if Selected_user == "Overall":
        count=0
        for message in df['messager']:
            if message==r"<Media omitted>":
                count=count+1
        return count
    else:
        for message in df[df['User']==Selected_user]["messager"]:
            count=0
            if message==r"<Media omitted>":
                count=count+1
        return count
    

def link_count(Selected_user,df):
    if Selected_user == "Overall":
        count=0
        for message in df['messager']:
            if message==r"https":
                count=count+1
        return count
    else:
        for message in df[df['User']==Selected_user]["messager"]:
            count=0
            if message==r"https":
                count=count+1
        return count
    
def most_engaged(df):
    x = df['User'].value_counts().head()
    return x

def word_cloud(Selected_user,df):
    if Selected_user == "Overall":
        df = df[df['messager'] != "Group disreption"]
        df = df[df['messager'] != "<Media omitted>"]
        df = df[df['messager'] != "This message was deleted"]
        wc = WordCloud(width=400,height=400,min_font_size=12,background_color='white')
        df_wc = wc.generate(df['messager'].str.cat(sep=" ")) 
        return df_wc
    else:
        df = df[df['messager'] != "<Media omitted>"]
        df = df[df['messager'] != "Group disreption"]
        df = df[df['messager'] != "This message was deleted"]
        wc = WordCloud(width=400,height=400,min_font_size=12,background_color='white')
        df_wc = wc.generate(df[df['User']==Selected_user]['messager'].str.cat(sep=" ")) 
        return df_wc 
    
def frequent_words(Selected_user,df):
    df2 = df
    df2['messager'] = df2['messager'].apply(nfx.remove_stopwords)
    if Selected_user == "Overall":
        s=[]
        for i in df2['messager']:
            s.append(i)
        x = []
        for i in s:
            x.extend(i.split(" "))
        counts = Counter(x)
        df3 = pd.DataFrame(counts.items(),columns=["Value", "Count"])
        df3 = df3[df3['Value'] != "Group"]
        df3 = df3[df3['Value'] != "disreption"]
        df3 = df3[df3['Value'] != " "]
        df3 = df3[df3['Value'] != "<Media"]
        df3 = df3[df3['Value'] != "omitted>"]
        df3 = df3.sort_values(by="Count", ascending=False)
        return df3
    else:
        s=[]
        for i in df[df['User']==Selected_user]['messager']:
            s.append(i)
        x = []
        for i in s:
            x.extend(i.split(" "))
        counts = Counter(x)
        df3 = pd.DataFrame(counts.items(),columns=["Value", "Count"])
        df3 = df3[df3['Value'] != "Group"]
        df3 = df3[df3['Value'] != "disreption"]
        df3 = df3[df3['Value'] != " "]
        df3 = df3[df3['Value'] != "<Media"]
        df3 = df3[df3['Value'] != "omitted>"]
        df3 = df3.sort_values(by="Count", ascending=False)
        return df3
    
def emojis_count(Selected_user,df):
    if Selected_user == "Overall":
        emojis = []
        for message in df['messager']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return df
    else:
        emojis = []
        for message in df[df['User']==Selected_user]['messager']:
            emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
        df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
        return df

def time_line(Selected_user,df):
    if Selected_user == "Overall":
        timeline = df.groupby(['Year','month_num','mounth']).count()['messager'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['mounth'][i]+" "+str(timeline['Year'][i]))
        timeline["time"] = time
        return timeline
    else:
        df2 = df[df['User']==Selected_user]
        timeline = df2.groupby(['Year','month_num','mounth']).count()['messager'].reset_index()
        time = []
        for i in range(timeline.shape[0]):
            time.append(timeline['mounth'][i]+" "+str(timeline['Year'][i]))
        timeline["time"] = time
        return timeline
    
def daily_engament(Selected_user,df):
    if Selected_user == "Overall":
        df["Day_name"] = df["Message_data"].dt.day_name()
        return df['Day_name'].value_counts()
    else:
        df["Day_name"] = df[df["User"]==Selected_user]["Message_data"].dt.day_name()
        return df['Day_name'].value_counts()
    
def monthly_engament(Selected_user,df):
    if Selected_user == "Overall":
        return df['mounth'].value_counts()
    else:
        
        return df[df["User"]==Selected_user]['Day_name'].value_counts()