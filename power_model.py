from typing import Dict, Union

class PowerModel():
    def __init__(
            self, 
            miner_characteristics: Dict[str, Union[str, float]], 
            opex_proportion: float,
            electricity_available_year: float, 
        ):
        assert set(miner_characteristics).issuperset({'name', 'hash', 'power_use', 'cost'})

        self._miner_name: str = miner_characteristics['name']
        self._miner_hash: float = miner_characteristics['hash']
        self._miner_power_use: float =  miner_characteristics['power_use']
        self._miner_cost: float = miner_characteristics['cost']
        
        self._opex_proportion: float = opex_proportion
        self._electricity_available_year: float = electricity_available_year


    def set_miner(self, miner_characteristics: Dict[str, Union[str, float]]):
        assert set(miner_characteristics).issuperset({'name', 'hash', 'power_use', 'cost'})
        
        self._miner_name: str = miner_characteristics['name']
        self._miner_hash: float = miner_characteristics['hash']
        self._miner_power_use: float =  miner_characteristics['power_use']
        self._miner_cost: float = miner_characteristics['cost']
        
    def get_miner_name(self):
        return self._miner_name
    
    def get_miner_hash(self):
        return self._miner_hash
    
    def get_total_miner_hash_rate(self):
        return self._rigs_deployed * self._miner_hash
    
    def get_miner_power_use(self):
        return self._miner_power_use
    
    def get_miner_cost(self):
        return self._miner_cost
    
    def get_total_miner_costs(self):
        return self.get_miner_cost() * self.get_rigs_deployed()
    
    def set_opex_proportion(self, opex_proportion: float) -> None:
        self._opex_proportion = opex_proportion
    
    def get_opex_proportion(self):
        return self._opex_proportion
    
    def set_electricity_available_year(self, electricity_available_year: float):
        self._electricity_available_year = electricity_available_year
        self.update_rigs_deployed()

    def update_rigs_deployed(self):
        HOURS_PER_YEAR = 24*365.25
        WH_PER_KWH = 1000
        self._rigs_deployed = (WH_PER_KWH*self._electricity_available_year) / (HOURS_PER_YEAR*self._miner_power_use)

    def get_electricity_available_year(self):
        return self._electricity_available_year

    def get_rigs_deployed(self):
        return self._rigs_deployed
        
    
    