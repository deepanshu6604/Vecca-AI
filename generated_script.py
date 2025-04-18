import time

def handle_frustrated_user(refined_emotion, refined_intent):
    """
    Handles a frustrated user by checking task status, reporting, apologizing, and proposing solutions.

    Args:
        refined_emotion: The user's refined emotion (e.g., "Frustrated").
        refined_intent: A list of dictionaries, each describing an intent.
    """

    # Simulate a task that might have failed
    task_status = "incomplete"  # Change to "complete" for testing success
    error_message = "Database connection timed out."  # Example error

    # Check task status
    print("Checking task status...")
    time.sleep(1)  # Simulate processing time

    # Report status and address frustration
    print("\nReport:")
    if task_status == "complete":
        print("Your task has been completed successfully!")
    else:
        print(f"I understand your frustration.  Unfortunately, your task is {task_status}.")
        print(f"The following error occurred: {error_message}")
        print("I'm working to resolve this issue.")


    # Apologize
    print("\nApology:")
    print("I sincerely apologize for the inconvenience and frustration this has caused.")

    # Propose a solution
    print("\nProposed Solution:")
    if task_status == "incomplete":
        print("I'm currently attempting to reconnect to the database.  I'll notify you via email once the task is complete.")
        print("If the issue persists, I'll escalate this to our database administrator.")
        print("In the meantime, you can try [suggest a workaround, if applicable].")
    else:
        print("We're glad we could resolve this for you!")


# Example usage (replace with actual data from your system)
refined_emotion = "Frustrated"
refined_intent = [
    {"intent": "check_task_status", "description": "Check the status of the previously requested task(s)."},
    {"intent": "report_status", "description": "Report back to the user on the status of the task(s)."},
    {"intent": "apologize", "description": "Offer a sincere apology for the incomplete task."},
    {"intent": "propose_solution", "description": "Propose a solution or alternative approach."},
]

handle_frustrated_user(refined_emotion, refined_intent)