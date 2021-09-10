import streamlit as st  
import pandas as pd  
import plotly.express as px 
import base64  
from io import StringIO, BytesIO  
import time


def generate_excel_download_link(df):
    towrite = BytesIO()
    df.to_excel(towrite, encoding="utf-8", index=False, header=True)  # write to BytesIO buffer
    towrite.seek(0)  # reset pointer
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="data_download.xlsx">Download Excel File</a>'
    return st.markdown(href, unsafe_allow_html=True)

def generate_html_download_link(fig):
    towrite = StringIO()
    fig.write_html(towrite, include_plotlyjs="cdn")
    towrite = BytesIO(towrite.getvalue().encode())
    b64 = base64.b64encode(towrite.read()).decode()
    href = f'<a href="data:text/html;charset=utf-8;base64, {b64}" download="plot.html">Download Plot</a>'
    return st.markdown(href, unsafe_allow_html=True)

def switcher(value):
        '''
            Above -8         Very Good           	
            >=-12  to < -8  Good  	
            >=-16 to < -12  Medium   	
            Below -16       Bad       	
        '''
        if value > - 8 :
            return "Very Good"
        elif value < -8 and value >= -12 :
            return "Good"
        elif value < -12 and value >= -16 :
            return "Medium"
        elif value < -16 :
            return "Bad"

if __name__ == '__main__':
    st.set_page_config(page_title='Excel Plotter')
    st.title('Excel Plotter 📈')
    st.subheader('Feed me with your Excel file')

    uploaded_file = st.file_uploader('Choose a XLSX file', type='xlsx')
    if uploaded_file:
        st.markdown('---')
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        df['is_ecno'] = [ switcher(item) if item else "Good" for item in df["ecno"] ]
        
        st.dataframe(df )
        groupby_column = st.selectbox(
            ' Analyse by ',
            ('ecno',),
        )
        
        # -- GROUP DATAFRAME
        output_columns = [groupby_column]
        df_grouped = df.groupby(by=[groupby_column], as_index=False)[output_columns].sum()
        # -- PLOT DATAFRAME
        fig = px.bar(
        df_grouped,
        y=df['is_ecno'],
        x=df['ecno'],
        color_continuous_scale=['red', 'yellow', 'green'],
        template='plotly_white',
        title=f'<b>Analyse by {groupby_column}</b>'
    )
        st.plotly_chart(fig)
        
        is_enco = list(df['is_ecno'].values)
        status = ["Good" , "Very Good" , "Medium" , "Bad"]
        for statu in status :
            x = is_enco.count(statu)
            x = (x * 100 )/len(is_enco)
            good = st.empty().text(f"{statu} : {x:.2f} %")
            bar = st.progress(int(x))
        
        # -- DOWNLOAD SECTION
        st.subheader('Downloads:')
        generate_excel_download_link(df_grouped)
        generate_html_download_link(fig)
