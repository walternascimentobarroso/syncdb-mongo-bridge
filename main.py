import json
import argparse
import ast
from exporter import export_collections
from importer import import_collections
from patch import patch_documents


def main():
    parser = argparse.ArgumentParser(description="MongoDB Exporter/Importer/Patcher")
    subparsers = parser.add_subparsers(dest="command")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export collections to JSON")
    export_parser.add_argument(
        "--collections", nargs="*", help="Collections to export (default: all)"
    )
    export_parser.add_argument(
        "--query",
        type=str,
        help='Query filter as a JSON string (e.g. \'{"status": "error"}\')',
        default="{}",
    )

    # Import command
    import_parser = subparsers.add_parser("import", help="Import collections from JSON")
    import_parser.add_argument(
        "--collections", nargs="*", help="Collections to import (default: all)"
    )

    # Patch command
    patch_parser = subparsers.add_parser(
        "patch", help="Patch documents in output folder"
    )
    patch_parser.add_argument(
        "--filter",
        required=True,
        type=str,
        help='Filter dict as string (e.g. \'{"connectionId": "old-id"}\')',
    )
    patch_parser.add_argument(
        "--update",
        required=True,
        type=str,
        help='Update dict as string (e.g. \'{"connectionId": "new-id"}\')',
    )

    args = parser.parse_args()

    if args.command == "export":
        query = json.loads(args.query)
        export_collections(collections=args.collections, query=query)
    elif args.command == "import":
        import_collections(collections=args.collections)
    elif args.command == "patch":
        try:
            filter_dict = ast.literal_eval(args.filter)
            update_dict = ast.literal_eval(args.update)
            if not isinstance(filter_dict, dict) or not isinstance(update_dict, dict):
                raise ValueError()
        except Exception:
            parser.error("Both --filter and --update must be valid Python dicts")
        patch_documents(filter_dict, update_dict)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
