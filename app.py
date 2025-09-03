import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt




st.sidebar.title("Whatsapp chat analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    st.header("Chats DataFrame")
    abc = st.dataframe(df)
    user_list = df['User'].unique().tolist()
    user_list.remove('group_notifiction')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("show Analysis W.R.T",user_list)
    num_messages = helper.fetch_stats(selected_user,df)



    if st.sidebar.button("show Analysis"):

        time_line = helper.time_line(selected_user, df)
        st.title("Chat Time Line")
        fig, ax = plt.subplots()
        ax.plot(time_line["time"], time_line["messager"], marker="o")
        plt.xticks(rotation=90)  
        st.pyplot(fig)


        col1, col2,  = st.columns(2)
        st.title("Chat Activity")

        with col1:
            st.title("Daily Activity")
            x = helper.daily_engament(selected_user,df)
            fig2, ax = plt.subplots()
            ax.bar(x.index, x.values, color="green")
            ax.set_title("Engaged(Bar)")
            ax.set_xlabel("Days")
            ax.set_ylabel("Engamennt")
            plt.xticks(rotation=45)
            st.pyplot(fig2)
        
        with col2:
            st.title("Month Activity")
            x = helper.monthly_engament(selected_user,df)
            fig2, ax = plt.subplots()
            ax.bar(x.index, x.values, color="purple")
            ax.set_title("Engaged(Bar)")
            ax.set_xlabel("Month")
            ax.set_ylabel("Engamennt")
            plt.xticks(rotation=45)
            st.pyplot(fig2)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        
        with col2:
            st.header("Total words")
            st.title(helper.words_count(selected_user,df))
        with col3:
            st.header("Media File")
            st.title(helper.media_shared(selected_user,df))
        with col4:
            st.header("Link Shared")
            st.title(helper.link_count(selected_user,df))

        if selected_user == "Overall":
            st.title("Most Engaged Users")
            x = helper.most_engaged(df)
            col1, col2 = st.columns(2)

            with col1:
                labels = x.index
                sizes = x.values

                fig, ax = plt.subplots()
                ax.pie(
                    sizes,
                    labels=labels,
                    autopct='%1.1f%%',
                    shadow=True,
                    startangle=140
                )
                ax.set_title("Most Engaged Users")
                st.pyplot(fig)

            with col2:
                fig2, ax = plt.subplots()
                ax.bar(x.index, x.values, color="red")
                ax.set_title("Most Engaged Users (Bar)")
                ax.set_xlabel("Users")
                ax.set_ylabel("Message Count")
                plt.xticks(rotation=45)
                st.pyplot(fig2)

        df_wc = helper.word_cloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.title("Word Cloud")
        st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            df3 = helper.frequent_words(selected_user,df)
            st.header(f"Most Frequent words used by {selected_user}")
            abc = st.dataframe(df3)
        with col2:
            df3 = df3.head(10)
            fig2, ax = plt.subplots()
            ax.bar(df3['Value'],df3['Count'], color="red")
            ax.set_title("Most Used words")
            ax.set_xlabel("Words")
            ax.set_ylabel("Count")
            plt.xticks(rotation=45)
            st.title("Word Count Plot")
            st.pyplot(fig2)

        col1, col2 = st.columns(2)
        
        with col1:
            st.title("Emojis Count")
            dfr = helper.emojis_count(selected_user,df)
            st.dataframe(dfr)
        with col2:
            my_list = dfr[1]
            fig, ax = plt.subplots()
            ax.pie(
                my_list,
                labels=dfr[0],
                autopct='%1.1f%%',
                shadow=True,                    
                startangle=140
            )
            ax.set_title("Emojies Frequency")
            st.title("Emojies Frequency")
            st.pyplot(fig)



