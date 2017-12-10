
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from scipy import stats, integrate
import seaborn as sn
import pandas as pd
from pylab import savefig

titanic = sns.load_dataset('titanic')
df = titanic.pivot_table(index='embark_town', columns='age_group', values='fare', aggfunc=np.median)
sns.heatmap(titanic.corr(), annot=True, fmt=".2f")
