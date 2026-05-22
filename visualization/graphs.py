import plotly.express as px
import plotly.graph_objects as go


class StockGraphs:

    # ==========================================
    # LINE CHART
    # ==========================================

    def line_chart(self, df, company_name):

        fig = px.line(
            df,
            x="Date",
            y="Close",
            title=f"{company_name} Line Chart"
        )

        return fig

    # ==========================================
    # BAR CHART
    # ==========================================

    def bar_chart(self, df, company_name):

        fig = px.bar(
            df,
            x="Date",
            y="Close",
            title=f"{company_name} Bar Chart"
        )

        return fig

    # ==========================================
    # AREA CHART
    # ==========================================

    def area_chart(self, df, company_name):

        fig = px.area(
            df,
            x="Date",
            y="Close",
            title=f"{company_name} Area Chart"
        )

        return fig

    # ==========================================
    # SCATTER PLOT
    # ==========================================

    def scatter_chart(self, df, company_name):

        fig = px.scatter(
            df,
            x="Date",
            y="Close",
            title=f"{company_name} Scatter Plot"
        )

        return fig

        # ==========================================
    # CANDLESTICK CHART
    # ==========================================

    def candlestick_chart(self, df, company_name):

        fig = go.Figure(data=[go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )])

        fig.update_layout(
            title=f"{company_name} Candlestick Chart"
        )

        return fig
