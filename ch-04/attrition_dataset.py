import pandas as pd
import numpy as np

import torch
from torch.utils.data import Dataset

# for oversampling the minority class
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import LabelEncoder

# the class to wrap the dataset in a Torch Dataset

# compared to example in chap. 2 this class has been modified incorporatinhg oversampling
DEBUG = False

class AttritionDataset(Dataset):
    """Oracle Attrition dataset."""

    # categoricals cols are identified dynamically
    # the rule used: each cols with < 10 distinct values
    def identify_categoricals(self):
        # theshol to identify categoricals cols
        THR = 10

        nunique = self.df.nunique()
        types = self.df.dtypes

        self.categorical_columns = []

        for col in self.df.columns:
            # identifichiamo come categoriche tutte le colonne che soddisfano questa condizione
            # la soglia THR la possiamo cambiare
            if types[col] == "object" or nunique[col] < THR:
                if DEBUG:
                    print(f"{col} distinct values: {self.df[col].nunique()}")

                self.categorical_columns.append(col)

    def codify_categoricals(self):
        for col in self.categorical_columns:
            # codifichiamo i categorici con LabelEncoder
            l_enc = LabelEncoder()
            self.df[col] = l_enc.fit_transform(self.df[col].values)

    """
    In __init__ we encapsulate the logic for loading the data from csv
    remove unneeded cols
    identify categoricals
    codify as integer, using LabelEncoder categoricals
    """

    def __init__(self, csv_file, over_sample=False):
        """Initializes instance of class AttritionDataset.

        Args:
            csv_file (str): Path to the csv file with the data.

        """
        # here we read the entire csv
        self.df = pd.read_csv(csv_file)

        # cols not to be used
        self.cols_to_drop = [
            "Directs",
            "name",
            "Over18",
            "WeeklyWorkedHours",
            "EmployeeNumber",
        ]

        self.target = "Attrition"

        # dropping cols not to be used
        self.df = self.df.drop(columns=self.cols_to_drop)

        # label encoding of categoricals
        self.identify_categoricals()
        self.codify_categoricals()

        # the ds is unbalanced, improve with oversampling
        X = self.df.drop(self.target, axis=1).values
        y = self.df[self.target].values
        
        if over_sample:
            oversampler = RandomOverSampler(sampling_strategy='minority')
            X, y = oversampler.fit_resample(X, y)
        
        # Save features and target as tensors
        # the type must be float, not Long
        self.X = torch.from_numpy(X).to(dtype=torch.float32)
        self.y = torch.from_numpy(y).to(dtype=torch.float32)

    """
    A PyTorch Dataset has two fundamentals methods
    __len__ which must return the number of records in the dataset
    __get_item must return item of index idx as a Tensor
    """

    def __len__(self):
        return self.X.shape[0]

    def __getitem__(self, idx):

        return (self.X[idx], self.y[idx])