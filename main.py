import streamlit as st
import plotly.express as px

from power_model import PowerModel
from electricity_model import ElectricityModel
from financial_model import FinancialModel



def main(asic_miners, financial_model: FinancialModel):
    st.set_page_config(page_title="Bitcoin Mining", layout="wide")

    st.markdown("<h1 style='text-align: center;'>Bitcoin Mining</h1>", unsafe_allow_html=True)

    st.sidebar.subheader("Power Model Parameters")

    opex_proportion = st.sidebar.slider(
        "Proportion of Operating Expenses", 
        min_value=0.0,
        max_value=1.0, 
        step=0.01, 
        format="%.2f",
        value=0.15
    )

    electricity_available_per_year = st.sidebar.slider(
        "Electricity Available (in kWh/year)", 
        min_value=1_000_000,
        max_value=100_000_000, 
        step=1_000_000, 
        value=10_000_000

    )

    st.sidebar.subheader("Electricity Model Parameters")
    low_breakeven_cost, high_breakeven_cost = st.sidebar.slider(
        "Electricity Break-Even Cost (in \$)", 
        min_value=0.00,
        max_value=0.20, 
        value=(0.01, 0.10),
        step=0.01,
        format="$%.2f"
    )

    low_landfill_revenue_share, high_landfill_revenue_share = st.sidebar.slider(
        "Landfill Revenue Share", 
        min_value=0.0,
        max_value=0.4, 
        value=(0.05, 0.3),
        step=0.01,
        format="%.2f"
    )

    st.sidebar.subheader("Financial Model Parameters")
    mining_pool_fees = st.sidebar.slider(
        "Mining Pool Fees", 
        min_value=0.0,
        max_value=0.2, 
        step=0.01, 
        format="%.2f",
        value=0.02
    )
    hash_price_mean = st.sidebar.slider(
        "Mean Hash Price", 
        min_value=0.0,
        max_value=0.4, 
        step=0.01, 
        format="$%.2f",
        value=0.075
    )

    num_samples = st.sidebar.slider(
        "Number of Monte-Carlo Simulations", 
        min_value=10_000,
        max_value=500_000, 
        step=10_000, 
        value=100_000
    )

    electricity_model = financial_model._electricity_model
    power_model = financial_model._power_model

    power_model.set_opex_proportion(
        opex_proportion=opex_proportion
    )
    power_model.set_electricity_available_year(
        electricity_available_year=electricity_available_per_year
    )

    electricity_model.set_breakeven_costs(
        low_breakeven_cost=low_breakeven_cost,
        high_breakeven_cost=high_breakeven_cost
    )
    electricity_model.set_landfill_revenue_share(
        low_landfill_revenue_share=low_landfill_revenue_share,
        high_landfill_revenue_share=high_landfill_revenue_share
    )
    electricity_model.set_num_samples(
        num_samples=num_samples
    )

    financial_model.set_mining_pool_fees(
        mining_pool_fees=mining_pool_fees
    )
    financial_model.set_hash_price_mean(
        hash_price_mean=hash_price_mean
    )
    financial_model.set_num_samples(
        num_samples=num_samples
    )

    resulting_data = financial_model.get_data(asic_miners)

    st.subheader("Annual Land Fill Hash Revenue")
    fig = px.histogram(
        data_frame=resulting_data, 
        x='Annual Land Fill Hash Revenue', 
        color='Miner',
        barmode='overlay'
        )
    st.plotly_chart(fig, use_container_width=True, show_hist=False)

    st.subheader("Annual Miner Hash Revenue")
    fig = px.histogram(
        data_frame=resulting_data, 
        x='Annual Miner Hash Revenue', 
        color='Miner',
        barmode='overlay'
        )
    st.plotly_chart(fig, use_container_width=True, show_hist=False)

    st.subheader("Annual Miner Net Revenue")
    fig = px.histogram(
        data_frame=resulting_data, 
        x='Annual Miner Net Revenue', 
        color='Miner',
        barmode='overlay'
        )
    st.plotly_chart(fig, use_container_width=True, show_hist=False)

    st.subheader("Annual Combined Net Revenue")
    fig = px.histogram(
        data_frame=resulting_data, 
        x='Annual Combined Net Revenue', 
        color='Miner',
        barmode='overlay'
        )
    st.plotly_chart(fig, use_container_width=True, show_hist=False)




if __name__ == "__main__":
    asic_miners = {
        'S19 XP': {
            'name': 'S19 XP',
            'hash': 151,
            'power_use': 3247,
            'cost': 3473,
        },
        'S21' :
        {
            'name': 'S21',
            'hash': 200,
            'power_use': 3500,
            'cost': 5000,
        },
        'S21 Hydro': {
            'name': 'S21 Hydro',
            'hash': 335,
            'power_use': 5360,
            'cost': 6533,
        },  
    }

    power_model = PowerModel(
        miner_characteristics=asic_miners['S19 XP'], 
        opex_proportion=0.15, 
        electricity_available_year=10_000_000
    )

    electricity_model = ElectricityModel(
        low_breakeven_cost=0.05,
        high_breakeven_cost=0.20,
        low_landfill_revenue_share=0.05,
        high_landfill_revenue_share=0.20,
        num_samples=10_000
    )

    financial_model = FinancialModel(
        mining_pool_fees=0.02,
        hash_price_mean=0.07,
        power_model=power_model,
        electricity_model=electricity_model
    )
    main(asic_miners, financial_model)