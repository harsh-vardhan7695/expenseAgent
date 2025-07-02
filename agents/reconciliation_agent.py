from autogen import Agent
import pandas as pd
from typing import Dict, Any

class ReconciliationAgent(Agent):
    def __init__(self, name="ReconciliationAgent"):
        super().__init__(name)

    def run(self, 
            citibank_path: str = 'data/citibank_transactions.xlsx', 
            concur_path: str = 'data/concur_transactions.xlsx',
            event_col: str = 'event_id') -> Dict[str, Any]:
        """
        Reads transaction files, reconciles them by a key column, and returns the common data.
        """
        print("Starting reconciliation...")
        try:
            citibank_df = pd.read_excel(citibank_path)
            concur_df = pd.read_excel(concur_path)
        except FileNotFoundError as e:
            print(f"Error: One of the transaction files was not found. {e}")
            return {"all_found": False, "error": str(e)}
        except Exception as e:
            print(f"Error reading Excel files: {e}. Please ensure they are valid .xlsx files.")
            return {"all_found": False, "error": str(e)}

        if event_col not in citibank_df.columns or event_col not in concur_df.columns:
            error_msg = f"Error: Key column '{event_col}' not found in one or both files."
            print(error_msg)
            return {"all_found": False, "error": error_msg}

        citibank_events = set(citibank_df[event_col].unique())
        concur_events = set(concur_df[event_col].unique())
        missing_events = list(citibank_events - concur_events)
        all_found = len(missing_events) == 0

        print(f"Found {len(citibank_events)} unique events in CitiBank and {len(concur_events)} in Concur.")

        common_events = citibank_events & concur_events
        citibank_common = citibank_df[citibank_df[event_col].isin(common_events)]
        concur_common = concur_df[concur_df[event_col].isin(common_events)]

        print(f"Reconciliation complete. Found {len(common_events)} common events.")
        return {
            "all_found": all_found,
            "citibank_df": citibank_common,
            "concur_df": concur_common,
            "event_col": event_col,
            "missing_events": missing_events
        }

