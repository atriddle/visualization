import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def convert_to_float(x):
    try:
        return float(x) if isinstance(x, str) else x
    except ValueError:
        return x


# 获取当前文件夹路径
current_folder = os.getcwd()
current_measures = ["rmse", "spearman", "pearson", "ci", "r_square_score", "MedAE"]
folders = [folder for folder in os.listdir(current_folder) if os.path.isdir(os.path.join(current_folder, folder))]
output_path1 = os.path.join(current_folder, "1output")
for i in range(4):
    first_folder = folders[i+3]
    first_folder_path = os.path.join(current_folder, first_folder)
    models = [folder for folder in os.listdir(first_folder_path) \
                 if os.path.isdir(os.path.join(first_folder_path, folder))]
    output_dirs = os.listdir("./1output")
    output_path = os.path.join(output_path1, output_dirs[i])
    print(output_path)
    for current_measure in current_measures:
        new_df = pd.DataFrame()
        for model in models:
            model_path = os.path.join(first_folder_path, model)
            csv_file_path = os.path.join(model_path, "preds_reg.csv")
            df = pd.read_csv(csv_file_path)
            df = df.drop([1, 3, 5, 7])
            column_name = current_measure  # 获取第三列的列名
            wanted_column = pd.DataFrame(df[column_name])
            wanted_column = wanted_column.rename(columns={column_name: model})
            new_df = pd.concat([new_df, wanted_column], axis=1)
        new_df.reset_index(drop=True, inplace=True)

        # 假设 'data' 是您的DataFrame
        # 定义一个转换函数


        # 应用转换函数到第二行以后的数据
        new_df.iloc[0:] = new_df.iloc[0:].applymap(convert_to_float)
        print(new_df)
        # Define the number of points per feature, which should be the number of rows in the data
        num_points = new_df.shape[0]
        num_features = new_df.shape[1]
        # Set up the plot again
        fig, ax = plt.subplots(figsize=(8.5, 6))
        features = new_df.columns
        color_code = ['#f8766d', '#c49a00', '#53b400', '#00c094', '#00b6eb', '#a58aff', '#fb61d7']
        shape_code = ['h', 'o', 's', 'D', 'p', 'v', '^']
        for i, feature in enumerate(features):
            # 计算每个散点的位置
            positions = np.linspace(0.8*i - 0.2, 0.8*i + 0.2, num_points)
            # 绘制散点
            ax.scatter(positions, new_df[feature], label=f'{feature} new_df', color=color_code[i], marker=shape_code[i])
            # 计算平均值和标准误差
            mean_value = new_df[feature].mean()
            std_deviation = new_df[feature].std()
            errors = std_deviation / np.sqrt(num_points)  # 计算标准误差

            # 绘制平均值线和误差线
            ax.hlines(mean_value, 0.8*i - 0.2, 0.8*i + 0.2, color='black', linewidth=0.8, label=f'{feature} mean' if i == 0 else "")
            ax.errorbar(0.8*i, mean_value, yerr=errors, fmt='', color='black', ecolor='black', capsize=5)

        # 设置图形属性
        tick_positions = [i*0.8 for i in range(num_features)]  # 使用指数增长的位置
        ax.set_xticks(tick_positions)
        ax.set_xticklabels(features)
        ax.set_xlabel('Models')
        ax.set_title(current_measure)  # 请替换为适合您数据的标题

        # 添加图例
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())
        file_name = current_measure + first_folder + ".svg"
        final_file_path = os.path.join(output_path, file_name)
        plt.savefig(final_file_path, format='svg')

