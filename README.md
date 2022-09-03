# 自動裁定取引システム
このシステムは、BybitとBinanceの2つの市場で発生する仮想通貨価格の歪みを検知し、利益が出ると判断した場合エントリーし、価格が収束した後エグジットする裁定取引を行うシステムです。<br>
※現時点で利益計算や売買アルゴリズムが未完成のため、予期しない損失が出る可能性があります。

## 免責
当サイトに掲載されているコードは、有価証券や仮想通貨など投資を勧誘することを目的としておらず、また何らかの保証・約束をするものではありません。
投資に関する決定は利用者様ご自身のご判断において行っていただきますようお願い申し上げます。
また、掲載情報のご利用に起因するいかなる損害につきましても、当方は責任を負いかねます。


## Required setup 
```
pip install pybit
pip install binance-futures-connector
```

## Required env setup
### BYBIT
```
AK_BYBIT=
AS_BYBIT=
BYBIT_END_POINT=
```
### BINANCE
```
AK_BINANCE=
AS_BINANCE=
BINANCE_END_POINT=
```
### LINE NOTIFY
```
LINE_TOKEN=
LINE_END_POINT=
```
