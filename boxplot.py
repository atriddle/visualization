import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd


df = pd.read_csv('anova.csv')


tukey_results = pairwise_tukeyhsd(endog=df.melt(value_name='values')['values'],
                                  groups=df.melt(value_name='values')['variable'],
                                  alpha=0.05)

# Get summary as a DataFrame
tukey_summary_df = pd.DataFrame(data=tukey_results.summary().data[1:], columns=tukey_results.summary().data[0])

# Filter significant results
significant_results = tukey_summary_df[tukey_summary_df['reject'] == True]
print(significant_results)

plt.figure(figsize=(12, 8))
ax = sns.boxplot(data=df)
plt.title('Boxplot with Detailed Significance Markings')
plt.ylabel('Values')
plt.grid(True)


def star_significance(p_value):
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return ''


# Add significance annotations with detailed stars
layer_adjust = 2  # Height adjustment for layered significance

for index, row in significant_results.iterrows():
    group1, group2 = int(row['group1'][-1]) - 1, int(row['group2'][-1]) - 1
    stars = star_significance(row['p-adj'])
    max_y = max(df.max()[group1], df.max()[group2])
    y = max_y + 0.5 + (layer_adjust * list(significant_results.index).index(index))
    plt.plot([group1, group1, group2, group2], [y, y + 0.2, y + 0.2, y], lw=1.5, c='k')
    plt.text((group1 + group2) / 2, y + 0.2, stars, ha='center', va='bottom', color='k')

plt.savefig('boxplot.svg')
plt.show()