# import streamlit as st
# import pandas as pd
# import os
# from io import BytesIO


# # Set up our App
# st.set_page_config(page_title="💽Data Sweeper", layout='wide')

# # Display the main app title and introductory text
# st.title("💽Advanced Data Sweeper")  
# st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")


# # File uploader widget that accepts CSV and Excel files
# uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# if uploaded_files:
#     for file in uploaded_files:
#         file_extension = os.path.splitext(file.name)[-1].lower()

#         if file_extension == ".csv":
#             df = pd.read_csv(file)
#         elif file_extension == ".xlsx":
#             df = pd.read_excel(file)
#         else:
#             st.error(f"Unsupported file type: {file_extension}")
#             continue

#         #Display info about the file
#         st.write(f"**📄 File Name:** {file.name}")
#         st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")
        
#         #Show 5 rows of our df
#         st.write("🔍 Preview of the Uploaded File:")
#         st.dataframe(df.head())

#         # Data cleaning options
#         st.subheader("🛠️ Data Cleaning Options")
#         if st.checkbox(f"Clean Data for {file.name}"):
#             col1, col2 = st.columns(2)
#             with col1:
#                 if st.button(f"Remove Duplicates from {file.name}"):
#                     df.drop_duplicates(inplace=True)
#                     st.write("Duplicates Removed!")
#             with col2:
#                 if st.button(f"Fill Missing Values for {file.name}"):
#                     numeric_cols = df.select_dtypes(include=['number']).columns
#                     df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
#                     st.write("Missing Values have been Filled!")

#         #Choose Specific Columns to Keep or Convert
#         st.subheader("🎯 Select Columns to Convert")
#         columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
#         df = df[columns]

#         #Create Some Data Visualizations
#         st.subheader("📊 Data Visualization")
#         if st.checkbox(f"Show Visualization for {file.name}"):
#             st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

#         #Convert the File -> CSV to Excel
#         st.subheader("🔄 Conversion Options")
#         conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
#         if st.button(f"Convert {file.name}"):
#             buffer = BytesIO()
#             if conversion_type == "CSV":
#                 df.to_csv(buffer, index=False)
#                 file_name = file.name.replace(file_extension, ".csv")
#                 mime_type = "text/csv"
#             elif conversion_type == "Excel":
#                 df.to_excel(buffer, index=False, engine='openpyxl')
#                 file_name = file.name.replace(file_extension, ".xlsx")
#                 mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
#             buffer.seek(0)

#              # Download button
#             st.download_button(
#                 label=f"⬇️ Download {file.name} as {conversion_type}",
#                 data=buffer,
#                 file_name=file_name,
#                 mime=mime_type
#             )

# st.success("🎉 All files processed successfully!")



import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up App
st.set_page_config(page_title="💽 Data Sweeper", layout='wide')

# Dark Mode Toggle
dark_mode = st.toggle("🌙 Dark Mode")
if dark_mode:
    st.markdown(""" <style> body { background-color: #1e1e1e; color: white; } </style> """, unsafe_allow_html=True)

# Title
st.title("💽 Advanced Data Sweeper")  
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        file_size = file.size / 1024  # in KB
        
        if file_size > 5120:  # Limit to 5MB
            st.warning(f"⚠️ {file.name} is too large (>5MB). Consider compressing it.")
            continue
        
        # Read file
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue

        # Display file info
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file_size:.2f} KB")
        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        df_cleaned = df.copy()
        
        if st.checkbox(f"Apply Cleaning for {file.name}"):
            if st.button(f"Remove Duplicates - {file.name}"):
                df_cleaned.drop_duplicates(inplace=True)
                st.success("✅ Duplicates Removed!")
            
            if st.button(f"Fill Missing Values - {file.name}"):
                numeric_cols = df_cleaned.select_dtypes(include=['number']).columns
                df_cleaned[numeric_cols] = df_cleaned[numeric_cols].fillna(df_cleaned[numeric_cols].mean())
                st.success("✅ Missing Values Filled!")
            
            if st.button(f"Trim Text & Convert Case - {file.name}"):
                text_cols = df_cleaned.select_dtypes(include=['object']).columns
                for col in text_cols:
                    df_cleaned[col] = df_cleaned[col].str.strip().str.lower()
                st.success("✅ Text Trimmed & Lowercased!")

        # Column Selection
        st.subheader("🎯 Select Columns to Keep")
        columns = st.multiselect(f"Choose Columns for {file.name}", df_cleaned.columns, default=df_cleaned.columns)
        df_cleaned = df_cleaned[columns]
        
        # Visualization Options
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Charts for {file.name}"):
            chart_type = st.selectbox("Select Chart Type:", ["Bar Chart", "Line Chart", "Pie Chart"], key=file.name)
            if chart_type == "Bar Chart":
                st.bar_chart(df_cleaned.select_dtypes(include='number'))
            elif chart_type == "Line Chart":
                st.line_chart(df_cleaned.select_dtypes(include='number'))
            elif chart_type == "Pie Chart":
                st.write("📌 Pie charts require categorical data.")
                col = st.selectbox("Select Column for Pie Chart:", df_cleaned.columns)
                st.write(df_cleaned[col].value_counts().plot.pie(autopct="%.2f%%"))
                st.pyplot()
        
        # File Conversion
        st.subheader("🔄 Convert & Download")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"convert_{file.name}")
        if st.button(f"Convert & Download {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df_cleaned.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            else:
                df_cleaned.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"⬇️ Download {file_name}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
