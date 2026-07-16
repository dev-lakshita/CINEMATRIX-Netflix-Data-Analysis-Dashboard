import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import base64
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter

st.set_page_config(page_title="DRAFT 1",page_icon='📑',layout='wide')
df1=pd.read_csv('netflix_titles.csv')
df=pd.read_csv('cleaned_dataset.csv')
df['date_added']=pd.to_datetime(df['date_added'],errors='coerce')
df['year_added']=df['date_added'].dt.year
df['month_added']=df['date_added'].dt.month
df_movies=df[df['type']=='Movie'].copy()
df_movies['duration']=df_movies['duration'].str.replace("min",'').astype(int)
df_tv=df[df['type']=='TV Show'].copy()
df.rename(columns={'listed_in':'genre'},inplace=True)

with st.sidebar:
    st.title("📋 MENU")
    st.image('MY OBSESSION.jpeg',width=400)
    side=option_menu(menu_title="Select to View",options=["Home",'Dataset','Visualization','Insights'],icons=['house','table','bar-chart','search'])

if side=='Home': 
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
        color: #E50914;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7); /* Adds a subtle shadow for better readability */
    }
    .text-overlay-box p {
        color: #e5e5e5;                        /* Off-white color for better readability */
        font-size: 1.5rem;
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

elif side=='Dataset':
    with open('ha.jpeg','rb')as f:
        data=base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp{{background-image:url("data:image/jpeg;base64,{data}");
                background-size:cover;}}
        </style>
        """,unsafe_allow_html=True)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.metric("Total Titles",df.shape[0])
        with col2:
            st.metric("Movies",df[df['type']=="Movie"].shape[0])
        with col3:
            st.metric("TV Shows",df[df['type']=="TV Show"].shape[0])
        with col4:
            st.metric("Countries",df['country'].nunique())
        t1,t2=st.tabs(['Cleaned Dataset','Original Dataset'])
        with t2:
            st.title("Original DataSet")
            st.write(df1)
        with t1:
            st.title("Cleaned Dataset")
            st.write(df)
            st.write("Original dataset contained missing and duplicate values. Data " \
            "cleaning was performed using Pandas to handle null values,standardize columns " \
            "and prepare data for visualization")

elif side=='Visualization':
    st.title("THE VISUALIZATION PAGE")
    t1,t2,t3,t4,t5,t6=st.tabs(['Movies/TV Shows','Country Analysis','Genre','Ratings','Duration','Trends Over Years'])
    with t1:
        st.header("MOVIES VS TV SHOWS")
        c1,c2=st.columns(2)
        with c2:
            selected_year=st.slider("Select Release Year",2000,2021)
            df_new=df[df['release_year']==selected_year]
            if not df_new.empty:
                fig=px.histogram(df_new,x='type',color='type',color_discrete_map={"Movie":"#5DA3E5","TV Show":"#F15BB5"},title='Content Released each year')
                fig.update_layout(yaxis=dict(tickformat=',d'),xaxis=dict(categoryorder='array',categoryarray=['Movie','TV Show']))
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig)
            else:
                st.info(f"🎬 No Content available for the year {selected_year}")
        with c1:
             fig=px.pie(df,names='type',color='type',color_discrete_map={"Movie":"#4D9AAF","TV Show":"#ECECA8"},title='Overall Movies vs TV-Shows')
             st.plotly_chart(fig)
    with t2:
        topcntry=st.slider("SELECT TO SEE NUMBER OF TOP CONTENT PRODUCING COUNTRIES ",1,10  )
        top_country_list=df['country'].value_counts().head(topcntry).index
        df_filtered=df[df['country'].isin(top_country_list)]
        a=df_filtered.groupby(['country','type']).size().reset_index()
        a.columns=['country','type','count']
        a['country']=pd.Categorical(a['country'],categories=top_country_list,ordered=True)
        a =a.sort_values(by='country')
        c1,c2=st.columns(2)
        with c2:
            fig=px.bar(a,x="country",y='count',color='type',title=f"Top {topcntry} Content Producing Countries along with Content Type",barmode='stack')#,color_continuous_scale='reds_r')
            st.plotly_chart(fig)
        with c1:
            fig=px.pie(a,names='country',values='count',hole=0.5,title=f'Top {topcntry} Content Producing Countries')
            st.plotly_chart(fig)
        st.write(df['country'].value_counts().head(topcntry))
    with t3:
        st.title("Most Popular Genres")
        numb=st.slider("SELECT THE NUMBER OF MOVIES/TV SHOWS",1,5)
        genre_data=[]
        for idx, row in df.iterrows():
            if pd.notnull(row['genre']):
                split_genres = [genre.strip() for genre in row['genre'].split(',')]
                for genre in split_genres:
                    genre_data.append({'word': genre,'type': row['type'],'release_year': row['release_year'],'year_added': row['year_added']})
        df_genres = pd.DataFrame(genre_data)
        top_genres_list = df_genres['word'].value_counts().head(numb).index
        df_genre_filtered = df_genres[df_genres['word'].isin(top_genres_list)]
        dftop=df_genre_filtered.groupby(['word','type']).size().reset_index(name='count')
        dftop['word']=pd.Categorical(dftop['word'],categories=top_genres_list,ordered=True)
        dftop = dftop.sort_values(by='word')
        c1,c2=st.columns(2)
        with c1:
            dftop_total=df_genre_filtered['word'].value_counts().reset_index(name='count')
            dftop_total.columns=['word','count']
            fig=px.bar(dftop_total,x='count',y='word',title="No. of Occurrences of Each Genre",color='word')
            fig.update_xaxes(categoryorder='array',categoryarray=top_genres_list)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        with c2:
            avg_years=df_genre_filtered.groupby('word')['year_added'].mean().reset_index()
            avg_years.columns=['word','avg_year_added']
            avg_years['word']=pd.Categorical(avg_years['word'],categories=top_genres_list,ordered=True)
            avg_years = avg_years.sort_values(by='word')                                                                            
            fig=px.line(avg_years,x='word',y='avg_year_added',markers=True,title="Average Release Years for the top most popular Genres")
            fig.update_yaxes(autorange=True,tickformat=".1f")
            st.plotly_chart(fig)
        st.header(f"Top {numb} Genres are:")
        st.write(dftop)
    with t4:
        st.title("Ratings Analysis")
        c1,c2=st.columns(2)
        with c2:
            top_countries=df['country'].value_counts().head(10).index
            top_ratings=df['rating'].value_counts().head(10).index
            df_heatmap=df[df['country'].isin(top_countries)& df['rating'].isin(top_ratings)]
            heatmap_data=df_heatmap.groupby(['country','rating']).size().unstack(fill_value=0)
            fig=px.imshow(heatmap_data,text_auto=True,aspect='auto',color_continuous_scale="blackbody",title="Heatmap: Content Ratings across Top 10 Countries")
            fig.update_layout(xaxis_title="Content Rating",yaxis_title="Country")
            st.plotly_chart(fig)

        df_cleaned=df[~df['rating'].str.contains('min',case=False)]
        with c1:
            fig=px.histogram(df_cleaned,x='rating',color='rating')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig)
        st.write(df['rating'].value_counts().head(10))
    with t5:
        st.header("Duration Analysis")
        df_movies['duration_num']=pd.to_numeric(df_movies['duration'],errors='coerce').fillna(0).astype(float)
        df_tv['duration_num']=pd.to_numeric(df_tv['duration'],errors='coerce').fillna(0).astype(float)
        c1,c2=st.columns(2)
        with c1:
            st.subheader("Movie Runtime Distribution")
            fig=px.histogram(df_movies,x='duration_num',nbins=30,labels={'duration_num':'Duration(Minutes)'},title='Number of Movies vs Durations',color_discrete_sequence=["#1BC7E9"])
            fig.update_layout(yaxis_title="Number of Movies")
            st.plotly_chart(fig)
            st.write(df_movies['duration_num'].value_counts().head(20))
        with c2:
            st.subheader("TV Show Longetivity")
            df_tv['season_num']=df_tv['duration'].str.extract('(\d)').astype(int)
            tvs=df_tv.groupby('duration')['season_num'].first().reset_index()
            tvs['count']=df_tv['duration'].value_counts().values
            tvs=tvs.sort_values('season_num')
            fig=px.line(tvs,x='duration',y='count',markers=True,title='Number of Season per TV Show')
            fig.update_layout(xaxis_title="Number of Seasons",yaxis_title="Number of TV Shows")
            st.plotly_chart(fig)
            st.write(df_tv['season_num'].value_counts())#.head(20))
    with t6:
        st.title("Netflix Trends Over the Years")
        df_trends=df.groupby(['year_added','type']).size().reset_index(name="count")
        movies=df_trends[df_trends['type']=='Movie']
        tv_shows=df_trends[df_trends['type']=='TV Show']
        df_cleaned=df[~df['rating'].str.contains('min',case=False)].reset_index(names='count')
        ratings_counts=df_cleaned['rating'].value_counts().reset_index(name='count')
        fig=make_subplots(rows=3,cols=2,subplot_titles=("Total Content Added Over Years(Movies)","Total Content Added Over Years(TV Shows)", "Country-wise Content Trend Over Years ","Growth of Content by Genre","Cumulative Growth of Content","Content Ratings Trend Over Years"))
        fig.add_trace(go.Scatter(x=movies['year_added'],y=movies['count'],name='Movies',mode='lines+markers'),row=1,col=1)
        fig.update_yaxes(title_text="Movies Added", row=1, col=1)
        fig.add_trace(go.Scatter(x=tv_shows['year_added'],y=tv_shows['count'],name='TV Shows',mode='lines+markers'),row=1,col=2)
        fig.update_yaxes(title_text="TV Shows Added", row=1, col=2)

        
        # fig.add_trace(go.Histogram(x=df['release_year'],name='Release Year',marker_color='orange'),row=2,col=1)
        # fig.update_xaxes(title_text="Release Year", row=2, col=1)
        # fig.update_layout(height=400)
        country_df = df.copy()
        country_df['country'] = country_df['country'].fillna('Unknown')
        country_df['country'] = country_df['country'].str.split(',').str[0]
        top_country = country_df['country'].value_counts().head(5).index
        # fig.add_trace(go.Bar(x=top_country.values,y=top_country.index,orientation='h',name='Countries'),row=2,col=1)
        # fig.update_xaxes(title_text="Content Count",row=2,col=1)
        # fig.update_yaxes(title_text="Country",row=2,col=1)
        country_year=country_df.groupby(['year_added','country']).size().reset_index(name='count')
        country_year=country_year[country_year['country'].isin(top_country)]
        for c in top_countries:
            temp = country_year[country_year['country'] == c]
            fig.add_trace(go.Bar(x=temp['year_added'],y=temp['count'],name=c),row=2,col=1)
        fig.update_layout(barmode='stack')
        fig.update_xaxes(title_text="Year Added",row=2,col=1)
        fig.update_yaxes(title_text="Content Count",row=2,col=1)
        
                

        
        genre_df = df.copy()
        genre_df['genre']=genre_df['genre'].str.split(',').str[0]
        top_genres = genre_df['genre'].value_counts().head(3).index
        genre_trend = genre_df.groupby(['year_added', 'genre']).size().reset_index(name='count')
        genre_trend = genre_trend[genre_trend['genre'].isin(top_genres)]
        for g in top_genres:
            temp = genre_trend[genre_trend['genre'] == g]
            fig.add_trace(go.Scatter(x=temp['year_added'],y=temp['count'],mode='lines',name=g),row=2,col=2)
        fig.update_xaxes(title_text="Year Added",row=2,col=2)
        fig.update_yaxes(title_text="Content Count",row=2,col=2)
        cumulative = df.groupby('year_added').size().reset_index(name='count')
        cumulative['cumulative_count'] = cumulative['count'].cumsum()
        fig.add_trace(go.Scatter(x=cumulative['year_added'],y=cumulative['cumulative_count'],mode='lines+markers',name='Cumulative Growth'),row=3,col=2)
        fig.update_yaxes(title_text="Total Content",row=3,col=2)
        rating_trend = df.groupby(['year_added','rating']).size().reset_index(name='count')
        top_ratings = ['TV-MA','TV-14','PG','R']
        rating_trend = rating_trend[rating_trend['rating'].isin(top_ratings)]
        for r in top_ratings:
            temp = rating_trend[rating_trend['rating']==r]
            fig.add_trace(go.Scatter(x=temp['year_added'],y=temp['count'],mode='lines',name=r),row=3,col=1)
        fig.update_layout(height=1000,width=1100)
        fig.update_layout(barmode='stack',height=800,width=1000)
        st.plotly_chart(fig)

elif side=='Insights':
    with open('ha.jpeg','rb')as f:
        data=base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <style>
        .stApp{{background-image:url("data:image/jpeg;base64,{data}");
                background-size:cover;}}
        </style>
        """,unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.metric("Top Genre", "International Movies")
                st.caption("Most frequently occurring genre.")    
            with st.container(border=True):
                st.metric("Type of Content","Movies")
                st.caption("Movies dominate Netflix's catalog")
        with col2:
            with st.container(border=True):
                st.metric("Top Country", "United States")
                st.caption("Largest content producer.")
            with st.container(border=True):
                st.metric("Common Rating", "TV-MA")
                st.caption("The most common content rating")
        with st.container(border=True):
            st.metric("Global Expansion", "India,UK,Japan,South Korea ")
            st.caption("Thes countries are among Netflix's major content contributors after United States")
        
            # with st.container(border=True):
            #     st.metric("TV Show Longetivity", "1 Season")
            #     st.caption("The most common Season Duration")
