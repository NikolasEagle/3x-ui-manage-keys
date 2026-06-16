import argparse
from .models import AuthInfo


def extract_info_from_flags() -> AuthInfo:
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=lambda prog: argparse.HelpFormatter(
            prog, max_help_position=40, width=120
        ),
    )
    parser.add_argument("-h", "--help", action="help", help="Show help information")
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        help="URL panel - http://<host>:<port>",
        required=True,
    )
    parser.add_argument(
        "-U",
        "--username",
        type=str,
        help="Username",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--password",
        type=str,
        help="Password",
        required=True,
    )
    parser.add_argument(
        "-i",
        "--id",
        type=int,
        help="Inbound ID",
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output directory to save keys",
        required=True,
    )
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Matrix config for sending keys",
        required=True,
    )
    args = parser.parse_args()

    return AuthInfo(
        PANEL_URL=args.url,
        USERNAME=args.username,
        PASSWORD=args.password,
        ID=args.id,
        OUTPUT=args.output,
        CONFIG=args.config,
    )
