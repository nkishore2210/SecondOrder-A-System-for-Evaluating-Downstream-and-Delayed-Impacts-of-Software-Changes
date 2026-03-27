import pandas as pd

def load_and_preprocess(file_path):
    df = pd.read_csv(file_path)

    version_A = df[df['version'] == 'A']
    version_B = df[df['version'] == 'B']

    summary_stats = {
        "version_A": version_A.describe(),
        "version_B": version_B.describe()
    }

    return version_A, version_B, summary_stats