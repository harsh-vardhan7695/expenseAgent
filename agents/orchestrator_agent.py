from .reconciliation_agent import ReconciliationAgent
from .document_parser_agent import DocumentParserAgent
from .matching_agent import MatchingAgent
from .splitting_agent import SplittingAgent
from .report_agent import ReportAgent
from .notification_agent import NotificationAgent

class OrchestratorAgent:
    def __init__(self):
        print("Initializing Orchestrator and its agents...")
        self.reconciliation_agent = ReconciliationAgent()
        self.document_parser_agent = DocumentParserAgent()
        self.matching_agent = MatchingAgent()
        self.splitting_agent = SplittingAgent()
        self.report_agent = ReportAgent()
        self.notification_agent = NotificationAgent()

    def run(self):
        print("\n--- Starting Expense Processing Workflow ---")

        # Step 1: Reconcile transactions
        print("\n[Step 1/6] Running Reconciliation Agent...")
        reconciliation_result = self.reconciliation_agent.run()

        if not reconciliation_result.get("all_found", False):
            missing = reconciliation_result.get('missing_events', [])
            print(f"Warning: Reconciliation incomplete. Missing {len(missing)} events in Concur: {missing}")
            
            # Step 2: Parse expense documents because reconciliation was not fully successful
            print("\n[Step 2/6] Running Document Parser Agent...")
            parsed_expenses = self.document_parser_agent.run()
            if not parsed_expenses:
                print("No documents were parsed. Stopping workflow.")
                print("--- Workflow finished. ---")
                return

            # Step 3: Match expenses using the parsed documents
            print("\n[Step 3/6] Running Matching Agent...")
            matched_expenses = self.matching_agent.run(parsed_expenses, reconciliation_result)
        else:
            print("Reconciliation successful. All transactions found in Concur.")
            # Format the reconciled data to be used by the splitting agent
            citibank_df = reconciliation_result.get("citibank_df", pd.DataFrame())
            matched_expenses = []
            for _, row in citibank_df.iterrows():
                matched_expenses.append({"expense": row.to_dict(), "matched_citibank": row.to_dict(), "match_score": 1.0})

        # Step 4: Split expenses
        print("\n[Step 4/6] Running Splitting Agent...")
        split_expenses = self.splitting_agent.run(matched_expenses)

        # Step 5: Generate reports
        print("\n[Step 5/6] Running Report Agent...")
        reports = self.report_agent.run(split_expenses)

        # Step 6: Notify participants
        print("\n[Step 6/6] Running Notification Agent...")
        self.notification_agent.run(reports)

        print("\n--- Expense Processing Workflow Finished Successfully ---")

