import pandas as pd
import numpy as np
import logging
from typing import Dict
from datetime import timedelta

logger = logging.getLogger("QFE.data_generation")

def generate_time_series(config: Dict) -> pd.DataFrame: # Geometric Browning Motion
    start_date = config.get("start_date")
    end_date = config.get("end_date")
    initial_price = config.get("initial_price")
    volatility = config.get("volatility")
    trend = config.get("trend")
    num_series = config.get("num_series", 1)
    timeframe = config.get("timeframe")

    if not all([start_date, end_date, initial_price, volatility, trend, num_series]> 0):
        logger.error("Missing/invalid parameters from cfg")
        return pd.DataFrame()

    try:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
    except ValueError:
        logger.error(f"Invalid date format. Std Format: YYYY-MM-DD")
        return pd.DataFrame()

    if(end_date < start_date):
        logger.error(f"Invalid date format. End Date is before Start Date")
        return pd.DataFrame()

    delta_t = timedelta(days=1)
    dates = pd.date_range(start_date, end_date, freq=delta_t)
    num_days = len(dates)

    prices=np.zeros((num_days, num_series))
    prices[0,:] = initial_price
    for t in range(1, num_days):
        z = np.random.normal(size=(num_series))
        prices[t,:] = prices[t-1,:] * np.exp((trend-0.5*volatility**2)*delta_t.days/365+volatility * np.sqrt(delta_t.days/365)*z)

    df=pd.DataFrame({'date': dates})
    for i in range(num_series):
        df[f'price_{i}'] = prices[:,i]
    return df


if __name__ == "__main__":
    config= {
        "start_date": "2020-01-01",
        "end_date": "2024-12-31",
        "initial_price": 100,
        "volatility": 0.2,
        "trend": 0.05,
        "num_series": 3,

    }

    df = generate_time_series(config)
    if not df.empty:
        print(df.head())
        print(df.tail())