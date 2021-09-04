import imaplib
import json 
import os 


# Load Config From Environment
transfer_dict = json.loads(os.environ["EMAILSYNC"])


# Transfer 
with imaplib.IMAP4_SSL(host=transfer_dict["server_from"]["host"], port=993) as server_from:
    server_from.login(transfer_dict["server_from"]["username"], transfer_dict["server_from"]["password"])
    with imaplib.IMAP4_SSL(host=transfer_dict["server_to"]["host"], port=993) as server_to:
        server_to.login(transfer_dict["server_to"]["username"], transfer_dict["server_to"]["password"])
        
        for dir_from, dir_to in transfer_dict["dirs"].items():
            box_select = server_from.select(dir_from, readonly=False)  #open box which will have its contents copied
            print('Fetching messages from \'%s\'...' % dir_from)
            resp, items = server_from.search(None, 'ALL')  #get all messages in the box
            msg_nums = items[0].split()
            print('%s messages to archive' % len(msg_nums))

            for msg_num in msg_nums:
                resp, data = server_from.fetch(msg_num, "(FLAGS INTERNALDATE BODY.PEEK[])") # get email
                message = data[0][1] 
                flags = imaplib.ParseFlags(data[0][0]) # get flags
                if len(flags) > 0:
                    flag_str = " ".join([f.decode() for f in flags])
                else: 
                    flag_str = b""
                print(flag_str)
                date = imaplib.Time2Internaldate(imaplib.Internaldate2tuple(data[0][0])) #get date
                copy_result = server_to.append(dir_to, flag_str, date, message) # copy to archive

                if copy_result[0] == 'OK': 
                    del_msg = server_from.store(msg_num, '+FLAGS', '\\Deleted') # mark for deletion

            ex = server_from.expunge() # delete marked
            print('expunge status: %s' % ex[0])
            if not ex[1][0]: # result can be ['OK', [None]] if no messages need to be deleted
                print('expunge count: 0')
            else:
                print('expunge count: %s' % len(ex[1]))
