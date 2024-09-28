import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
bmi = df['weight'] / (df['height'] / 100) ** 2
df['overweight'] = np.where(bmi > 25, 1, 0)

# 3
# Normalize the data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, make the value 0. If the value is more than 1, make the value 1.

df['cholesterol'] = np.where(df['cholesterol'] > 1, 1, 0)
df['gluc'] = np.where(df['gluc'] > 1, 1, 0)
# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    # 6
    df_cat = df_cat.rename(columns={'variable': 'feature', 'value': 'value'})
    df_cat['total'] = 1
    df_cat = df_cat.groupby(['cardio', 'feature', 'value'], as_index=False).count()

    # Set the order of the features
    feature_order = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    
    # 7 and 8
    cat_plot = sns.catplot(x='feature', y='total', hue='value', col='cardio', data=df_cat, kind='bar', order=feature_order)
    fig = cat_plot.figure

    # Access axes for each cardio value and set labels
    for ax in cat_plot.axes.flat:
        ax.set_xlabel("variable")
        ax.set_ylabel("total")

        # Set tick labels for the x-axis
        ax.set_xticks(range(len(feature_order)))  # Set appropriate range
        ax.set_xticklabels(feature_order)

    # 9
    fig.savefig('catplot.png')
    return fig




# 10
def draw_heat_map():
    # 11
    df_heat = df.copy()
    
    height_2_5th = df['height'].quantile(0.025)
    height_97_5th = df['height'].quantile(0.975)
    weight_2_5th = df['weight'].quantile(0.025)
    weight_97_5th = df['weight'].quantile(0.975)

    # Filter the DataFrame to exclude incorrect data
    df_heat = df_heat[
        (df_heat['height'] >= height_2_5th) & (df_heat['height'] <= height_97_5th) &
        (df_heat['weight'] >= weight_2_5th) & (df_heat['weight'] <= weight_97_5th) & (df_heat['ap_lo'] <= df_heat['ap_hi'])
    ]
    # 12
    corr = df_heat.corr()

    # 13
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize=(12, 8))

    # 15
    sns.heatmap(corr, mask=mask, cmap='coolwarm', annot=True, fmt=".1f", 
                square=True, linewidths=.5, cbar_kws={"shrink": .8}, ax=ax)
    ax.set_title('Correlation Heatmap', fontsize=18)

    # 16
    fig.savefig('heatmap.png')
    return fig