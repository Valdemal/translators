import click

from config import TABLE, lexeme_factory, rules_to_choices
from translation import LexicalAnalyzer, SyntaxAnalyzer
from translation.types import Lexeme


def display_lexemes(lexemes: list[Lexeme]):
    click.echo(f"{'Лексема':<20}|{'Тип лексемы':<20}")
    click.echo('-' * 40)

    for lexeme in lexemes:
        click.echo(f"{str(lexeme.value):<20}|{str(lexeme.type):<20}")

    click.echo('-' * 40)


@click.command()
@click.argument('filename')
def translate_file(filename):
    try:
        with open(filename, 'r') as file:
            code = file.read()

        lexical_analyzer = LexicalAnalyzer(TABLE, lexeme_factory)
        syntax_analyzer = SyntaxAnalyzer(rules_to_choices)

        lexemes = lexical_analyzer.analyze(code)
        display_lexemes(lexemes)
        click.echo("Итог трансляции:")
        click.echo(syntax_analyzer.analyze(lexemes))

    except FileNotFoundError:
        click.echo(f"Ошибка: Файл '{filename}' не найден.")
    except Exception as e:
        click.echo(f"Произошла ошибка: {e}")


if __name__ == '__main__':
    translate_file()
