import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import dfprocess
import supporter
import numpy as np

st.sidebar.image('https://e7.pngegg.com/pngimages/102/349/png-clipart-whatsapp-computer-icons-logo-whatsapp-green-and-white-what-s-up-logo-grass-desktop-wallpaper.png',width=100)
st.sidebar.info('NOT powered by Whatsapp')
st.sidebar.title('Whatsapp Chat Analyzer')
upload = st.sidebar.file_uploader('Upload Your Chat History File',type=['txt'],accept_multiple_files=False)

if upload is not None:

    data = upload.getvalue().decode('utf-8')

    dataframe = dfprocess.preprocess(data)

    frame= dataframe.copy()
    list = frame['message']!='joined to group'
    df1= frame[list]
    list0= df1['message']!= 'added to group'
    df2= df1[list0]
    x= df2['user'] != 'group_notification'
    df_1 = df2[x]
    
    v1 = st.title('Whatsapp Chat')
    v2= st.dataframe(df_1)

    frame1=dataframe.copy()
    list1 = ((frame1['message']=='joined to group')|(frame1['message']=='added to group'))
    df3= frame1[list1]
    user_list = df3['user'].unique().tolist() 
    user_list.sort()

    v3 =st.header('Total Members')
    v4 = st.title(len(user_list))
    

    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Chat Analysis of ',user_list)
    df = dataframe.copy()

    if selected_user == 'Overall':

        st.title('Most Active Members')
            
        x, new_df=supporter.most_busy_user(df)
        fig, ax= plt.subplots()
            
        col1,col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values, color='green')
            plt.xlabel("Member")
            plt.ylabel("Number of Message")
            plt.xticks(rotation=90)
            st.pyplot(fig)

        with col2:
            st.dataframe(new_df)

    if st.sidebar.button('Show'):
        v1.empty()
        v2.empty()
        v3.empty()
        v4.empty()
       
        user_df = supporter.dataframe(selected_user,df)
        st.title('Member Chat')
        st.dataframe(user_df)
        st.title("Member Statistic")
        num_messages, words, num_media, links = supporter.fetch_stats(selected_user,df)

        col1, col2, col3, col4= st.columns(4)

        with col1:
            st.header("Total Messages Sent")
            st.title(num_messages)

        with col2:
            st.header("Total Words Used")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media)

        with col4:
            st.header("Total Links Shared")
            st.title(links)

        if user_df.empty:
            st.header("Non Active Member")
        else:
            st.title("Monthly Timeline")
            timeline_df= supporter.monthly_timeline(selected_user, dataframe)
            fig, ax= plt.subplots()
            plt.bar(timeline_df['time'],timeline_df['message'])
            plt.xlabel("Month")
            plt.ylabel("Number of Message")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
            st.title("Daily Timeline")
            daily_timeline_df= supporter.daily_timeline(selected_user, dataframe)
            fig, ax= plt.subplots()
            plt.plot(daily_timeline_df['date'],daily_timeline_df['message'], color='black')
            plt.xlabel("Days")
            plt.ylabel("Number Of Message")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
            st.title("Activity Map")
            col1, col2= st.columns(2)
            
            with col1:
                st.header('Most Busy Day')
                busy_day=supporter.weekly_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color='red')
                plt.xlabel("Day")
                plt.ylabel("Number of Message")
                plt.xticks(rotation=45)
                st.pyplot(fig)
                
            with col2:
                st.header('Most Busy Month')
                busy_month=supporter.month_activity(selected_user, df)
            
                fig, ax= plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color='orange')
                plt.xlabel("Month")
                plt.ylabel("Number of Message")
                plt.xticks(rotation=45)
                st.pyplot(fig)

            st.title('Most Commonly Used Words')
            common_df= supporter.most_common_words(selected_user,df)

            col1,col2 = st.columns(2)

            with col1:
                fig, ax= plt.subplots()
                ax.bar(common_df[0], common_df[1])
                plt.xlabel("Commonly Used Words")
                plt.ylabel("Number of Use")
                plt.xticks(rotation=90)
                st.pyplot(fig)

            with col2:
                st.dataframe(common_df)
        
        
            st.title('Commonly Shared Emoji')
            emoji_df = supporter.show_emoji(selected_user,df)
        
        
            if emoji_df.empty:
                st.write('No Emoji was Sent')
        
            else :
                col1,col2 = st.columns(2)
            
                with col1:
                    st.dataframe(emoji_df)
                
                with col2:
                    fig, ax= plt.subplots()
                    ax.pie(emoji_df[1], labels= emoji_df[0])
                    plt.legend(emoji_df[0], loc ="best")
                    st.pyplot(fig)
