#!/usr/bin/env python3

import yaml
from pathlib import Path
import click


def reform(text: str) -> str:
    return text.replace("-", " ").capitalize()


@click.command()
@click.argument("filepath", type=click.Path(exists=True, dir_okay=False))
@click.option(
    "-d",
    "--mkdir",
    is_flag=True,
    help="also create directory structure at the FILENAME location",
)
def generate(filepath, mkdir):

    """
    \b
    Generates a numbered Johhny Decimal index in Markdown format.
    Can also create directory structure for the index.

    FILEPATH is a path to YAML template for Johnny Decimal structure.
    """

    basename = Path(filepath).stem

    markdown_lines = []
    directories = []

    with open(filepath) as file:
        jd = yaml.load(file, Loader=yaml.FullLoader)

    for i, (area, categories) in enumerate(jd.items()):
        markdown_lines.append(f"# {i}0-{i}9 {reform(area)}")

        uncategorized = [a for a in categories if isinstance(a, str)]
        categories = [
            {"uncategorized": uncategorized}
            ] + [a for a in categories if isinstance(a, dict)]

        for j, category_dict in enumerate(categories):
            category, *_ = category_dict.keys()
            projects, *_ = category_dict.values()
            markdown_lines.append(f"## {i}{j} {reform(category)}")
            projects = ["meta"] + projects

            for k, project in enumerate(projects):
                markdown_lines.append(f"### {i}{j}.{k:02d} {reform(project)}")
                directories.append(
                    f"{basename}"
                    f"/{i}0-{i}9 {reform(area)}"
                    f"/{i}{j} {reform(category)}"
                    f"/{i}{j}.{k:02d} {reform(project)}"
                )

    with open(f"{basename}.md", "w") as file:
        file.writelines([line + "\n" for line in markdown_lines])

    if mkdir:
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


if __name__ == "__main__":
    generate()
