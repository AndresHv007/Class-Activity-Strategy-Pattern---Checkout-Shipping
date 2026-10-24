from abc import ABC, abstractmethod
from .models import Order


class ShippingCostStrategy(ABC):
    @abstractmethod
    def calculate(self, order: Order) -> float:
        pass

    def calculate_cost(self, order: Order) -> float:
        return self.calculate(order)

    def shipping_cost(self, order: Order) -> float:
        return self.calculate(order)


class StandardShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        if order.subtotal >= 1000:
            return 0.0
        return 49.0


class ExpressShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 99.0 + 12.0 * order.weight_kg


class PickupShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 0.0


class SameDayShipping(ShippingCostStrategy):
    def calculate(self, order: Order) -> float:
        return 149.0 + 18.0 * order.weight_kg
