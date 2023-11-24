import pandas as pd
import streamlit as st
import io


fileName ='empty'

fileName = st.file_uploader("Browse for or drag and drop the name of your Neighbourwoods INPUT excel workbook", 
    type = ['xlsm', 'xlsx', 'csv'], 
    key ='fileNameKey')


def getData(fileName):

    if fileName is not None:

        df_trees = pd.DataFrame()

        try:
            df_trees = pd.read_excel(fileName, sheet_name = "summary", header = 0)
        
        except ValueError:
            st.write("Oops, are you sure your file is a Neighbourwoods SUMMARY file with a worksheet called 'summary'?")

        return df_trees
    
df_trees = getData(fileName)

st.dataframe(df_trees)



# # create two dataframes
# df1 = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
# df2 = pd.DataFrame({'C': [7, 8, 9], 'D': [10, 11, 12]})


# # create a buffer to hold the data
# buffer = io.BytesIO()

# # create a Pandas Excel writer using the buffer
# writer = pd.ExcelWriter(buffer, engine='xlsxwriter')

# # write the dataframes to separate sheets in the workbook
# df1.to_excel(writer, sheet_name='Sheet1', index=False)
# df2.to_excel(writer, sheet_name='Sheet2', index=False)

# # save the workbook to the buffer
# # writer.save()
# writer.close()


# # reset the buffer position to the beginning
# buffer.seek(0)

# # create a download link for the workbook
# st.download_button(
#     label='Download Data',
#     data=buffer,
#     file_name='ddownloaded data.xlsx',
#     mime='application/vnd.ms-excel')