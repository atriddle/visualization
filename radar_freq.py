import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# df = pd.read_csv('AA_radic_Demo.csv')  # 将'your_file.csv'替换为你的文件名
# first_40 = df['sequence'].head(40)
# result = ''.join(first_40)
df = pd.read_csv('AA_radic_Demo_two seq.csv')
sequence1 = df['sequence1']
sequence2 = df['sequence2'].dropna()
result = ''.join(sequence1)
result1 = ''.join(sequence2)
# clustalXAAColors = {
#     #    Hydrophobic (Blue)
#     "A": "#809df0",
#     "I": "#809df0",
#     "L": "#809df0",
#     "M": "#809df0",
#     "F": "#809df0",
#     "W": "#809df0",
#     "V": "#809df0",
#     #    Positive charge (Red)
#     "K": "#ed000a",
#     "R": "#ed000a",
#     #    Negative charge (Magenta)
#     "D": "#be38bf",
#     "E": "#be38bf",
#     #    Polar (Green)
#     "N": "#29c417",
#     "Q": "#29c417",
#     "S": "#29c417",
#     "T": "#29c417",
#     #    Cysteins (Pink)
#     "C": "#ee7d80",
#     #    Glycines (Orange)
#     "G": "#ef8f48",
#     #    Prolines (Yellow)
#     "P": "#c1c204",
#     #    Aromatics (Cyan)
#     "H": "#23a6a4",
#     "Y": "#23a6a4",
#     #    STOP
#     "_": "#FF0000",
#     "*": "#AAAAAA",
# }
# letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y','Z', 'U', 'B', 'X']
letters = ['A', 'I', 'L', 'M', 'F', 'V', 'W', 'K', 'R', 'D', 'E', 'N', 'Q', 'S', 'T', 'C', 'G', 'P', 'H', 'Y']
counts = {letter: result.count(letter) for letter in letters}
counts1 = {letter: result1.count(letter) for letter in letters}
colors = ["#809df0", "#809df0", "#809df0","#809df0","#809df0","#809df0", "#809df0", "#ed000a", "#ed000a", \
          '#be38bf', '#be38bf', '#29c417', '#29c417', '#29c417', '#29c417', '#ee7d80', '#ef8f48', '#c1c204', \
          '#23a6a4', '#23a6a4']
dot_colors = ["#738dd8", "#738dd8", "#738dd8","#738dd8","#738dd8","#738dd8", "#738dd8", "#d50009", "#d50009", \
          '#ab32ac', '#ab32ac', '#25b015', '#25b015', '#25b015', '#25b015', '#d67173', '#d78141', '#aeaf04', \
          '#209594', '#209594']
df = pd.DataFrame(list(counts.values()), index=letters, columns=['Count'])
df1 = pd.DataFrame(list(counts1.values()), index=letters, columns=['Count'])

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.set_rlabel_position(-37)
# 数据
angles = np.linspace(0, 2 * np.pi, len(df)+2, endpoint=False).tolist()
del angles[20:22]
stats = df['Count'].tolist()
stats1 = df1['Count'].tolist()
sum_0 = sum(stats)
sum_1 = sum(stats1)
freq = [x / sum_0 for x in stats]
freq1 = [x / sum_0 for x in stats1]
print(freq)
print(freq1)
# 留出中心空白的设置
inner_radius = 0.05  # 内半径大小，根据需要调整

# 绘制条形图
bars = ax.bar(angles, freq, color=colors, width=0.24, alpha=0.6, bottom=inner_radius)

ax.set_xticks([])  # 隐藏角度刻度

# 在每个柱上方标注对应的字母
for bar, label, angle in zip(bars, df.index, angles):
    rotation = np.degrees(angle)
    alignment = 'center'
    if bar.get_height() + inner_radius > 0.001:  # 判断高度，以便调整标签位置
        ax.text(angle, 0.25, label,
                rotation=rotation, ha=alignment, va='center', color='black', fontsize=9)

# 在每个柱的顶端添加点并连接这些点
tops = [bar.get_height() + inner_radius for bar in bars]
tops1 = [x + 0.05 for x in freq1]

for angle, top, color in zip(angles, tops, dot_colors):
    ax.plot(angle, top, 'o', color=color, alpha=0.8, markersize=4)
for angle, top, color in zip(angles, tops1, dot_colors):
    ax.plot(angle, top, 'o', color=color, alpha=0.8, markersize=2.7)

ax.plot(angles, tops, 'k-', alpha=0.8, lw=1.8)
# 'k-' 表示黑色('k')线('-')
ax.plot(angles, tops1, 'k-', alpha=0.4, lw=0.9)


# 调整Y轴刻度标签，避免显示负数
current_ticks = ax.get_yticks()
print(current_ticks)
current_ticks = [x + 0.025 for x in current_ticks]
new_ticks = [max(0, x - 0.05) for x in current_ticks]

ax.set_yticks(current_ticks)  # 使用原始的刻度位置
ax.set_yticklabels([f"{x:.3f}" for x in new_ticks])  # 使用调整后的刻度标签


# 设置Y轴的上限，确保柱形图显示完整
ax.set_ylim(0, max(freq) + inner_radius + 0.025)
plt.savefig('sample_freq.svg')
plt.show()