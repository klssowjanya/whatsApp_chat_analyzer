import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    try:
        df = preprocessor.preprocess(data)
    except ValueError as e:
        st.error(f"Error: {e}")

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Show analysis with respect to", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"<h3 style='text-align: center;'>Total Messages</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>{num_messages}</p>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<h3 style='text-align: center;'>Total Words</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>{words}</p>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<h3 style='text-align: center;'>Media shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>{num_media_messages}</p>",
                        unsafe_allow_html=True)

        with col4:
            st.markdown(f"<h3 style='text-align: center;'>Links shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; font-size: 24px;'>{num_links}</p>", unsafe_allow_html=True)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily_timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'],color='violet')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #activity map
        st.title('Activity Map')
        col1,col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax =plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #activity hetmap
        st.title("Weekly Activity")
        user_heatmap = helper.user_heatmap(selected_user, df)
        # st.pyplot(sns.heatmap(user_heatmap))
        fig,ax = plt.subplots()
        sns.heatmap(user_heatmap,ax=ax)
        st.pyplot(fig)

        # Finding the busiest user in the group (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='pink')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most Common Words
        st.markdown(f"<h3 style='text-align: center;'>Most Common Words</h3>", unsafe_allow_html=True)
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Emoji Analysis
        st.markdown(f"<h3 style='text-align: center;'>Emoji Analysis</h3>", unsafe_allow_html=True)
        emoji_df = helper.emoji_helper(selected_user, df)
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(), autopct="%0.2f")
            st.pyplot(fig)
