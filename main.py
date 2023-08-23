import pandas as pd
import pyreadr
from tqdm import tqdm
from src.household import Household


def get_synth_hh():
    df = pyreadr.read_r('input/household_synth.rds')[None]
    df.rename(columns={'imputed_newest_const_dates': 'imputed_newest_const_date'}, inplace=True)
    return df


def describe_synth_hh():
    df = get_synth_hh()
    print(df.columns)
    print(df.describe().to_string())


def map_synth_hh_flex_scenarios():
    flex_scenarios = []
    df = get_synth_hh()
    for index, row in tqdm(df.iterrows(), total=len(df)):
        hh = Household().setup(row.to_dict())
        hh.map_flex_scenario()
        flex_scenarios.append(hh.gen_flex_scenario())
    pd.DataFrame(flex_scenarios).to_csv('output/flex_scenario_mapping_updated.csv', index=False)


def calc_pv_benefit():
    synth_hh = pd.read_csv('output/flex_scenario_mapping_updated.csv')
    flex_scenarios = pd.read_excel('input/flex_scenarios/Scenarios.xlsx')
    flex_results = pd.read_excel('input/flex_scenarios/Result_RefScenarios.xlsx')
    flex_results.set_index('ID_Scenario', inplace=True)

    def find_flex_scenarios(row):
        df = flex_scenarios.loc[(flex_scenarios["ID_Building"] == row["ID_Building"]) &
                                (flex_scenarios["ID_Behavior"] == row["ID_Behavior"]) &
                                (flex_scenarios["ID_Boiler"] == row["ID_Boiler"]) &
                                (flex_scenarios["ID_HotWaterTank"] == row["ID_HotWaterTank"]) &
                                (flex_scenarios["ID_SpaceHeatingTank"] == row["ID_SpaceHeatingTank"]) &
                                (flex_scenarios["ID_Battery"] == row["ID_Battery"]) &
                                (flex_scenarios["ID_SpaceCoolingTechnology"] == row["ID_SpaceCoolingTechnology"])]
        scenario_ids = {}
        for _, scenario_row in df.iterrows():
            scenario_ids[scenario_row["ID_PV"]] = scenario_row["ID_Scenario"]
        return scenario_ids

    synth_hh_update = []
    for index, row in tqdm(synth_hh.iterrows(), total=len(synth_hh)):
        flex_scenario_ids = find_flex_scenarios(row)
        if len(flex_scenario_ids) > 0:
            d = row.to_dict()
            d["TotalCost_withPV"] = flex_results.iloc[flex_scenario_ids[1]]["TotalCost"]
            d["TotalCost_withoutPV"] = flex_results.iloc[flex_scenario_ids[2]]["TotalCost"]
            d["Grid2Load_withPV"] = flex_results.iloc[flex_scenario_ids[1]]["Grid2Load"]
            d["Grid2Load_withoutPV"] = flex_results.iloc[flex_scenario_ids[2]]["Grid2Load"]
            d["Feed2Grid_withPV"] = flex_results.iloc[flex_scenario_ids[1]]["Feed2Grid"]
            synth_hh_update.append(d)
    pd.DataFrame(synth_hh_update).to_csv('output/synth_hh_pv_benefit_updated.csv', index=False)


if __name__ == "__main__":
    # describe_synth_hh()
    # map_synth_hh_flex_scenarios()
    calc_pv_benefit()
