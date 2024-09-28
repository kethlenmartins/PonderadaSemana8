import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
lower_limit = df['value'].quantile(0.025)
upper_limit = df['value'].quantile(0.975)
df = df[(df['value'] >= lower_limit) & (df['value'] <= upper_limit)]

def draw_line_plot():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df.index, df['value'], color='red')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar_plot = df.copy()
    df_bar_plot['year'] = df_bar_plot.index.year
    df_bar_plot['month'] = df_bar_plot.index.month
    df_bar_plot_bar = df_bar_plot.groupby(['year', 'month'])['value'].mean().unstack()

    fig, ax = plt.subplots(figsize=(10, 6))
    df_bar_plot_bar.plot(kind='bar', ax=ax)

    ax.set_title('Average Daily Page Views per Month')
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title='Months', labels=[
        'January', 'February', 'March', 'April', 'May', 'June', 
        'July', 'August', 'September', 'October', 'November', 'December'])
    
    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box['date']]
    df_box['month'] = [d.strftime('%b') for d in df_box['date']]
    df_box['month_num'] = df_box['date'].dt.month 
    df_box = df_box.sort_values('month_num') 

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    sns.boxplot(x='year', y='value', data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(x='month', y='value', data=df_box, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
