import re
import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from blockchain import blockexplorer
from blockchain import statistics
import datetime


stats = statistics.get()
valor_moeda = stats.market_price_usd


def to_btc(val):
    return val/100000000


datas = []
alturas = []
volumes_btc = []
volume_dolar = []
carteiras = []

qtd = 300

for x in range(0, qtd):
    block = blockexplorer.get_block_height(x)
    altura = block[0].height
    print(altura)
    alturas.append(altura)
    for transaction in block[0].transactions:
        timestamp = transaction.time
        data = datetime.datetime.fromtimestamp(timestamp)
        data = data.strftime('%Y-%m-%d %H:%M:%S')
        datas.append(data)
        # isso aqui é pra pegar apenas as transaçoes válidas
        if transaction.block_height != -1:
            for saida in transaction.outputs:
                endereco = saida.address
                carteiras.append(endereco)
                value = to_btc(saida.value)
                volumes_btc.append(value)
                volume_dolar.append(value * valor_moeda)


fig = make_subplots(
    rows=3, cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    specs=[[{"type": "table"}],
           [{"type": "scatter"}],
           [{"type": "scatter"}]]
)

fig.add_trace(
    go.Scatter(
        x=datas,
        y=volumes_btc,
        mode="lines",
        name="quantidade mineirada"
    ),
    row=3, col=1
)
""" fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Hash-rate"],
        mode="lines",
        name="hash-rate-TH/s"
    ),
    row=2, col=1
) """

fig.add_trace(
    go.Table(
        header=dict(
            values=["Data da <br> transação",
                    "Altura do <br> Bloco",
                    "volume de <br> saída (BTC)",
                    "Valor em<br>Dólar",
                    "carteira de <br> destino"],
            font=dict(size=10),
            align="left"
        ),
        cells=dict(
            values=[datas, alturas, volumes_btc, volume_dolar, carteiras],
            align="left")
    ),
    row=1, col=1
)

fig.update_layout(
    height=800,
    width=1200,
    showlegend=False,
    title_text="primeiros 300 blocos",
)

fig.show()
