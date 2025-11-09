from src.parsing.argsparser import setup_argsparser
from src.strategies.strategies import Context
from config import setup_logger, config
from src.utils.cleaner import clear_folder


def main():
    argsparser = setup_argsparser()
    args = argsparser.parse_args()

    setup_logger(
        log_level=args.log_level,
        without_logs=args.without_logs,
        silent=args.silent,
    )

    if args.command == "strategy":
        context = Context(args.strategy_)
        context.start_strategy()
    if args.command == "clean":
        clear_folder(config.LOG_DIR)


if __name__ == "__main__":
    main()
