from dataclasses import dataclass
from typing import Optional


@dataclass
class RiskParameters:
    max_risk_per_trade: float = 0.01  # 1% of account
    max_drawdown: float = 0.2  # 20% max drawdown
    max_position_size: float = 0.1  # 10% of account per trade


class RiskManager:
    """Handle risk calculations and validations."""

    def __init__(self, params: RiskParameters) -> None:
        self.params = params
        self.account_balance = 0.0  # this should be loaded from DB or API
        self.drawdown = 0.0

    def update_account_balance(self, balance: float) -> None:
        self.account_balance = balance

    def can_open_position(self, risk_amount: float) -> bool:
        if risk_amount > self.params.max_risk_per_trade * self.account_balance:
            return False
        if self.drawdown > self.params.max_drawdown * self.account_balance:
            return False
        return True

    def calculate_position_size(self, stop_loss_distance: float) -> float:
        risk_capital = self.params.max_risk_per_trade * self.account_balance
        if stop_loss_distance == 0:
            return 0.0
        return min(risk_capital / stop_loss_distance, self.params.max_position_size * self.account_balance)
