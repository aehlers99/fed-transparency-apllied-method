import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

data = pd.read_csv('dataMotivacao.csv', sep = ';')
data = data.replace("0 = No.", 0.)
data = data.astype(str).astype(float)

score = data.sum(axis=0).drop("Unnamed: 0")

scoreIndex = score.index

scoreIndex_clean = []


for index in scoreIndex:
    scoreIndex_clean.append(index.replace("PDFs/monetary", "").replace("a1.pdf", ""))


year = scoreIndex_clean.str[0:4]
month = scoreIndex_clean.str[4:6]
scoreIndex_clean = pd.Series(scoreIndex_clean)
day = scoreIndex_clean.str[6:8]

scoreIndex_label = year + "-" + month + "-" + day

df_score = pd.DataFrame({"date": scoreIndex_label.values, "score": score.values})
df_score = df_score.sort_values(by = "date")

plot = sns.barplot(x = "date", y = "score", data = df_score)
plot.set_xticklabels(plot.get_xticklabels(), rotation=90)
plt.show()

#def animate(i):
#    data = df_score.iloc[:int(i+1)]
#    graph = sns.barplot(x = 'data', y = 'score', data = df_score)
#
#ani = plt.animation.FuncAnimation(fig, animate, frames = (len(df_score)), interval = 700, blit = False, repeat = True)


