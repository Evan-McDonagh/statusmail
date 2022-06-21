# statusmail

A simple Python program for sending an alert email via `stmp` when a request to a given domain results in an error respponse. I have found this useful for keeping track of the status of an express server which occasionally stops responding correctly but does not crash out of the server process and trigger existing monitoring services. 

The script will track the previous up/down state of the target domain and only send an email if the status has changed from `UP` to `DOWN` when it was last ran. 

To use, setup your `config.json` with your details as follows:

```json
{
    "sender": "<My Email Display Name> [myemail@emaildomain.com]",
    "domain": "mydomain.tocheck.com",
    "recipients": [
        "email1@torecieve.com",
    ],
    "smtp": {
        "server": "smtp.somedomain.com",
        "login": "smtplogin@somedomain.com",
        "password": "password"
    }
}
```

Use of this program with your GMail account will require you te generate an app password via your Google account settings to use in the `password` field of the `config.json`.

To run:

```
$ python3 statusmail.py
```