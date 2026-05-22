import yfinance as yf
import pandas as pd


class StockDataFetcher:

    def fetch_stock_data(self, symbol):

        stock_data = yf.download(
            symbol,
            period="1mo",
            progress=False
        )

        stock_data.reset_index(inplace=True)

        # Flatten multi-level columns
        stock_data.columns = [
            col[0] if isinstance(col, tuple) else col
            for col in stock_data.columns
        ]

        return stock_data