import pandas as pd

def read_data(data_file_name):
    """ Read data file (i.e., excel/csv)

        Args:
            data_file_name: str
                Name of the file to be loaded

        Returns: 
            : pandas.DataFrame
                Contents of the excel file loaded into a DataFrame 
    """

    data_root_path="../Data/"
    return pd.read_excel(data_root_path+data_file_name, engine='openpyxl')

def remove_columns(df, columns_list):
    """ Removed specified columns from a DataFrame

        Args:
            df: DataFrame
                DataFrame which contains the data
            columns_list: list
                List of column names which are needed to be removed
                
        Returns: 
            df: pandas.DataFrame
                Contents of the DataFrame after removing the specified columns 
    """
    
    for each_column in columns_list:
        try:
            del df[each_column]
        except:
            print("Warning: given column ", each_column, " does not exist!")
    return df