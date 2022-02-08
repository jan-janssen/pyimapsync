from argparse import ArgumentParser, SUPPRESS
from pyimapsync.shared import transfer_emails


def get_transfer_dict_cmd(server_from_str, server_to_str, folders_str):
    """
    Convert command line options to transfer dictionary

    Args:
        server_from_str (str): counter to iterate over environment variables
        server_to_str (str): Environment variables from os.environ
        folders_str (str)

    Returns:
        dict: transfer dictionary
    """
    server_from_lst = server_from_str.split(";")
    server_to_lst = server_to_str.split(";")
    folders_dict = {
        el[0]: el[1] for el in [s.split(":") for s in folders_str.split(";")]
    }

    return {
        "server_from": {
            "host": server_from_lst[0],
            "username": server_from_lst[1],
            "password": server_from_lst[2],
        },
        "server_to": {
            "host": server_to_lst[0],
            "username": server_to_lst[1],
            "password": server_to_lst[2],
        },
        "dirs": folders_dict,
    }


def command_line_parser():
    """
    Main function primarly used for the command line interface
    """
    parser = ArgumentParser(prog="syncemail", add_help=False)
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-f", "--server_from", help="Server to transfer emails from", required=True
    )
    required.add_argument(
        "-t", "--server_to", help="Server to transfer emails to", required=True
    )
    required.add_argument(
        "-i", "--inboxes", help="Inboxes to be transferred", required=True
    )
    optional.add_argument(
        "-h",
        "--help",
        action="help",
        default=SUPPRESS,
        help="show this help message and exit",
    )
    args = parser.parse_args()
    transfer_dict = get_transfer_dict_cmd(
        server_from_str=args.server_from,
        server_to_str=args.server_to,
        folders_str=args.inboxes,
    )
    transfer_emails(transfer_dict=transfer_dict)


if __name__ == "__main__":
    command_line_parser()
