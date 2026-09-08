from app.data.models import Candle


class CandleValidator:

    @staticmethod
    def validate(candle: Candle) -> None:

        # Price values must be positive
        if candle.open <= 0:
            raise ValueError("Open price must be greater than 0")

        if candle.high <= 0:
            raise ValueError("High price must be greater than 0")

        if candle.low <= 0:
            raise ValueError("Low price must be greater than 0")

        if candle.close <= 0:
            raise ValueError("Close price must be greater than 0")

        # Volume cannot be negative
        if candle.volume < 0:
            raise ValueError("Volume cannot be negative")

        # OHLC relationship
        if candle.high < candle.low:
            raise ValueError("High cannot be lower than low")

        if candle.high < candle.open:
            raise ValueError("High cannot be lower than open")

        if candle.high < candle.close:
            raise ValueError("High cannot be lower than close")

        if candle.low > candle.open:
            raise ValueError("Low cannot be higher than open")

        if candle.low > candle.close:
            raise ValueError("Low cannot be higher than close")