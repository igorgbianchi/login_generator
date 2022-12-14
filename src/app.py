import logging

import click

from utils import general as general_utils
from utils.nlp import NLP


def get_logger(log_level: str) -> logging.Logger:
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=log_level
    )
    logger = logging.getLogger(__name__)

    return logger


@click.command()
@click.option(
    "--input-filepath",
    "-i",
    default="Massa de Dados.txt",
    help="Names' filepath to generate logins. Must be '.txt' extension.",
)
@click.option(
    "--output-filepath",
    "-o",
    default="output",
    help="Filepath to write the generated logins.",
)
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Set program's log level.",
)
def generate_logins(input_filepath: str, output_filepath: str, log_level: str) -> None:
    logger = get_logger(log_level)
    logger.info("Program started.")
    names = general_utils.read_names(input_filepath)
    nlp = NLP()
    normalized_names = nlp.normalize_many(names)
    logger.info("Names normalized.")
    output = general_utils.combine_all(normalized_names)
    logger.info(f"{len(output.data)} logins generated.")
    general_utils.write_on_file(output_filepath, output)
    logger.info("Saved on JSON file. Program finished.")


if __name__ == "__main__":
    generate_logins()
