from typing import Optional


class Household:

    def __init__(self):
        self.hid: Optional[float] = None
        self.hh_type_a: Optional[str] = None
        self.hh_type_e: Optional[str] = None
        self.imputed_newest_const_date: Optional[float] = None
        self.imputed_oldest_const_date: Optional[float] = None
        self.imputed_house_condition: Optional[str] = None
        self.house_size: Optional[float] = None
        self.n_persons: Optional[float] = None
        self.n_kids: Optional[float] = None
        self.ac: Optional[int] = None
        self.pv: Optional[int] = None

    def setup(self, household_info: dict):
        for key, value in household_info.items():
            if key in self.__dict__.keys():
                setattr(self, key, value)
        return self

    def map_flex_scenario(self):
        # default values
        self.id_region = 1  # Germany
        self.id_space_heating_tank: int = 1  # default value
        self.id_hot_water_tank: int = 1  # default value
        self.id_heating_element: int = 1  # default value
        self.id_vehicle: int = 1  # default value, always "no EV"
        self.id_battery: int = 1  # default value, always "no battery"
        self.id_energy_price: int = 1

        # inferred with household_synth.rds
        self.id_building: int = self.map_building()
        self.id_boiler: int = self.map_boiler()
        self.id_behavior: int = self.map_behavior()
        self.id_space_cooling_technology: int = self.map_space_cooling_technology()

        # focusing technology: take the difference of 1 and 2
        self.id_pv: int = 1

    def map_building(self):
        # a representative building from the database will be mapped based on
        self.hh_type_a: Optional[float] = None  # SFH values: undetached house, detached house, and farm house.
        self.hh_type_e: Optional[str] = None  # urban_region or rural_region
        self.imputed_newest_const_date: Optional[float] = None  # starting year of construction
        self.imputed_oldest_const_date: Optional[float] = None  # ending year of construction
        self.imputed_house_condition: Optional[str] = None  # values: in a good condition, some renovations, full_renovations, dilapidated, NAs (as “in a good condition").
        self.house_size: Optional[float] = None
        # missing --> age class, renovation information
        return 1

    def map_boiler(self):
        # type of heating system and heating technology --> mapped based on RENDER data
        self.hh_type_a: Optional[float] = None  # SFH values: undetached house, detached house, and farm house.
        self.hh_type_e: Optional[str] = None  # urban_region or rural_region
        self.imputed_newest_const_date: Optional[float] = None  # starting year of construction
        self.imputed_oldest_const_date: Optional[float] = None  # ending year of construction
        return 1

    def map_behavior(self):
        # appliance electricity and hot water profiles
        # --> without teleworking, we distribute annual consumption (according to person number) to generic profiles
        # --> with teleworking, we generate profiles based on assumptions of teleworking and household composition
        self.n_persons: Optional[float] = None
        self.n_kids: Optional[float] = None
        return 1

    def map_space_cooling_technology(self):
        ac_dict = {
            0: 1,
            1: 2
        }
        return ac_dict[int(self.ac)]

    def gen_flex_scenario(self):
        return{
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
            "ID_PV": self.id_pv,
            "ID_Battery": self.id_battery,
            "ID_Vehicle": self.id_vehicle,
        }

    def energy_cost_change(self):
        # Energy cost change of following technology changes can be fetched from FLEX-Operation results database
        # adopting PV or increasing its size
        # adopting battery or increasing its size
        # switch to HP from a fuel-based boiler
        # adopting SEMS
        ...











