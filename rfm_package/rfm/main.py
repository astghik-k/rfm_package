"""Main module."""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import squarify
import warnings
warnings.filterwarnings("ignore")
pd.set_option('display.max_columns', None)


def create_rfm_columns(data, id, dates, revenue):
    """
    Calculates recency, frequency and monetary values
    for each person based on purchase date and revenue,
    Adds Recency, Frequency, Monetary columns to dataset

    Parameters
    ----------
    data : object
        Input dataset

    id : object
        Input customer ids

    dates : datetime64[ns]
        Input dates with YY/MM/DD date format

    revenue :int64


    Returns
    -------
    df : object
        Dataframe with 4 columns: id, Recency, Frequency, Monetary

    """
    max_date = data[dates].max()
    df = data.groupby(id).agg(
        {dates: lambda date: (max_date - date.max()).days,
                               id: lambda num: len(num),
                               revenue: lambda price: price.sum()})
    df.columns = ['Recency', 'Frequency', 'Monetary']
    df.reset_index(inplace = True)
    return df


def scale_rfm_columns(data):
    """
    Encodes Recency column from 1-4 (4 is the most recent)
    Encodes Frequency column 4-1 (4 is the more frequent)
    Encodes Monetary column 4-1 (4 is the most money)
    Parameters
    ----------
    data : object
        Dataframe with 4 columns: id, Recency, Frequency, Monetary

    Returns
    -------
    data: object
        Dataframe with 7 columns: id, Recency, Frequency, Monetary, R, F, M


    """
    data['R'] = pd.qcut(data['Recency'], 4, ['1', '2', '3', '4'])
    data['F'] = pd.qcut(data['Frequency'], 4, ['4', '3', '2', '1'])
    data['M'] = pd.qcut(data['Monetary'], 4, ['4', '3', '2', '1'])
    return data


def plot_rfm(data):
    """
    Plots density histograms for Recency, Frequency and Monetary columns

    Parameters
    ----------
    data : object
        Dataframe with 7 columns: id, Recency, Frequency, Monetary, R, F, M

    Returns
    -------
    plot
        3 density histograms for Recency, Frequency, Monetary columns in one graph

    """
    plt.figure(figsize=(12,10))
    plt.subplot(3, 1, 1); sns.distplot(data['Recency'])
    plt.subplot(3, 1, 2); sns.distplot(data['Frequency'])
    plt.subplot(3, 1, 3); sns.distplot(data['Monetary'])
    plt.tight_layout()
    plt.show()


def rfm_scores(data):
    """
    Sums R, F, M scores for each person saves in RFM Score column
    Converting R,F,M Scores to string, concatenates them, and saves in RFM Segments column

    Parameters
    ----------
    data : object
        Dataframe with 7 columns: id, Recency, Frequency, Monetary, R, F, M



    Returns
    -------
    data: object
        Dataframe with 7 columns: id, Recency, Frequency, Monetary, R, F, M. RFM_Score, RFM_Segment


    """
    data['RFM_Score'] = data.R.astype(int) +data.F.astype(int) + data.M.astype(int)
    data['RFM_Segment'] = data.R.astype(str) + data.F.astype(str) + data.M.astype(str)
    data = data.sort_values('RFM_Segment', ascending=False)
    return data


def top_customers(data):
    """
    Sorts RFM Segment column in descending order

    Parameters
    ----------
    data : object


    Returns
    -------
    data: object
        Dataframe with 7 columns: id, Recency, Frequency, Monetary, R, F, M. RFM_Score, RFM_Segment(sorted order)

    """
    data = data.sort_values('RFM_Segment', ascending=False)
    return data


def naming(df):
    """
    Names each RFM Score value

    Parameters
    ----------
    df : object


    Returns
    -------
    str

    """
    if df['RFM_Score'] >= 9:
            return 'Can\'t Loose Them'
    elif ((df['RFM_Score'] >= 8) and (df['RFM_Score'] < 9)):
        return 'Champions'
    elif ((df['RFM_Score'] >= 7) and (df['RFM_Score'] < 8)):
        return 'Loyal/Commited'
    elif ((df['RFM_Score'] >= 6) and (df['RFM_Score'] < 7)):
        return 'Potential'
    elif ((df['RFM_Score'] >= 5) and (df['RFM_Score'] < 6)):
        return 'Promising'
    elif ((df['RFM_Score'] >= 4) and (df['RFM_Score'] < 5)):
        return 'Requires Attention'
    else:
        return 'Demands Activation'

def give_names_to_segments(data):
    """
    Applies naming() to Segment Name column

    Parameters
    ----------
    data : object


    Returns
    -------
    data: object
        Dataframe with 8 columns: id, Recency, Frequency, Monetary, R, F, M. RFM_Score, RFM_Segment, Segment_Name


    """
    data['Segment_Name'] = data.apply(naming, axis=1)
    return data


def segments_distribution(data):
    """
    Calculates means for Recency, Frequency and Monetary columns and counts for each segment name

    Parameters
    ----------
    data : object


    Returns
    -------
    df : object
        DataFrame with 5 columns Segment_Name, Recency mean, Frequency Mean, Monetary Mean, Monetary count


    """
    df = data.groupby('Segment_Name').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']}).round(1)

    return df


def visualize_segments(data):
    """
    Plots a squrify graph for each segment depending on their count and Recency mean, Frequency mean, Monetary mean

    Parameters
    ----------
    data : object
        DataFrame with 5 columns Segment_Name, Recency mean, Frequency Mean, Monetary Mean, Monetary count



    Returns
    -------
    plot
        Squarify graph for all segment distributions

    """
    data.columns = ['RecencyMean','FrequencyMean','MonetaryMean', 'Count']
    fig = plt.gcf()
    ax = fig.add_subplot()
    squarify.plot(sizes=data['Count'],
    label=['Can\'t Loose Them',
    'Champions',
    'Loyal/Commited',
    'Requires Attention',
    'Potential',
    'Promising',
    'Demands Activation'], color=sns.color_palette("Spectral",
                                     len(data)))
    plt.title("RFM Segments",fontsize=18,fontweight="bold")
    plt.axis('off')
    plt.show()
