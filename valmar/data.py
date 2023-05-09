import pandas as pd
import numpy as np
from datetime import datetime


def convert_category_label(df: pd.DataFrame, label_col: str) -> pd.DataFrame:
    """
    Convert category label in to separate columns: sex and age.

    :param df : Pandas DataFrame with data.
    :param label_col : name of the DataFrame column with categories.
    :return: DataFrame with new columns.
    """

    # Inner function to evaluate the gender
    def extract_age(category):
        try:
            return int(category[-2:])
        except ValueError:
            return np.nan

    df['AGE'] = df[label_col].apply(extract_age)
    # Drop rows in AGE column with empty data
    df.dropna(subset=['AGE'], inplace=True)
    # Create and fill SEX column
    df['SEX'] = [participant[0] for participant in df[label_col]]
    return df


def times_conversion(df: pd.DataFrame, pace_label_col: str, time_label_col: [str]) -> pd.DataFrame:
    """
    Convert times into numeric representation as total number of seconds

    :param df: Pandas DataFrame with data
    :param pace_label_col: name of the DataFrame column with runner pace
    :param time_label_col: List with names of the DataFrame columns
    :return: DataFrame with times represented in numeric types
    """
    df[time_label_col[0]] = pd.to_timedelta(df[time_label_col[0]].astype(str)).dt.total_seconds()
    df[time_label_col[1]] = pd.to_timedelta(df[time_label_col[1]].astype(str)).dt.total_seconds()
    # Convert pace time into datetime time format
    df[pace_label_col] = df[pace_label_col].apply(lambda x: datetime.strptime(x, '%M,%S').time())
    df[pace_label_col] = pd.to_timedelta(df[pace_label_col].astype(str)).dt.total_seconds()
    return df


def invalid_data_in_column(df: pd.DataFrame, label_col: str, correct_type: type) -> pd.DataFrame:
    """
    Find invalid data which should be numeric and replace them with correct ones
    :param df: Pandas DataFrame with data
    :param label_col: name of the DataFrame column with invalid data
    :param correct_type: name of the correct data type
    :return: DataFrame with fixed data
    """
    df[label_col] = pd.to_numeric(df[label_col], errors='coerce')
    df.loc[df[label_col].isna(), label_col] = (df[df[label_col].isna()].index + 1).astype(int)
    df[label_col] = df[label_col].astype(correct_type)
    return df


def preprocess(df) -> pd.DataFrame:
    """
    Preprocess the data.
    :param df: Pandas DataFrame with original data
    :return: DataFrame with preprocessed data
    """
    df = invalid_data_in_column(df=df, label_col='OFFICIAL POS.', correct_type=int)
    df = times_conversion(df=df, pace_label_col='REAL AVERAGE', time_label_col=['OFFICIAL TIME', 'REAL TIME'])
    df = convert_category_label(df=df, label_col='CATEGORY')
    return df
