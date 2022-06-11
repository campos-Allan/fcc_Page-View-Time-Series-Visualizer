"""forth challenge from 'Data Analysis with Python Projects'
on FreeCodeCamp.org
"""

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.DataFrame(pd.read_csv('fcc-forum-pageviews.csv', index_col='date'))
# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) &
        (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20, 10))
    df.plot(ax=ax)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.reset_index()
    df_bar['date'] = pd.to_datetime(df_bar['date'], format='%Y-%m-%d')
    df_bar['Months'] = df_bar['date'].dt.month_name()
    df_bar['Years'] = df_bar['date'].dt.year
    df_bar.drop(['date'], axis=1, inplace=True)

    df_bar = df_bar.groupby([df_bar['Years'], df_bar['Months']], sort=False)[
        'value'].mean().round().astype(int)
    df_bar = df_bar.reset_index()
    df_bar = df_bar.rename(columns={'value': 'Average Page Views'})
    missing_months = {
        'Years': [2016, 2016, 2016, 2016],
        'Months': ['January', 'February', 'March', 'April'],
        'Average Page Views': [0, 0, 0, 0]
    }
    df_bar = pd.concat([pd.DataFrame(missing_months), df_bar])
    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_title(
        'Daily freeCodeCamp Forum Average Page Views per Month', fontsize=15)
    plotting = sns.barplot(data=df_bar, x='Years',
                           y='Average Page Views', hue='Months', palette='tab10')
    plotting.set_xticklabels(plotting.get_xticklabels(),
                             rotation=90, fontsize=12)
    plotting.set_xlabel('Years', fontsize=20)
    plotting.set_ylabel('Average Page Views', fontsize=20)
    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'], format='%Y-%m-%d')
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box = df_box.rename(
        columns={'value': 'Page Views', 'year': 'Year', 'month': 'Month'})
    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(20, 10))
    sns.boxplot(ax=ax[0], x='Year', y='Page Views', data=df_box)
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year", fontsize=15)
    ax[0].set_ylabel("Page Views", fontsize=15)
    sns.boxplot(ax=ax[1], x='Month', y='Page Views', data=df_box, order=[
                "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month", fontsize=15)
    ax[1].set_ylabel("Page Views", fontsize=15)

    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
