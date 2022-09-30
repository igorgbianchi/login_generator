import click

from utils import general as general_utils
from utils.nlp import NLP


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
    default="output.json",
    help="JSON filepath to write the generated logins.",
)
@click.option(
    "--log-level",
    "-l",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Set program's log level.",
)
def generate_logins(input_filepath: str, output_filepath: str, log_level: str) -> None:
    logger = general_utils.get_logger(log_level)
    logger.info("Program started.")
    names = general_utils.read_names(input_filepath)
    nlp = NLP(logger=logger)
    normalized_names = [nlp.normalize(name) for name in names]
    logger.info("Names normalized.")
    output = general_utils.combine_all(normalized_names)
    logger.info("Logins generated.")
    general_utils.write_on_file(output_filepath, output)
    logger.info("Program finished.")


if __name__ == "__main__":
    generate_logins()
