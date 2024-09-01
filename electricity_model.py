from scipy import stats
import numpy as np

class ElectricityModel():

    def __init__(
            self, 
            low_breakeven_cost: float, 
            high_breakeven_cost: float, 
            low_landfill_revenue_share: float, 
            high_landfill_revenue_share: float,
            num_samples: int
        ):
        assert high_breakeven_cost > low_breakeven_cost
        assert 0 <= low_landfill_revenue_share < high_landfill_revenue_share <= 1

        self._num_samples = num_samples
        
        self._low_breakeven_cost = low_breakeven_cost
        self._high_breakeven_cost = high_breakeven_cost
        self._simulated_breakeven_costs = self.sample_breakeven_cost()

        self._low_landfill_revenue_share = low_landfill_revenue_share
        self._high_landfill_revenue_share = high_landfill_revenue_share
        self._simulated_landfill_revenue_shares = self.sample_landfill_revenue_share()

    def set_num_samples(self, num_samples):
        if num_samples == self._num_samples:
            return None
        else:
            self._num_samples = num_samples
            self._simulated_breakeven_costs = self.sample_breakeven_cost()
            self._simulated_landfill_revenue_shares = self.sample_landfill_revenue_share()

    def get_simulated_landfill_revenue_shares(self) -> np.ndarray:
        return self._simulated_landfill_revenue_shares
    
    def get_simulated_breakeven_costs(self) -> np.ndarray:
        return self._simulated_breakeven_costs
    
    def set_breakeven_costs(self, low_breakeven_cost: float, high_breakeven_cost: float) -> None:
        if low_breakeven_cost == self._low_breakeven_cost and high_breakeven_cost == self._high_breakeven_cost:
            return None
        else:
            self._low_breakeven_cost = low_breakeven_cost
            self._high_breakeven_cost = high_breakeven_cost
            self.sample_breakeven_cost()

    def sample_breakeven_cost(self) -> np.ndarray:
        mean_breakeven_cost = (self._low_breakeven_cost + self._high_breakeven_cost) / 2
        standard_deviation_breakeven_cost = (self._low_breakeven_cost + self._high_breakeven_cost) / 5

        sample = stats.lognorm.rvs(
            s=standard_deviation_breakeven_cost,
            loc=mean_breakeven_cost,
            size=self._num_samples,
            random_state=0
        )

        sample[sample < self._low_breakeven_cost] = self._low_breakeven_cost
        sample[sample > self._high_breakeven_cost] = self._high_breakeven_cost

        return sample
    
    def set_landfill_revenue_share(self, low_landfill_revenue_share: float, high_landfill_revenue_share: float) -> None:
        if low_landfill_revenue_share == self._low_landfill_revenue_share and high_landfill_revenue_share == self._high_landfill_revenue_share:
            return None
        else:
            self._low_landfill_revenue_share = low_landfill_revenue_share
            self._high_landfill_revenue_share = high_landfill_revenue_share
            self.sample_landfill_revenue_share()
    
    def sample_landfill_revenue_share(self) -> np.ndarray:
        scale = self._high_landfill_revenue_share - self._low_landfill_revenue_share

        return stats.uniform.rvs(
            loc=self._low_landfill_revenue_share,
            scale=scale,
            size=self._num_samples,
            random_state=0
        )