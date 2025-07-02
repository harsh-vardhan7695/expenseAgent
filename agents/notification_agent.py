from autogen import Agent
import os

class NotificationAgent(Agent):
    def run(self, reports):
        for report_path in reports:
            participant = os.path.basename(report_path).replace('participant_', '').replace('.csv', '')
            print(f"Notification: Sent report to participant {participant} ({report_path})") 