import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from streamlit import session_state
from io import BytesIO 
try:
    with open("data_visualization_app.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except Exception as e:
    st.error("❌ Error Occurred")
    st.code(str(e))
@st.cache_data
def load_data(uploaded_file):
    """Load CSV file with caching"""
    # return uploaded_file
    return pd.read_csv(uploaded_file)

def fig_to_bytes(fig, fmt="png", dpi=300, transparent=False):
    buf = BytesIO()
    fig.savefig(
        buf,
        format=fmt,
        dpi=dpi,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        transparent=transparent,
    )
    buf.seek(0)
    return buf
st.set_page_config(page_title="Data Visualization App", layout="wide",page_icon="📊", initial_sidebar_state="expanded",
                   menu_items={
        "Get Help": "https://docs.streamlit.io",
        "Report a bug": "https://github.com/your-repo/issues",
        "About": """
                ### 📊 Data Visualization App  
                Visualize your datasets with ease using various charts powered by Seaborn & Streamlit.

                👨‍💻 Developed by: **Fakhur Ali 23-bsIT-29**  
                🛠️ Version: `v1.0.0`  
                🔗 GitHub: [Visit Repo](https://github.com/your-username/your-repo)  
                        """})


#********************************************css start***************************************************


st.title("Data visualization app")
st.subheader("Upload file here and explore your data")
uploaded_file = st.file_uploader("📂 upload csv file here: ",type=['csv','xlsx','txt'])





# ************************* GLOBAL VARIABLES ***********************



plots=["Scatter plot","Line plot","Bar plot","Count plot","Pair plot","Histogram plot","Box plot","relational plot"]
    
palette_options = [
'dark','Dark2','Set1','Set2','Set3','deep', 'Accent','pastel','Pastel1','Pastel2', 'muted', 'bright',   'colorblind',
'tab10', 'tab20','coolwarm', 'RdBu', 'BrBG', 'PiYG', 'Spectral', 'vlag', 'icefire','rocket', 'mako', 'flare', 'crest',
'Blues', 'Greens', 'Oranges', 'Purples', 'Reds', 'YlGnBu', 'YlOrBr', 'YlOrRd','twilight', 'twilight_shifted', 'hsv',
'cubehelix'
            ]

def reset_inputs():
    # Get current plot type (default to scatter)
    current_plot = session_state.get('current_plot', 'scatter')
    
    # Reset based on plot type
    if current_plot in ['scatter', 'line', 'relational']:
        session_state.ind_x = session_state.defaults['scatter_x']
        session_state.ind_y = session_state.defaults['scatter_y']
    elif current_plot in ['bar', 'box', 'count']:
        session_state.ind_x = session_state.defaults['bar_x']
        session_state.ind_y = session_state.defaults['bar_y']
    elif current_plot == 'histogram':
        session_state.ind_x = session_state.defaults['hist_x']
        session_state.ind_stat = session_state.defaults['stat']
        session_state.ind_mult = session_state.defaults['multiple']
        session_state.ind_elem = session_state.defaults['element']
    elif current_plot == 'pair':
        session_state.ind_spac = session_state.defaults['pair_cols']
        session_state.ind_kind = session_state.defaults['pair_kind']
        session_state.ind_diag = session_state.defaults['pair_diag']

    elif current_plot == 'facetgrid':
        # Reset plot type and color
        
        session_state.gr_color = session_state.defaults['facet_color']
        
        # Reset axes based on plot type
        if session_state.gr_kind in ["kdeplot", "histplot"]:
            session_state.gr_x = session_state.defaults['facet_num_x']
        elif session_state.gr_kind == "countplot":
            session_state.gr_x2 = session_state.defaults['facet_cat_x']
        else:  # Other plot types
            session_state.gr_x2 = session_state.defaults['facet_cat_x']
            session_state.gr_y = session_state.defaults['facet_y']
        
        # Reset grouping options
        session_state.gr_col = "No Any"
        session_state.gr_row = "No Any"
        session_state.gr_hue = "No Any"
         
    # Reset common settings
    session_state.ind_hue = session_state.defaults['hue']
    session_state.ind_color = session_state.defaults['color']
    session_state.ind_style = session_state.defaults['style']
    session_state.ind_est = session_state.defaults['estimator']
    
    

#************************************************************************************


if uploaded_file is not None:
    
    df=load_data(uploaded_file)
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    categ = ["No Any"] + categorical_cols.tolist()
    numberic_cols = df.select_dtypes(include=['number']).columns.tolist()
    num_col=["All"] + numberic_cols
    seaborn_compatible_plots = [
            'scatterplot', 'lineplot', 'barplot', 'boxplot', 'violinplot', 'stripplot',
            'swarmplot', 'histplot', 'kdeplot', 'pointplot', 'countplot' ]

    if "defaults" not in session_state:
        session_state.defaults = {
            # Scatter/Line/Relational plots
            'scatter_x': df.columns[0],
            'scatter_y': df.columns[1] if len(df.columns) > 1 else df.columns[0],
            
            # Bar/Box/Count plots
            'bar_x': categorical_cols[0] if len(categorical_cols) > 0 else df.columns[0],
            'bar_y': numberic_cols[0] if len(numberic_cols) > 0 else df.columns[0],
            
            # Histogram
            'hist_x': numberic_cols[0] if len(numberic_cols) > 0 else df.columns[0],
            'stat': "count",
            'element': "bars",
            'multiple': "dodge",
           
            

            'pair_cols': numberic_cols,  
            'pair_kind': "scatter",      
            'pair_diag': "auto" ,        

            
            
            'facet_num_x': numberic_cols[0] if len(numberic_cols) > 0 else df.columns[0],  
            'facet_cat_x': categorical_cols[0] if len(categorical_cols) > 0 else df.columns[0], 
            'facet_y': numberic_cols[0] if len(numberic_cols) > 0 else df.columns[0],  
            'facet_color': palette_options[0], 
            
            # Common
            'hue': "No Any",
            'color': 'dark',
            'style': "No Any",
            'estimator': "mean"


        }
    

    

    
    #**************************fatching data ********************************************
    with st.expander("Preview data"):
        st.dataframe(df.head())
    with st.expander("Basic info"):
        st.dataframe(df.describe())
        st.write(f"Rows : {df.shape[0]} _ Columns : {df.shape[1]}")
    with st.expander("📂 Filter data"):
        col = st.selectbox("🔎 Choose a column to filter", df.columns,key="filter",index=3)
        st.subheader(f"Filter by {col}")

        if pd.api.types.is_numeric_dtype(df[col]):
            min_val = float(df[col].min())
            max_val = float(df[col].max())
            val_range = st.slider(f"🔢 Pick a numeric range of {col}:", min_val, max_val, (min_val,max_val))
            filtered_data = df[(df[col] >= val_range[0]) & (df[col] <= val_range[1])]
        else:
            options = sorted(df[col].dropna().unique())
            selected = st.selectbox(f"🔽 Select a value to filter {col}:", options,key="selected")
            filtered_data = df[df[col] == selected]

        st.dataframe(filtered_data)
        st.write(f"🔢 {len(filtered_data)} rows found.")
    
    # *********************** visualization**********************************
    st.sidebar.title("Plot settings")
    plot_mode = st.sidebar.radio("Select Plot Mode :", ["📈 Single Plot", "🗂️ FacetGrid"])

    if plot_mode == "📈 Single Plot":
         st.sidebar.subheader(" 📈 Individual Plots (Single Chart)")
         plot = st.sidebar.selectbox("Select plot type",plots,index=None,key="ind_plot")
    
         if plot == "Scatter plot":
            session_state['current_plot'] = 'scatter'
            x=st.sidebar.selectbox("Select column for x-axis:",df.columns,key="ind_x")
            y_index = 1 if len(df.columns) > 1 else 0
            y=st.sidebar.selectbox("Select column for y-axis:",df.columns,index=y_index,key="ind_y")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category):",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            style=st.sidebar.selectbox("✨ Style (symbol/line variation)",categ,key="ind_style")
            style = None if style == "No Any" else style

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")
            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered = False

            with col1:
                if st.button("Generate Plot", key="scatter"):
                     plot_triggered = True                                        

            with col2:
                if st.button("Clear",on_click=reset_inputs):
                     pass
            if plot_triggered :
                        st.subheader("Data Visualization",divider=True)                
                        st.markdown(f"### 📊 {plot.title()}")
                        plt.figure(figsize=(10,6))
                        
                        sns.scatterplot(data=df,x=x,y=y,palette=color,hue=hue,style=style,alpha=1,s=100)
                        fig = plt.gcf()
                        st.pyplot(fig)
                        
                        st.download_button(
                            label="⬇️ Download chart",
                            data=fig_to_bytes(fig,fmt="png", dpi=300),
                            file_name=f"{plot.lower().replace(' ', '_')}.png",
                            mime="image/png")           
                        plt.close(fig)
         elif plot == "Line plot":
            session_state['current_plot'] = 'line'
            x=st.sidebar.selectbox("Select column for x-axis:",df.columns,key="ind_x")
            y_index = 1 if len(df.columns) > 1 else 0
            y=st.sidebar.selectbox("Select column for y-axis:",df.columns,index=y_index,key="ind_y")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            style=st.sidebar.selectbox("✨ Style (symbol/line variation)",categ,key="ind_style")
            style = None if style == "No Any" else style

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered = False

            with col1:
                if st.button("Generate Plot", key="line"):
                     plot_triggered = True
                     
                     
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                     pass
            if plot_triggered:
                     st.subheader("Data Visualization",divider=True)
                     st.markdown(f"### 📊 {plot.title()}")               
                     plt.figure(figsize=(10,6))
                     sns.lineplot(data=df,x=x,y=y,hue=hue,style=style,palette=color)
                     fig = plt.gcf()
                     st.pyplot(fig)
                        
                     st.download_button(
                            label="⬇️ Download chart",
                            data=fig_to_bytes(fig,fmt="png", dpi=300),
                            file_name=f"{plot.lower().replace(' ', '_')}.png",
                            mime="image/png")           
                     plt.close(fig)

         elif plot == "Bar plot":
            session_state['current_plot'] = 'bar'
            x=st.sidebar.selectbox("Select column for x-axis:",categorical_cols,key="ind_x")        
            y=st.sidebar.selectbox("Select column for y-axis:",df.columns,key="ind_y")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            estimator = st.sidebar.selectbox("🧮 Aggregation method",["mean","sum"],key="ind_est")
            
            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")
            
            
            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered = False

            with col1:
                if st.button("Generate Plot", key="bar"):
                     plot_triggered = True
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                     pass
            if plot_triggered:
                     st.subheader("Data Visualization",divider=True)
                     st.markdown(f"### 📊 {plot.title()}")
                     plt.figure(figsize=(10,6))            
                     sns.barplot(data=df,x=x,y=y,hue=hue,palette=color,legend=True ,estimator=estimator,saturation=1)
                     fig = plt.gcf()
                     st.pyplot(fig)
                        
                     st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig,fmt="png", dpi=300),
                        file_name=f"{plot.lower().replace(' ', '_')}.png",
                        mime="image/png")           
                     plt.close(fig)
         elif plot == "Histogram plot":
            session_state['current_plot'] = 'histogram'

            x=st.sidebar.selectbox("Select column for x-axis:",df.columns,key="ind_x")

            stat=st.sidebar.selectbox("select stat(What the y-axis shows.)",["count","probability","density"],key="ind_stat")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue
            if hue != None:
                multiple=st.sidebar.selectbox("📤 Display method for groups",["dodge","layer","stack","fill"],key="ind_mult")
            else: multiple = "dodge"

            element = st.sidebar.selectbox("📐 Histogram shape",["bars","step","poly"],key="ind_elem")

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")
            enable_kde = st.sidebar.toggle("Use KDE", value=True)

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered = False
            with col1:
                if st.button("Generate Plot", key="hist"):
                    plot_triggered = True
                    
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                    pass
            if plot_triggered:
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {plot.title()}")
                    plt.figure(figsize=(10,6))
                    sns.histplot(data=df,x=x,kde=enable_kde,hue=hue,stat=stat,multiple=multiple,element=element,palette=color)
                    fig = plt.gcf()
                    st.pyplot(fig)
                        
                    st.download_button(
                            label="⬇️ Download chart",
                            data=fig_to_bytes(fig,fmt="png", dpi=300),
                            file_name=f"{plot.lower().replace(' ', '_')}.png",
                            mime="image/png")           
                    plt.close(fig)

         elif plot == "Box plot":
            session_state['current_plot'] = 'box'
            x=st.sidebar.selectbox("Select column for x-axis:",categorical_cols,key="ind_x")
            y=st.sidebar.selectbox("Select column for y-axis:",df.columns,key="ind_y")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered=False

            with col1:
                if st.button("Generate Plot", key="box"):
                    plot_triggered=True
                    
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                    pass
            if plot_triggered:
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {plot.title()}")
                    plt.figure(figsize=(10,6))
                    sns.boxplot(data=df,x=x,y=y,hue=hue,palette=color,width=0.7,linewidth=3,saturation=0.9)
                    fig = plt.gcf()
                    st.pyplot(fig)
                    
                    st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig,fmt="png", dpi=300),
                        file_name=f"{plot.lower().replace(' ', '_')}.png",
                        mime="image/png")           
                    plt.close(fig)

         elif plot == "relational plot":
            session_state['current_plot'] = 'relational'
            x=st.sidebar.selectbox("Select column for x-axis:",df.columns,key="ind_x")
            y_index = 1 if len(df.columns) > 1 else 0
            y=st.sidebar.selectbox("Select column for y-axis:",df.columns,index=y_index,key="ind_y")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            style=st.sidebar.selectbox("✨ Style (symbol/line variation)",categ,key="ind_style")
            style = None if style == "No Any" else style

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered=False

            with col1:
                if st.button("Generate Plot", key="rel"):
                    plot_triggered=True
                
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                    pass
            if plot_triggered:
                    
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {plot.title()}")
                    g=sns.relplot(data=df,x=x,y=y,hue=hue,palette=color,style=style,height=4,aspect=1.5)
                    fig = getattr(g, "figure", getattr(g, "fig", None))
                    st.pyplot(fig)
                    st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig,fmt="png", dpi=300),
                        file_name=f"{plot.lower().replace(' ', '_')}.png",
                        mime="image/png")           
                    plt.close(fig)
            
         elif plot == "Count plot":
            session_state['current_plot'] = 'count'
            x=st.sidebar.selectbox("Select column for x-axis:",categorical_cols,key="ind_x")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered=False

            with col1:
                if st.button("Generate Plot", key="count"):
                    plot_triggered=True
                
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                    pass
            if plot_triggered:
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {plot.title()}")
                    plt.figure(figsize=(10,6))
                    sns.countplot(data=df,x=x,palette=color,hue=hue,saturation=1)
                    fig = plt.gcf()
                    st.pyplot(fig)
                    
                    st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig,fmt="png", dpi=300),
                        file_name=f"{plot.lower().replace(' ', '_')}.png",
                        mime="image/png")           
                    plt.close(fig)

         elif plot == "Pair plot":
            session_state['current_plot'] = 'pair'

            spacific_col=st.sidebar.multiselect("🔬 Specific columns to include",options=numberic_cols,
                                                default=numberic_cols,key="ind_spac",
                                                help="You can include spacific colums and remove unwantrd")

            kind=st.sidebar.selectbox("Choice kind",["scatter","reg","hist","kde"],key="ind_kind")
            diag_kind=st.sidebar.selectbox("📌 Diagonal plot type",["auto","hist","kde"],key="ind_diag")

            hue=st.sidebar.selectbox("🎨 Hue (color split by category)",categ,key="ind_hue")
            hue = None if hue == "No Any" else hue

            color=st.sidebar.selectbox("🎨 Choose color palette",palette_options,key="ind_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered=False

            with col1:
                if st.button("Generate Plot", key="pair"):
                    plot_triggered=True
                
            with col2:
                if st.button("Clear", on_click=reset_inputs):
                    pass
            if plot_triggered:
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {plot.title()}")
                    pair=sns.pairplot(data=df,palette=color,hue=hue,kind=kind,diag_kind=diag_kind,vars=spacific_col,height=2,aspect=1.5)
                    fig = getattr(pair, "figure", getattr(pair, "fig", None))
                    st.pyplot(fig)
                    st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig,fmt="png", dpi=300),
                        file_name=f"{plot.lower().replace(' ', '_')}.png",
                        mime="image/png")           
                    plt.close(fig)
         else:
             st.sidebar.markdown("There are many plots Choose according to your requirments And view data in different charts")
        
    elif plot_mode == "🗂️ FacetGrid":
        st.sidebar.subheader(" 🗂️ FacetGrid (create subplot)")

        session_state['current_plot'] = 'facetgrid'  # Track current plot type
    
        # 1. Plot type selection
        kind = st.sidebar.selectbox("Type of plot:",seaborn_compatible_plots,key="gr_kind")
        if kind is not None:
             
            # 2. Conditional axis inputs
            if kind in ["kdeplot", "histplot"]:
                x = st.sidebar.selectbox("Select column for x-axis:",numberic_cols,key="gr_x")
            elif kind == "countplot":
                x = st.sidebar.selectbox("Select column for x-axis:",categorical_cols,key="gr_x2")
            else:
                x = st.sidebar.selectbox("Select column for x-axis:",categorical_cols,key="gr_x2")
                y = st.sidebar.selectbox("Select column for y-axis:",numberic_cols,key="gr_y")
            
            # 3. Grouping options (keep existing)
            col = st.sidebar.selectbox("🧱 Subplot by column", categ, key="gr_col")
            col = None if col == "No Any" else col
            row = st.sidebar.selectbox("🧱 Subplot by row", categ, key="gr_row") 
            row = None if row == "No Any" else row
            hue = st.sidebar.selectbox("🎨 Hue", categ, key="gr_hue")
            hue = None if hue == "No Any" else hue
            color = st.sidebar.selectbox("🎨 Choose color palette", palette_options,key="gr_color")

            col1, col2 = st.sidebar.columns([1, 1])
            plot_triggered=False

            with col1:
                if st.button("Generate Plot", key="grid"):
                    plot_triggered=True
                
            with col2:
                if st.button("Clear",on_click=reset_inputs):
                    pass
            if plot_triggered:
                    st.subheader("Data Visualization",divider=True)
                    st.markdown(f"### 📊 {kind.title()}")
                    if row or col :
                        if hue:
                            g = sns.FacetGrid(data=df, col=col, row=row, hue=hue, height=3,aspect=1.4, palette=color)
                        else:
                            g = sns.FacetGrid(data=df, col=col, row=row, hue=hue, height=3,aspect=1.5, palette=color)
                    else:
                        g = sns.FacetGrid(data=df, col=col, row=row, hue=hue, height=4,aspect=1.7, palette=color)


                    plot_func = getattr(sns, kind)
                    if kind in ["countplot", "histplot", "kdeplot"]:
                        g.map_dataframe(plot_func, x=x)
                    else:
                        g.map_dataframe(plot_func, x=x, y=y)
                    g.add_legend()        
                    plt.tight_layout(pad=1)
                    # st.pyplot(g.figure)
                    fig = g.figure  # <— the matplotlib Figure
                    st.pyplot(fig)

                    st.download_button(
                        label="⬇️ Download chart",
                        data=fig_to_bytes(fig, fmt="png", dpi=300),
                        file_name=f"{kind.lower()}_facetgrid.png",
                        mime="image/png",
                    )
                    plt.close(fig)
        else:
            st.sidebar.markdown("There is many plots Choose according to your requirments And view data in different styles")
st.markdown("""
    <div class="custom-footer">
        📊 Developed with ❤️ by <b>Fakhur Ali 23-bsIT-29</b> | 📅 2025 | 🌐 <a href='https://yourportfolio.com' target='_blank'>Portfolio</a>
    </div>
""", unsafe_allow_html=True)
