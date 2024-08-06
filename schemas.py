from typing import List

from pydantic import BaseModel, Field


class StockOrder(BaseModel):
    order_date: str = Field(description='委託日期')
    order_time: str = Field(description='委託時間')
    market_type: str = Field(description='盤別')
    trade_type: str = Field(description='交易類別')
    trade_condition: str = Field(description='交易條件')
    market: str = Field(description='股票名稱')
    order_amount: str = Field(description='成交股數')
    order_price: str = Field(description='價格')
    cancel_amount: str = Field(description='取消股數')
    fill_amount: str = Field(description='成交股數')
    avg_fill_price: str = Field(description='成交均價')
    state: str = Field(description='狀態')

    @staticmethod
    def from_list_data(data: List[str]):
        return StockOrder(
            order_date=data[0],
            order_time=data[1],
            market_type=data[2],
            trade_type=data[3],
            trade_condition=data[4],
            market=data[5],
            order_amount=data[6],
            order_price=data[7],
            cancel_amount=data[8],
            fill_amount=data[9],
            avg_fill_price=data[10],
            state=data[11]
        )


class FutureOrder(BaseModel):
    order_date: str = Field(description='委託日期')
    order_time: str = Field(description='委託時間')
    order_id: str = Field(description='委託單號')
    option_type: str = Field(description='期權別')
    trade_type: str = Field(description='交易類別')
    market: str = Field(description='商品名稱')
    order_price: str = Field(description='價格')
    order_amount: str = Field(description='口數')
    cancel_amount: str = Field(description='取消口數')
    fill_amount: str = Field(description='成交口數')
    avg_fill_price: str = Field(description='成交均價')
    position_action: str = Field(description='倉位動作')
    order_condition: str = Field(description='委託條件')
    action_device: str = Field(description='下單裝置')
    market_type: str = Field(description='盤別')
    state: str = Field(description='狀態')

    @staticmethod
    def from_list_data(data: List[str]):
        return FutureOrder(
            order_date=data[0],
            order_time=data[1],
            order_id=data[2],
            option_type=data[3],
            trade_type=data[4],
            market=data[5],
            order_price=data[6],
            order_amount=data[7],
            cancel_amount=data[8],
            fill_amount=data[9],
            avg_fill_price=data[10],
            position_action=data[11],
            order_condition=data[12],
            action_device=data[13],
            market_type=data[14],
            state=data[15]
        )
