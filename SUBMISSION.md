# Submission

## Repository URL
https://github.com/AndresHv007/Class-Activity-Strategy-Pattern---Checkout-Shipping

## Questions and Answers

### What varies?
The shipping cost calculation algorithms and pricing formulas for each shipping service.

### What stays stable?
The checkout workflow (`Checkout`), the `Order` data structure, total order calculation logic, and the `ShippingCostStrategy` interface contract.

### What complexity cost does Strategy introduce?
Class proliferation and indirection: each shipping algorithm requires an additional class, and client code must know how to instantiate or choose the appropriate strategy.
