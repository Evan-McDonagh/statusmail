# downchecker

Simple Python scripts for checking status of a web page and generating an email message in the event that the server does not respond with an OK status. I have found this useful for checking keeping track of the status of an express server occasionally stops responding correctly but does not crash out of the server process. 

These scripts are expected to be combined a scheduler and with some emailing service which can handle an EmailMessage output. The script will track the previous up/down state of the target domain and only return with an EmailMessage if the status has changed from UP to DOWN when it was last ran, and the email message can be piped via standard input to a script which can send the email. 

