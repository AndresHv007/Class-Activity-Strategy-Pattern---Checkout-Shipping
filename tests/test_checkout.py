import pytest
from strategy_checkout.checkout import Checkout
from strategy_checkout.models import Order
from strategy_checkout.strategies import (
    ShippingCostStrategy,
    StandardShipping,
    ExpressShipping,
    PickupShipping,
    SameDayShipping,
)


def test_shipping_cost_strategy_is_abstract():
    with pytest.raises(TypeError):
        ShippingCostStrategy()


def test_standard_shipping_costs_49_below_threshold():
    order = Order(750.0, 2.0)
    strategy = StandardShipping()
    assert strategy.calculate(order) == 49.0
    assert Checkout(strategy).shipping_cost(order) == 49.0
    assert Checkout().shipping_cost(order, strategy) == 49.0


def test_standard_shipping_is_free_at_1000_or_more():
    strategy = StandardShipping()
    assert strategy.calculate(Order(1000.0, 1.0)) == 0.0
    assert strategy.calculate(Order(1250.0, 3.5)) == 0.0
    assert Checkout(strategy).shipping_cost(Order(1250.0, 3.5)) == 0.0


def test_express_shipping_uses_base_plus_weight():
    order = Order(500.0, 3.5)
    strategy = ExpressShipping()
    assert strategy.calculate(order) == 141.0
    assert Checkout(strategy).shipping_cost(order) == 141.0
    assert Checkout().shipping_cost(order, strategy) == 141.0


def test_pickup_is_free():
    order = Order(500.0, 3.5)
    strategy = PickupShipping()
    assert strategy.calculate(order) == 0.0
    assert Checkout(strategy).shipping_cost(order) == 0.0
    assert Checkout().shipping_cost(order, strategy) == 0.0


def test_same_day_shipping_uses_base_plus_weight():
    order = Order(500.0, 2.0)
    strategy = SameDayShipping()
    assert strategy.calculate(order) == 185.0
    assert Checkout(strategy).shipping_cost(order) == 185.0
    assert Checkout().shipping_cost(Order(500.0, 3.5), strategy) == 212.0


def test_total_adds_shipping_cost():
    order = Order(500.0, 2.0)
    assert Checkout(StandardShipping()).total(order) == 549.0
    assert Checkout().total(order, SameDayShipping()) == 685.0


def test_checkout_allows_changing_strategy():
    checkout = Checkout(StandardShipping())
    order = Order(500.0, 2.0)
    assert checkout.shipping_cost(order) == 49.0
    checkout.set_strategy(SameDayShipping())
    assert checkout.shipping_cost(order) == 185.0


def test_unknown_or_missing_strategy_is_rejected():
    order = Order(500.0, 2.0)
    with pytest.raises(ValueError):
        Checkout().shipping_cost(order, "teleport")
    with pytest.raises(ValueError):
        Checkout("teleport")
    with pytest.raises(ValueError):
        Checkout().shipping_cost(order)


def test_custom_strategy_without_modifying_checkout():
    class FlatShipping(ShippingCostStrategy):
        def calculate(self, order: Order) -> float:
            return 25.0

    order = Order(100.0, 1.0)
    assert Checkout(FlatShipping()).shipping_cost(order) == 25.0
