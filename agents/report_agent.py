from autogen import Agent
import pandas as pd
import os

class ReportAgent(Agent):
    def run(self, split_expenses):
        # Aggregate by participant
        reports_dir = 'reports'
        os.makedirs(reports_dir, exist_ok=True)
        df = pd.DataFrame(split_expenses)
        report_files = []
        for participant, group in df.groupby('participant'):
            report_path = os.path.join(reports_dir, f'participant_{participant}.csv')
            group.to_csv(report_path, index=False)
            print(f"Generated report for {participant}: {report_path}")
            report_files.append(report_path)
        return report_files 