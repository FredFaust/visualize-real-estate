import plotly.graph_objs as go
import plotly as py


def mean_price_bar_chart(complete_data):
    classed_by_locality = {}
    for d in complete_data:
        price = d['price']
        locality = d['locality']
        try:
            if price != "":
                if locality in classed_by_locality:
                    classed_by_locality[locality].append(float(price))
                else:
                    classed_by_locality[locality] = [float(price)]
        except Exception as ex:
            print(ex)
            print(d)

    localities = []
    mean_prices = []
    count = []
    for l, p in classed_by_locality.items():
        mean_p = int(sum(p) / len(p))
        count.append("Houses : {}".format(len(p)))
        localities.append(l)
        mean_prices.append(mean_p)

    show_bar_chart(localities, mean_prices, count)


def show_bar_chart(titles, values, count):
    trace1 = go.Bar(
        x=titles,
        y=values,
        text=count,
        marker=dict(
            color='rgb(158,202,225)',
            line=dict(
                color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.8
    )

    data = [trace1]
    layout = go.Layout(
        title='Average Price by Locality',
    )

    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, filename='charts/bar-mean-prices-by-locality')
