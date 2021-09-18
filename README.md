# Sync Email between IMAP servers 
This is yet another example to demonstrate how powerful the imaplib inside python is. 

**For Advanced Users**: Uses Github workflows to execute cron jobs for email synchronisation. 

## Python Interface
To test the script locally it can be imported as python module:
```
from pyimapsync import transfer_emails
transfer_emails(transfer_dict)
```
The transfer dictionary is defined as:  
```
transfer_dict = {
    "server_from": {
        "host": "oldimap.domain.com",
        "username": "user@old.domain.com",
        "password": "xxx"
    }, 
    "server_to": {
        "host": "newimap.domain.com",
        "username": "user@new.domain.com",
        "password": "xxx",
    },
    "dirs": {
        "folder_old": "folder_new"
    }
}
```

## Command Line Interface
On the command line the different parts of the connection are separated by semicolon:
```
python -m pyimapsync \
   --server_from "oldimap.domain.com;user@old.domain.com;xxx" \
   --server_to "newimap.domain.com;user@new.domain.com;xxx" \
   --inboxes "folder_old:folder_new"
```
