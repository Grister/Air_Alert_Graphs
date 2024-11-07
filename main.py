import os
import pandas as pd
import plotly.express as px

from compare_data import get_data


def collect_alerts():
    json_list = os.listdir(path="archive")
    data = []

    for file in json_list:
        data.extend(get_data(f"archive/{file}"))

    return data


def graph_by_region(data):
    df = pd.DataFrame(data)

    alerts_by_region = df.groupby('region').size().reset_index(name='alert_count')
    data_by_region = alerts_by_region[alerts_by_region['alert_count'] > 100]

    graph = px.bar(data_by_region.sort_values(by="alert_count", ascending=False),
                   x='region', y='alert_count', color='region',
                   title="Кількість тревог по регіонах",
                   labels={"alert_count": "Кількість тревог", "region": "Регіон"})

    graph.update_layout(xaxis_tickangle=-45)
    graph.show()


def graph_by_year(data):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    df['year_month'] = df['date'].dt.to_period('M')
    df['year_month'] = df['year_month'].dt.to_timestamp()
    df['year_month_str'] = df['year_month'].dt.strftime('%B %Y')

    alerts_by_year = df.groupby(['year_month', 'year_month_str']).size().reset_index(name='alert_count')

    graph = px.bar(alerts_by_year.sort_values(by="year_month", ascending=False),
                   x='alert_count', y='year_month_str', color='year_month_str',
                   title="Кількість тревог по місяцях",
                   labels={"alert_count": "Кількість тревог", "year_month_str": "Місяць"})

    graph.update_layout(xaxis_tickangle=-45)
    graph.show()


def main():
    alerts = collect_alerts()

    graph_by_region(alerts)
    graph_by_year(alerts)


if __name__ == '__main__':
    main()
