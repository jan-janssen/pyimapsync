# Sync Email between IMAP servers 
Use Github workflows to execute cron jobs

## Configuration

```
{
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
