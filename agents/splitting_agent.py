from autogen import Agent

class SplittingAgent(Agent):
    def run(self, matched_expenses):
        split_expenses = []
        for match in matched_expenses:
            expense = match["expense"]
            participants = expense.get("participant")
            if not participants:
                split_expenses.append({"participant": None, **match})
                continue
            # Support comma-separated participants or list
            if isinstance(participants, str):
                participants = [p.strip() for p in participants.split(",") if p.strip()]
            amount = float(expense.get("amount", 0))
            split_amount = amount / len(participants) if participants else amount
            for p in participants:
                split_expenses.append({
                    "participant": p,
                    "split_amount": split_amount,
                    **match
                })
        return split_expenses 