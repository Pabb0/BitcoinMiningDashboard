
from scipy import stats
import numpy as np
import pandas as pd

from power_model import PowerModel
from electricity_model import ElectricityModel


class FinancialModel():
    def __init__(
            self,
            mining_pool_fees: float,
            hash_price_mean: float,
            power_model: PowerModel,
            electricity_model: ElectricityModel,
            ) -> None:
        self._mining_pool_fees = mining_pool_fees
        self._hash_price_mean = hash_price_mean
        self._power_model = power_model
        self._electricity_model = electricity_model

        self._yearly_miner_costs_fraction = 0

        self._num_samples = self._electricity_model._num_samples
        self._simulated_hash_prices = self.sample_lognormal_hash_price()

    def set_mining_pool_fees(self, mining_pool_fees) -> None:
        self._mining_pool_fees = mining_pool_fees

    def set_yearly_miner_costs_fraction(self, yearly_miner_costs_fraction):
        self._yearly_miner_costs_fraction = yearly_miner_costs_fraction

    def set_hash_price_mean(self, hash_price_mean) -> None:
        if self._hash_price_mean == hash_price_mean:
            return None
        else:
            self._hash_price_mean = hash_price_mean
            self._simulated_hash_prices = self.sample_lognormal_hash_price()

    def set_num_samples(self, num_samples):
        if num_samples == self._num_samples:
            return None
        else:
            self._num_samples = num_samples
            self._simulated_hash_prices = self.sample_lognormal_hash_price()


    def sample_lognormal_hash_price(self) -> np.ndarray:
        # hash price denotes the price per day given so many hashes per second
        return self._hash_price_mean*stats.lognorm.rvs(
            s=np.log(1.5),
            loc=1,
            size=self._num_samples,
            random_state=0
        )
    

    def get_annual_hash_revenue_per_sample(self) -> np.ndarray:
        DAYS_PER_YEAR = 365.25
        total_hash_rate = self._power_model.get_total_miner_hash_rate()

        return self._simulated_hash_prices*total_hash_rate*DAYS_PER_YEAR
    

    def get_annual_land_fill_hash_revenue_per_sample(self) -> np.ndarray:
        return self.get_annual_hash_revenue_per_sample()*self._electricity_model.get_simulated_landfill_revenue_shares()
    

    def get_annual_miner_hash_revenue_per_sample(self) -> np.ndarray:
        return self.get_annual_hash_revenue_per_sample() - self.get_annual_land_fill_hash_revenue_per_sample()
    

    def get_annual_electricity_cost_of_mining_per_sample(self) -> np.ndarray:
        return self._electricity_model.get_simulated_breakeven_costs() * self._power_model.get_electricity_available_year()
    
        
    def get_annual_miner_net_revenue_per_sample(self) -> np.ndarray:
        bitcoin_mining_revenue = self.get_annual_miner_hash_revenue_per_sample()*(1 - self._mining_pool_fees) 
        operating_costs = self.get_annual_electricity_cost_of_mining_per_sample() * (1 + self._power_model.get_opex_proportion())
        miner_costs = self._power_model.get_total_miner_costs()*self._yearly_miner_costs_fraction


        return bitcoin_mining_revenue - operating_costs - miner_costs
    
    def get_combined_net_revenue_per_sample(self) -> np.ndarray:
        return self.get_annual_miner_net_revenue_per_sample() + self.get_annual_land_fill_hash_revenue_per_sample()
    

    def get_data(self, miner_dict) -> pd.DataFrame:
        result_df = pd.DataFrame()
        for miner in miner_dict:
            self._power_model.set_miner(miner_dict[miner])
            miner_result_df = pd.DataFrame()
            miner_result_df['Annual Land Fill Hash Revenue'] = self.get_annual_land_fill_hash_revenue_per_sample()
            miner_result_df['Annual Miner Hash Revenue'] = self.get_annual_miner_hash_revenue_per_sample()
            miner_result_df['Annual Miner Net Revenue'] = self.get_annual_miner_net_revenue_per_sample()
            miner_result_df['Annual Combined Net Revenue'] = self.get_combined_net_revenue_per_sample()
            miner_result_df['Miner'] = miner

            result_df = pd.concat([result_df, miner_result_df], axis=0)

        return result_df
