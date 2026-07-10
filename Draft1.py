import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter

st.set_page_config(page_title="DRAFT 1",page_icon='📑',layout='wide')
df1=pd.read_csv('netflix_titles.csv')
df=pd.read_csv('cleaned_dataset.csv')
df['date_added']=pd.to_datetime(df['date_added'],errors='coerce')
df['year_added']=df['date_added'].dt.year
df['month_added']=df['date_added'].dt.month
with st.sidebar:
    st.title("📋 MENU")
    st.image('MY OBSESSION.jpeg',width=400)
    side=option_menu(menu_title="Select to View",options=["Home",'Dataset','Visualization','Trends Over Years'],icons=['house','table','bar-chart','search'])
if side=='Home':
    # st.image('HOME.jpeg',width=100000000)import streamlit as st
    # 1. Inject the custom CSS for the dark overlay box
    st.markdown("""<style>
    .text-overlay-box {
        background-color: rgba(0, 0, 0, 0.65); /* Black with 65% opacity */
        padding: 25px;                         /* Spacing inside the box */
        border-radius: 10px;                   /* Rounded corners */
        margin-bottom: 30px;                   /* Creates the gap before images */
        border: 1px solid rgba(255, 255, 255, 0.1); /* Subtle white border */
    }
    .text-overlay-box h1 {
        margin-top: 0px;                       /* Removes extra top space from header */
        color: #ffffff;
    }
    .text-overlay-box p {
        color: #e5e5e5;                        /* Off-white color for better readability */
        font-size: 1.1rem;
        line-height: 1.6;
    }
    </style>""",
    unsafe_allow_html=True)
# 2. Render your text inside the styled HTML container
    st.markdown(
        """
        <div class="text-overlay-box">
            <h1>🎬 CINEMATRIX: NETFLIX DATA ANALYSIS</h1>
        </div>
        <div class="text-overlay-box">
            <p>
                Netflix is one of the world's largest streaming platforms, offering thousands of 
                movies and TV shows across different genres and countries. This dashboard provides 
                an interactive analysis of Netflix content to uncover trends, patterns, and insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True)

# 3. Your show posters/columns go right below this
# (The 'margin-bottom' in the CSS automatically handles the gap now!)
    with open('Favourite Colours.jpeg','rb')as f:
        data=base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp{{background-image:url("data:image/jpeg;base64,{data}");
                background-size:cover;}}
        </style>
        """,
        unsafe_allow_html=True)
    #     st.title("🎬 CINEMATRIX: NETFLIX DATA ANALYSIS ")
    #     st.markdown("###")
    #     st.subheader("Netflix is one of the world’s largest streaming platforms, offering thousands of movies and TV shows across different genres and countries. This dashboard provides an interactive analysis of Netflix content to uncover trends, patterns, and insights.")
    #     st.markdown("###")
        c1,c2,c3,c4,c5,c6,c7,c8=st.columns(8)
        with c1:
            st.image('0.jpeg')
        with c2:
            st.image('1.jpeg')
        with c3:
            st.image('2.jpeg')
        with c4:
            st.image('3.jpeg')
        with c5:
            st.image('4.jpeg')
        with c6:
            st.image('5.jpeg')
        with c7:
            st.image('6.jpeg')
        with c8:
            st.image('7.jpeg')
        # st.button("Play")
elif side=='Dataset':
    with open('ha.jpeg','rb')as f:
        data=base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp{{background-image:url("data:image/jpeg;base64,{data}");
                background-size:cover;}}
        </style>
        """,unsafe_allow_html=True)
        st.title("DataSet")
        st.write(df1)
        st.title("Cleaned Dataset")
        st.write(df)

elif side=='Visualization':
    st.title("THE VISUALIZATION PAGE")
    t1,t2,t3,t4=st.tabs(['Movies/TV Shows','Country Analysis','Genre','Ratings'])
    with t1:
        st.title("MOVIES VS TV SHOWS")
        c1,c2=st.columns(2)
        with c1:
            fig= px.histogram(df,x='type',color='type',color_discrete_map={"Movie":"#B61212","TV Show":"#F5F5F1"})
            st.plotly_chart(fig)
        with c2:
             fig=px.pie(df,names='type',color='type',color_discrete_map={"Movie":"#BD0B0B","TV Show":"#F5F5F1"})
             st.plotly_chart(fig)
    with t2:
        topcntry=st.slider("SELECT NUMBER OF TOP COUNTRIES ",1,10  )
        a=df['country'].value_counts().head(topcntry).reset_index()
        c1,c2=st.columns(2)
        with c1:
            fig=px.bar(a,x="country",y='count',color='count',title=f"Top {topcntry} Content Producing Countries")#,color_continuous_scale='reds_r')
            st.plotly_chart(fig)
        with c2:
            fig=px.pie(a,names='country',hole=0.5)
            st.plotly_chart(fig)
        st.write(df['country'].value_counts().head(topcntry))
    with t3:
        st.title("Most Popular Genres")
        numb=st.slider("SELECT THE NUMBER OF MOVIES/TV SHOWS",1,15)
        genre=[]
        for row in df['listed_in']:
            genre.extend(row.split(", "))
            top_genres=Counter(genre).most_common(numb)
        dftop=pd.DataFrame(top_genres,columns=['word','count'])
        c1,c2=st.columns([1,2])
        with c1:
            st.header(f"Top {numb} Genres are:")
            st.write(dftop)
        with c2:
            fig=px.sunburst(dftop,path=['word','count'])
            fig.update_layout(width=600,height=600)
            st.plotly_chart(fig)
    with t4:
        # misplaced_ratings=df[df['rating'].str.contains('min', na=False)]
        # print(misplaced_ratings[['title','rating','duration']])
        df_cleaned=df[~df['rating'].str.contains('min',case=False)]
        fig=px.histogram(df_cleaned,x='rating',color='rating')
        st.plotly_chart(fig)
        fig=px.histogram(df_cleaned,x='rating',color='type')
        st.plotly_chart(fig)
