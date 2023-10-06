import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def writeDFToFilepathAsCSV(array, columns, filepath, sortVal=-1):
    df = pd.DataFrame(data=np.array(array), columns=columns)
    if sortVal > 0:
        df = df.sort_values(by=[columns[1]], axis=0, ascending=False)
    df.to_csv(filepath, index=False)

def plotResults(x,y):
    plt.figure(figsize=(10, 6))
    plt.scatter(x, y, alpha=0.3)
    plt.title('Input Float Value vs. Breakeven Price')
    plt.xlabel('Input Float Value')
    plt.ylabel('$ Value (Before Steam 13% Tax)')
    plt.xlim(0, 1)
    plt.show()

def readCSVFileToDataframe(fileDirectory):
    df = pd.read_csv(fileDirectory)
    return df