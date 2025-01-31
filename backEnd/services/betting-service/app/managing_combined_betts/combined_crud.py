from sqlalchemy.orm import Session
from decimal import Decimal
from app.models import CombinedBet, CombinedBetDetail
from app.schemas import CombinedBetCreate

def create_combined_bet(db: Session, combined_bet_data: CombinedBetCreate):
    # Calculate base odds
    num_bets = len(combined_bet_data.details)
    if num_bets == 0:
        raise ValueError("No details in combined bet.")

    base_odds = Decimal("1.0")
    for detail in combined_bet_data.details:
        base_odds *= detail.coefficient

    bonus_percentage = 0
    if num_bets >= 5:
        bonus_percentage = 10 + 2 * (num_bets - 5)
    final_odds = base_odds * (Decimal("1.0") + Decimal(bonus_percentage) / Decimal("100.0"))

    potential_win = combined_bet_data.total_amount * final_odds

    new_combined_bet = CombinedBet(
        user_id=combined_bet_data.user_id,
        total_amount=combined_bet_data.total_amount,
        total_odds=final_odds,
        potential_win=potential_win,
        status="pending",
        created_at="NOW()"     
    )
    db.add(new_combined_bet)
    db.commit()
    db.refresh(new_combined_bet)

    # Create details
    for leg in combined_bet_data.details:
        new_detail = CombinedBetDetail(
            combined_bet_id=new_combined_bet.combined_bet_id,
            match_id=leg.match_id,
            bet_type=leg.bet_type,
            selected_team=leg.selected_team,
            coefficient=leg.coefficient,
            # status ="pending",
            created_at="NOW()"  # or datetime.now()
        )
        db.add(new_detail)

    db.commit()
    db.refresh(new_combined_bet)

    return new_combined_bet
