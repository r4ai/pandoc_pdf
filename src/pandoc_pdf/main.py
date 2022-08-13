from utils.functions import init_config, init_setting, generate_defaults_file_by_preset, generate_command_docker, generate_command_pandoc
from utils.env import CACHE_DIR, CONFIG_DIR
from pathlib import Path
import subprocess as sp
import click
from copy import deepcopy
from pprint import pprint
import sys


@click.command()
@click.option(
    '--debug',
    is_flag=True
)
@click.option(
    '-D', '--docker',
    type=str
)
@click.option(
    '-v', '--volume',
    type=str,
    multiple=True,
)
@click.option(
    '-V', '--variable',
    type=str,
    multiple=True
)
@click.option(
    '-M', '--metadata',
    type=str,
    multiple=True
)
@click.option(
    '-p', '--preset',
    type=click.Choice(['html5', 'latex']),
    default="latex"
)
@click.option(
    '-o', '--output',
    type=click.Path(path_type=Path),
    default='NULL',
)
@click.argument(
    'input_file',
    type=click.Path(exists=True, path_type=Path),
)
def pandoc_pdf(input_file: Path, debug: bool, docker, volume, metadata, variable, preset, output):
    """Command to generate pdf easily in pandoc."""
    output_file = deepcopy(output)
    volumes = deepcopy(volume)
    variables = deepcopy(variable)
    metadatas = deepcopy(metadata)
    del output
    del volume
    del variable
    del metadata
    if str(output_file) == 'NULL':
        output_file = Path(f"{input_file.stem}.pdf")
    init_config()
    generate_defaults_file_by_preset()
    setting_obj = init_setting(docker, volumes)
    if setting_obj['docker']['use_docker'] == True:
        defaults_file = Path(f'/cache/defaults_{preset}.yml')
    else:
        defaults_file = CACHE_DIR / f'defaults_{preset}.yml'

    # * ---Execute command
    args_docker = generate_command_docker(setting_obj)
    args_pandoc = generate_command_pandoc(
        setting_obj, defaults_file, input_file, output_file, preset, variables, metadatas)
    args = ' '.join(args_docker) + f" \"{' '.join(args_pandoc)}\""
    result = sp.run(args, shell=True)
    result_status = 'Succeeded' if result.returncode == 0 else 'Failed'
    result_color = '' if result.returncode == 0 else 'red'
    click.secho(
        f'{result_status} to generate {str(output_file)} from {str(input_file)} by {preset}.',
        fg=result_color,
        bold=True
    )

    #! ---DEBUG
    if debug:
        click.secho('\n---< DEBUG >---', fg='red')
        click.secho('Executed command:')
        click.secho(f'  {result.args}', bold=True)
        pprint(sys.path)

    if result.returncode == 0:
        return 0
    else:
        return 1


if __name__ == "__main__":
    pandoc_pdf()
