import imaplib


def _add_ports_to_transferdict(transfer_dict):
    """
    Validate the transfer dict to check if it specifies the port, otherwise set the default port to 993

    Args:
        transfer_dict (dict): transfer dictionary

    Returns:
        dict: transfer dictionary
    """
    for ts in [transfer_dict["server_from"], transfer_dict["server_to"]]:
        if "port" not in ts.keys():
            ts["port"] = 993
    return transfer_dict


def transfer_emails(transfer_dict):
    """
    Transfer the emails using the imaplib
    Based on https://stackoverflow.com/questions/7029702/script-to-move-messages-from-one-imap-server-to-another

    Args:
        transfer_dict (dict): transfer dictionary
    """
    transfer_dict = _add_ports_to_transferdict(transfer_dict)
    with imaplib.IMAP4_SSL(
            host=transfer_dict["server_from"]["host"],
            port=transfer_dict["server_from"]["port"]
    ) as server_from:
        server_from.login(
            transfer_dict["server_from"]["username"],
            transfer_dict["server_from"]["password"]
        )
        with imaplib.IMAP4_SSL(
                host=transfer_dict["server_to"]["host"],
                port=transfer_dict["server_from"]["port"]
        ) as server_to:
            server_to.login(
                transfer_dict["server_to"]["username"],
                transfer_dict["server_to"]["password"]
            )
            for dir_from, dir_to in transfer_dict["dirs"].items():
                _ = server_from.select(
                    dir_from,
                    readonly=False
                )
                print('Fetching messages from \'%s\'...' % dir_from)
                resp, items = server_from.search(None, 'ALL')
                msg_nums = items[0].split()
                print('%s messages to archive' % len(msg_nums))

                for msg_num in msg_nums:
                    resp, data = server_from.fetch(
                        msg_num,
                        "(FLAGS INTERNALDATE BODY.PEEK[])"
                    )
                    message = data[0][1]
                    flags = imaplib.ParseFlags(data[0][0])
                    if len(flags) > 0:
                        flag_str = " ".join([f.decode() for f in flags])
                    else:
                        flag_str = b""
                    date = imaplib.Time2Internaldate(
                        imaplib.Internaldate2tuple(
                            data[0][0]
                        )
                    )
                    copy_result = server_to.append(
                        dir_to,
                        flag_str,
                        date,
                        message
                    )

                    if copy_result[0] == 'OK':
                        _ = server_from.store(
                            msg_num,
                            '+FLAGS',
                            '\\Deleted'
                        )

                ex = server_from.expunge()
                print('expunge status: %s' % ex[0])
                if not ex[1][0]:
                    print('expunge count: 0')
                else:
                    print('expunge count: %s' % len(ex[1]))
