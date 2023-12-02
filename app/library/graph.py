import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import json
from io import StringIO


class Graph:
    def __init__(self, json_data: dict, file_name):
        self.data = json_data
        self.df1 = None
        self.df2 = None
        self.file_name = file_name
        self.create_table()

    def create_table(self):
        self.df1 = pd.read_json(StringIO(json.dumps(self.data["query1"])))
        self.df2 = pd.read_json(StringIO(json.dumps(self.data["query2"])))
        self.modify_table()

    def modify_table(self):
        # split to columns
        self.df1[['Time', 'Query', 'Data']] = self.df1[0].str.split('|', expand=True)
        self.df1.drop(columns=[0], inplace=True)
        self.df2[['Time', 'Query', 'Data']] = self.df2[0].str.split('|', expand=True)
        self.df2.drop(columns=[0], inplace=True)

        self.df1['Query + Data'] = self.df1['Query'] + "\n" + self.df1['Data'].str.replace("}, {", '},\n{')
        self.df2['Query + Data'] = self.df2['Query'] + "\n" + self.df2['Data'].str.replace("}, {", '},\n{')

        for index, row in self.df1.iterrows():
            self.df1['Query + Data'][index] = str(index + 1) + ". " + self.df1['Query + Data'][index]

        for index, row in self.df2.iterrows():
            self.df2['Query + Data'][index] = str(index + 1) + ". " + self.df2['Query + Data'][index]

        # set float type
        self.df1['Time'] = self.df1['Time'].astype(float)
        self.df2['Time'] = self.df2['Time'].astype(float)

        # add delta times
        self.df1['Timedelta'] = self.df1['Time'].diff()
        self.df2['Timedelta'] = self.df2['Time'].diff()

        self.create_graph()

    def create_graph(self):
        sns.set_theme(style="whitegrid")
        self.create_plot([self.df1, self.df2], ['Blue', 'Green'])
        plt.tight_layout()
        plt.savefig("static/images/" + self.file_name)

    def create_plot(self, array_of_df, pallette):
        fig, axes = plt.subplots(2, 1, sharex=True, figsize=(10, 6))
        for i, df in enumerate(array_of_df):
            ax = sns.lineplot(data=df, x='Time', y='Query + Data', marker='o', color=pallette[i], ax=axes[i])
            """if index >= 2:
                for i, value in enumerate(df['Date']):
                    ax.axvline(x=value, color=pallette[index], linestyle='--')"""
            for index, row in df.iterrows():
                if 'Previous query' in df['Query'][index]:
                    plt.plot([df.loc[index - 1, 'Time'], df.loc[index, 'Time']], [index - 1, index], color='red',
                             linestyle='-', linewidth=2)
                axes[0].axvline(x=df['Time'][index], color='grey', linestyle='--')
                axes[1].axvline(x=df['Time'][index], color='grey', linestyle='--')






