import streamlit as st
import sqlite3
from numerize import numerize
import pandas as pd

df = pd.read_csv('Data.csv')

states = list(df['State_Name'].unique())

st.sidebar.title("India Crop Production Analysis Using MySql")

user_menu = st.sidebar.radio('Select Option',
    ["How much is the total and average production?",
    "Which was the most productive year?",
    "Which are the most productive crops overall?",
    "Which are the most productive crops for particular state?",
    "Which is most productive crop with respect to district and year?",
    "Which is most productive year with respect to district and crop?",
    "Which are the most productive crops accoding to different seasons",
    "Which season suits the particular crop most?"]
)

st.sidebar.write("[Connect](https://www.linkedin.com/in/anaranje/)")
st.sidebar.write("[Get Data](https://data.world/thatzprem/agriculture-india)")

sqliteConnection = sqlite3.connect('cropdata.db', timeout=10)
cursor = sqliteConnection.cursor()


if user_menu=="How much is the total and average production?":
    sql_query = '''
    SELECT sum(Production) as Total_Production, 
    round(AVG(Production),3) as Average_Production 
    from cropdata;'''

    cursor.execute(sql_query)
    ans = cursor.fetchone()


    total_prodution = numerize.numerize(ans[0])
    average_production = numerize.numerize(ans[1])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Total Production")
        st.subheader(total_prodution)
    
    with col2:
        st.subheader("Average Production")
        st.subheader(average_production)


    checkbox1 = st.checkbox("Show Query")

    if checkbox1:
        st.code(sql_query.upper())


if user_menu=="Which was the most productive year?":
    sql_query = '''
    select Crop_Year, sum(Production) as Production 
    FROM cropdata 
    GROUP BY Crop_Year 
    ORDER by Production DESC;'''

    cursor.execute(sql_query)
    ans = cursor.fetchall()

    year = []
    production = []
    data = pd.DataFrame()

    for i in ans:
        year.append(i[0])
        production.append(numerize.numerize(i[1]))

    data['Year'] = year
    data['Production in tons'] = production

    st.header("Total Production By Year")
    st.dataframe(data)

    checkbox2 = st.checkbox("Show Query")

    if checkbox2:
        st.code(sql_query.upper())


if user_menu=="Which are the most productive crops overall?":
    sql_query = '''
    SELECT Crop, sum(Production) as Production
	FROM cropdata
	GROUP BY Crop
	ORDER BY Production DESC;'''

    cursor.execute(sql_query)
    ans = cursor.fetchall()

    crop = []
    production = []
    data = pd.DataFrame()

    for i in ans:
        crop.append(i[0])
        production.append(numerize.numerize(i[1]))

    data['Crop'] = crop
    data['Production in tons'] = production

    st.header("Total Production Per Crop")
    st.dataframe(data)

    checkbox3 = st.checkbox("Show Query")

    if checkbox3:
        st.code(sql_query.upper())


if user_menu=="Which are the most productive crops for particular state?":
    state_selected = st.selectbox("Select State",states)
    
    sql_query = f'''SELECT Crop, sum(Production) as Production 
    FROM cropdata 
    WHERE State_Name='{state_selected}' 
    GROUP by Crop 
    ORDER BY Production desc;'''

    cursor.execute(sql_query)
    ans = cursor.fetchall()

    crop = []
    production = []
    data = pd.DataFrame()

    for i in ans:
        crop.append(i[0])
        production.append(numerize.numerize(i[1]))

    data['Crop'] = crop
    data['Production in tons'] = production

    st.subheader(f"Most productive crops for {state_selected}")
    st.dataframe(data)

    checkbox4 = st.checkbox("Show Query")

    if checkbox4:
        st.code(sql_query.upper())


if user_menu=='Which is most productive crop with respect to district and year?':
    selected_state = st.selectbox('Select State',states)

    districts = list(df[df['State_Name']==selected_state]['District_Name'].unique())
    districts.insert(0,'All')
    selected_district = st.selectbox('Select District',districts)

    if selected_district=='All':
        years = list(df[df['State_Name']==selected_state]['Crop_Year'].unique())
    else:
        years = list(df[(df['State_Name']==selected_state) & (df['District_Name']==selected_district)]['Crop_Year'].unique())

    
    years.insert(0,'All')
    selected_year = st.selectbox('Selecte Year',years)


    if selected_district=='All' and selected_year=='All':
        sql_query = f'''
        SELECT District_Name as District, sum(Production) as Production
        FROM cropdata
        where State_Name='{selected_state}'
        GROUP BY District
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        district = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            district.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['District'] = district
        data['Production in tons'] = production
        title = f'District Wise Overall Production for {selected_state}'


    if selected_district!='All' and selected_year=='All':
        sql_query = f'''
        SELECT Crop_Year, sum(Production) as Production
        FROM cropdata
        WHERE State_Name='{selected_state}' and District_Name='{selected_district}'
        GROUP BY Crop_Year
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        year = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            year.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['Year'] = year
        data['Production in tons'] = production
        
        title = f'Year Wise Overall Production in {selected_state} for {selected_district} District'


    if selected_district=='All' and selected_year!='All':
        sql_query = f'''
        SELECT District_Name as District, sum(Production) as Production
        FROM cropdata
        where State_Name='{selected_state}' and Crop_Year={selected_year}
        GROUP BY District
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        district = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            district.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['District'] = district
        data['Production in tons'] = production

        title = f'District Wise Overall Production for {selected_state} in {selected_year}'


    if selected_district!='All' and selected_year!='All':
        sql_query = f'''
        SELECT District_Name as District, 
        Crop_Year, sum(Production) as Production
        FROM cropdata
        WHERE State_Name='{selected_state}' and District_Name='{selected_district}' and Crop_Year={selected_year};'''

        cursor.execute(sql_query)
        ans = cursor.fetchone()

        data = pd.DataFrame()
        data['District'] = [ans[0]]
        data['Year'] = [ans[1]]
        data['Production in tons'] = [numerize.numerize(ans[2])]


        title = f'Total Production for {selected_state} in {selected_district} District in {selected_year}'

    st.markdown(title)
    st.dataframe(data)

    checkbox5 = st.checkbox("Show Query")

    if checkbox5:
        st.code(sql_query.upper())



if user_menu=='Which is most productive year with respect to district and crop?':
    selected_state = st.selectbox('Select State',states)

    districts = list(df[df['State_Name']==selected_state]['District_Name'].unique())
    districts.insert(0,'All')
    selected_district = st.selectbox('Select District',districts)

    if selected_district=='All':
        crops = list(df[df['State_Name']==selected_state]['Crop'].unique())
    else:
        crops = list(df[(df['State_Name']==selected_state) & (df['District_Name']==selected_district)]['Crop'].unique())

    
    crops.insert(0,'All')
    selected_crop = st.selectbox('Selecte Crop',crops)


    if selected_district=='All' and selected_crop=='All':
        sql_query = f'''
        SELECT Crop_Year, sum(Production) as Production
        FROM cropdata
        where State_Name='{selected_state}'
        GROUP BY Crop_Year
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        year = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            year.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['Year'] = year
        data['Production in tons'] = production

        title = f'Year Wise Overall Production for {selected_state}'


    if selected_district!='All' and selected_crop=='All':
        sql_query = f'''
        SELECT Crop_Year, sum(Production) as Production
        FROM cropdata
        WHERE State_Name='{selected_state}' and District_Name='{selected_district}'
        GROUP BY Crop_Year
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        year = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            year.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['Year'] = year
        data['Production in tons'] = production

        title = f'Year Wise Overall Production for {selected_state} in {selected_district} District'


    if selected_district=='All' and selected_crop!='All':
        sql_query = f'''
        SELECT Crop_Year, sum(Production) as Production
        FROM cropdata
        where State_Name='{selected_state}' and Crop='{selected_crop}'
        GROUP BY Crop_Year
        ORDER BY Production DESC;'''

        cursor.execute(sql_query)
        ans = cursor.fetchall()

        year = []
        production = []
        data = pd.DataFrame()

        for i in ans:
            year.append(i[0])
            production.append(numerize.numerize(i[1]))

        data['Year'] = year
        data['Production in tons'] = production

        title = f'Year Wise Overall Production for {selected_state} of {selected_crop}'


    if selected_district!='All' and selected_crop!='All':
        sql_query = f'''
        SELECT Crop_Year, 
        District_Name as District, sum(Production) as Production
        FROM cropdata
        WHERE State_Name='{selected_state}' and District_Name='{selected_district}' and Crop='{selected_crop}';'''

        cursor.execute(sql_query)
        ans = cursor.fetchone()

        data = pd.DataFrame()
        data['Year'] = [ans[0]]
        data['District'] = [ans[1]]
        data['Production in tons'] = [numerize.numerize(ans[2])]

        title = f'Total Production for {selected_state} in {selected_district} District of {selected_crop}'

    st.markdown(title)
    st.dataframe(data)

    checkbox5 = st.checkbox("Show Query")

    if checkbox5:
        st.code(sql_query.upper())


if user_menu=="Which are the most productive crops accoding to different seasons":
    states1 = states
    states1.insert(0, 'All')
    selected_state = st.selectbox('Select State', states1)

    if selected_state=="All":
        seasons = list(df['Season'].unique())
    else:
        seasons = list(df[df['State_Name']==selected_state]['Season'].unique())
    selected_season = st.selectbox("Select Season", seasons)

    if selected_state=="All":
        sql_query = f'''
        select Crop, sum(Production) as Production
        FROM cropdata
        WHERE Season='{selected_season}'
        GROUP BY Crop
        ORDER BY Production desc'''

        title = f'Total Production in {selected_season} Season'
    else:
        sql_query = f'''
        select Crop, sum(Production) as Production
        FROM cropdata
        WHERE Season='{selected_season}' and State_Name = '{selected_state}'
        GROUP BY Crop
        ORDER BY Production desc'''

        title = f'Total Production for {selected_state} in {selected_season} Season'

    cursor.execute(sql_query)
    ans = cursor.fetchall()

    crop = []
    production = []
    data = pd.DataFrame()

    for i in ans:
        crop.append(i[0])
        production.append(numerize.numerize(i[1]))

    data['Crop'] = crop
    data['Production in tons'] = production


    st.markdown(title)
    st.dataframe(data)

    checkbox6 = st.checkbox("Show Query")

    if checkbox6:
        st.code(sql_query.upper())


if user_menu=="Which season suits the particular crop most?":
    states1 = states
    states1.insert(0, 'All')
    selected_state = st.selectbox('Select State', states1)

    if selected_state=="All":
        crops = list(df['Crop'].unique())
    else:
        crops = list(df[df['State_Name']==selected_state]['Crop'].unique())
    selected_crop = st.selectbox("Select Season", crops)

    if selected_state=="All":
        sql_query = f'''
        select Season, sum(Production) as Production
        FROM cropdata
        WHERE Crop='{selected_crop}'
        GROUP BY Season
        ORDER BY Production desc;'''

        title = f'Total Production of {selected_crop}'
    else:
        sql_query = f'''
        select Season, sum(Production) as Production
        FROM cropdata
        WHERE Crop='{selected_crop}' and State_Name='{selected_state}'
        GROUP BY Season
        ORDER BY Production desc;'''

        title = f'Total Production for {selected_state} of {selected_crop}'

    cursor.execute(sql_query)
    ans = cursor.fetchall()

    season = []
    production = []
    data = pd.DataFrame()

    for i in ans:
        season.append(i[0])
        production.append(numerize.numerize(i[1]))

    data['Season'] = season
    data['Production in tons'] = production


    st.markdown(title)
    st.dataframe(data)

    checkbox7 = st.checkbox("Show Query")

    if checkbox7:
        st.code(sql_query.upper())
