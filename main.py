import random

import pandas as pd
import pyreadr
from tqdm import tqdm
from src.household import Household


def get_synth_hh():
    df = pyreadr.read_r('data/household_synth.rds')[None]
    df.rename(columns={'imputed_newest_const_dates': 'imputed_newest_const_date'}, inplace=True)
    return df


def describe_synth_hh():
    print(get_synth_hh().describe().to_string())


def gen_synth_hh_flex_scenarios():
    flex_scenarios = []
    df = get_synth_hh()
    for index, row in tqdm(df.iterrows(), total=len(df)):
        hh = Household().setup(row.to_dict())
        hh.map_flex_scenario()
        flex_scenarios.append(hh.gen_flex_scenario())
    pd.DataFrame(flex_scenarios).to_csv('data/flex_scenarios.csv', index=False)


if __name__ == "__main__":
    # describe_synth_hh()
    gen_synth_hh_flex_scenarios()
