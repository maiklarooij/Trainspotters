from audioop import reverse
from email import header
import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt

df = pd.read_csv('experiment_genetic_2.csv')
#print(df.groupby(['breeding', 'selection', 'generations', 'mutate_rate', 'gp_size']).agg(['mean', 'min', 'max', 'median']).sort_values([('score', 'max')], ascending=False).nlargest(5, ('score', 'max')))
print(tabulate(df.groupby(['breeding', 'selection', 'generations', 'mutate_rate', 'gp_size']).agg(['mean', 'min', 'max', 'median']).sort_values([('score', 'max')], ascending=False).nlargest(5, ('score', 'max'))['score'], headers = 'keys', tablefmt = 'pipe'))
