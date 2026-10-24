from .models import Order
from .strategies import ShippingCostStrategy


class Checkout:
    def __init__(self, strategy: ShippingCostStrategy | None = None):
        if strategy is not None and not isinstance(strategy, ShippingCostStrategy):
            raise ValueError(f"Invalid shipping strategy: {strategy}")
        self.strategy = strategy

    def set_strategy(self, strategy: ShippingCostStrategy) -> None:
        if not isinstance(strategy, ShippingCostStrategy):
            raise ValueError(f"Invalid shipping strategy: {strategy}")
        self.strategy = strategy

    def shipping_cost(self, order: Order, strategy: ShippingCostStrategy | None = None) -> float:
        if isinstance(order, ShippingCostStrategy) and isinstance(strategy, Order):
            order, strategy = strategy, order
        selected_strategy = strategy or self.strategy
        if not isinstance(selected_strategy, ShippingCostStrategy):
            raise ValueError(f"Invalid shipping strategy: {selected_strategy}")
        return selected_strategy.calculate(order)

    def total(self, order: Order, strategy: ShippingCostStrategy | None = None) -> float:
        if isinstance(order, ShippingCostStrategy) and isinstance(strategy, Order):
            order, strategy = strategy, order
        return order.subtotal + self.shipping_cost(order, strategy)
