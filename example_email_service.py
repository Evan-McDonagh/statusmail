from email.message import EmailMessage
from sys import argv, stdin
from email.message import EmailMessage
from email import message_from_string

# Example email service which can accept piped output of downchecker.py
# eg. 
# $ python3 downchecker.py | python3 example_email_service.py

def main():
    s = stdin.read()

    email = message_from_string(s)

    print(email.get("From"))

if __name__ == "__main__":
    main()