import streamlit as st
from matplotlib import pyplot as plt


import preprocessor
import functions

st.sidebar.title("Whatsapp chat")


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    byte_data=uploaded_file.getvalue()
    data=byte_data.decode("utf-8")
    df=preprocessor.preprocess(data)

    st.dataframe(df)

    # drop down of all members
    unique_users=df['User'].unique().tolist()
    unique_users.sort()
    unique_users.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Select a userr",unique_users)


    #main analyusis
    if st.sidebar.button("Send Analysis"):
        num_messages,words,no_of_media,links=functions.fetch_stats(selected_user,df)

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Number Words")
            st.title(words)
        with col3:
            st.header("Total Media Files")
            st.title(no_of_media)
        with col4:
            st.header("Total Links Shared")
            st.title(links)

#Busiest people in the grp

        if selected_user == 'Overall':
            st.title("Most Busy People")
            x_axis,dff = functions.busy_peoples(selected_user, df)

            fig, ax = plt.subplots( )
            name = x_axis.index
            count = x_axis.values

            col1, col2 = st.columns(2)
            with col1:
                ax.bar(name, count)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

                with col2:
                    st.dataframe(dff,height=300)


        #Word Cloud
        st.title("WORD CLOUD")
        df_wc=functions.word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


    #most common word
        most_common_df=functions.most_common_words(selected_user,df)
        st.title("Most Common Words")

        col1,col2=st.columns([1,2])
        with col1:
            st.title("Dataset")
            st.dataframe(most_common_df)
        with col2:
            st.title("Graph")
            fig,ax=plt.subplots()
            ax.barh(most_common_df[0],most_common_df[1])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


    #emoji analysis
        emoji_df=functions.emoji_helper(selected_user,df)
        st.title("Emoji")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(7),labels=emoji_df[0].head(7),autopct='%'
                                                                          '0.2f')
            st.pyplot(fig)