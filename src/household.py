from typing import Optional
from src.utils import dict_sample
import pandas as pd
import numpy as np


class Household:

    def __init__(self, index: int):
        self.index = index
        self.year: Optional[float] = None
        self.synth: Optional[str] = None
        self.hid: Optional[float] = None
        self.hh_type_a: Optional[str] = None
        self.state: Optional[int] = None
        self.imputed_newest_const_date: Optional[float] = None
        self.imputed_oldest_const_date: Optional[float] = None
        self.id_building_construction_period: Optional[int] = None
        self.imputed_house_condition: Optional[str] = None
        self.house_size: Optional[float] = None
        self.head_age: Optional[int] = None
        self.n_persons: Optional[float] = None
        self.n_kids: Optional[float] = None
        self.ac: Optional[int] = None

    def setup(self, household_info: dict):
        for key, value in household_info.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
        self.init_building_construction_period()
        return self

    def map_flex_scenario(self):
        # default values
        self.id_region = 1  # Germany
        self.id_space_heating_tank: int = 1  # default value
        self.id_hot_water_tank: int = 1  # default value
        self.id_heating_element: int = 1  # default value
        self.id_battery: int = 1  # default value, always "no battery"
        self.id_energy_price: int = 1

        # inferred with household_synth.rds
        self.id_building: int = self.map_building()
        self.id_boiler: int = self.map_boiler()
        self.id_behavior: int = self.map_behavior()
        self.id_space_cooling_technology: int = self.map_space_cooling_technology()

    def init_building_construction_period(self):
        self.id_building_construction_period = 0
        building_year = 0.5 * (self.imputed_newest_const_date + self.imputed_oldest_const_date)
        if building_year <= 1948:
            self.id_building_construction_period = 1
        elif 1949 <= building_year <= 1978:
            self.id_building_construction_period = 2
        elif 1979 <= building_year <= 1994:
            self.id_building_construction_period = 3
        elif 1995 <= building_year:
            self.id_building_construction_period = 4
        else:
            pass

    def map_building(self):
        id_building = 0
        SFH = ['undetached_house', 'detached_house', 'farm_house']
        RENOVATED = ['in a good condition', 'some renovations', 'full_renovations']
        if self.hh_type_a in SFH:
            if self.id_building_construction_period == 1:
                if self.imputed_house_condition in RENOVATED:
                    id_building = 1
                else:
                    id_building = 2
            elif self.id_building_construction_period == 2:
                if self.imputed_house_condition in RENOVATED:
                    id_building = 3
                else:
                    id_building = 4
            elif self.id_building_construction_period == 3:
                if self.imputed_house_condition in RENOVATED:
                    id_building = 5
                else:
                    id_building = 6
            elif self.id_building_construction_period == 4:
                if self.imputed_house_condition in RENOVATED:
                    id_building = 7
                else:
                    id_building = 8
            else:
                pass
        return id_building

    @staticmethod
    def map_boiler():
        heating_technology_stock = {
            1: 0.070070771,  # HP
            2: 0.516852021,  # gases
            3: 0.077408182,  # solids
            4: 0.03903943,  # district heating
            5: 0.296629596  # liquids
        }
        return dict_sample(heating_technology_stock)

    def map_behavior(self):
        id_behavior = 0
        if self.n_persons == 1:
            id_behavior = 1
        elif self.n_persons == 2:
            if self.head_age < 65:
                id_behavior = 2
            elif self.head_age >= 65:
                id_behavior = 5
        elif self.n_persons == 3:
            id_behavior = 3
        elif self.n_persons >= 4:
            id_behavior = 4
        else:
            pass
        return id_behavior

    def map_space_cooling_technology(self):
        ac_dict = {
            0: 1,
            1: 2
        }
        return ac_dict[int(self.ac)]

    def gen_flex_scenario(self):
        return{
            "year": self.year,
            "synth": self.synth,
            "hid": self.hid,
            "ID_Region": self.id_region,
            "ID_Building": self.id_building,
            "ID_Boiler": self.id_boiler,
            "ID_HeatingElement": self.id_heating_element,
            "ID_SpaceHeatingTank": self.id_space_heating_tank,
            "ID_HotWaterTank": self.id_hot_water_tank,
            "ID_SpaceCoolingTechnology": self.id_space_cooling_technology,
            "ID_EnergyPrice": self.id_energy_price,
            "ID_Behavior": self.id_behavior,
            "ID_Battery": self.id_battery,
        }












