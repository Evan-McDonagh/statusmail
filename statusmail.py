from config import config
from sys import argv
from statusmanager import check_status_and_generate_outage_report, get_up_state, update_up_state, should_email
from emails import outage_email, send_message

has_custom_status_check = "-c" in argv or "--custom" in argv

def main():
    up_state = get_up_state()
    outage_report = check_status_and_generate_outage_report(custom=has_custom_status_check)
    update_up_state(up_state,outage_report.response.ok)

    if should_email(up_state,outage_report.response.ok):
        email_message = outage_email(
            sender=config.sender,
            recipients=config.recipients,
            outage_report=outage_report
        )
        send_message(config.smtp,email_message)

    return

if __name__ == "__main__":
    main()
