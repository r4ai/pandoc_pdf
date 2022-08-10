from copy import deepcopy
from pprint import pprint
import click
import yaml
import subprocess as sp
import pathlib
import shutil
from pathlib import Path

CONFIG_DIR = Path.home() / '.config' / 'pandoc_pdf'
CACHE_DIR = Path(__file__).parent / 'cache'


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
    type=str
)
@click.option(
    '-V', '--variable',
    type=str,
    multiple=True
)
@click.option(
    '-p', '--preset',
    type=click.Choice(['html5', 'latex']),
    default='latex'
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
def pandoc_pdf(input_file: Path, debug: bool, docker, volume, variable, preset, output):
    """Command to generate pdf easily in pandoc."""

    # * ---初期設定
    output_file = deepcopy(output)
    variables = deepcopy(variable)
    del output
    del variable
    if str(output_file) == 'NULL':
        output_file = Path(f"{input_file.stem}.pdf")
    init_config()
    setting_obj = init_setting()

    # * ---profile毎のdefaults_${profile}.ymlを作成
    with open(CONFIG_DIR / 'defaults.yml') as f:
        defaults_obj: dict = yaml.safe_load(f)
    for profile in defaults_obj:
        defaults_by_profile: Path = CACHE_DIR / f'defaults_{profile}.yml'
        if not defaults_by_profile.exists():
            defaults_by_profile.touch()
        with open(defaults_by_profile, 'w') as f:
            yaml.dump(defaults_obj[profile], f,
                      encoding='utf-8', allow_unicode=True)
        # * ---.tex
        if 'include-in-header' in defaults_obj[profile]:
            for tex_file_name in [''.join(tex_file_path.split('/')[-1:]) for tex_file_path in defaults_obj[profile]['include-in-header']]:
                shutil.copy(CONFIG_DIR / tex_file_name,
                            CACHE_DIR / tex_file_name)

    defaults_file = CACHE_DIR / f'defaults_{preset}.yml'

    # * ---コマンドの作成
    args_docker = ['docker', 'run', '--rm', '-it', '--volume',
                   f'{CACHE_DIR}:/cache', '--entrypoint', '/bin/bash']
    if (setting_obj['docker']['use_docker'] == True) or docker:
        defaults_file = f'/cache/defaults_{preset}.yml'
    if setting_obj['docker']['use_docker'] == True:
        # * ---volume mount
        if volume:
            args_docker.extend(['--volume', volume])
        else:
            for volume_path in setting_obj['docker']['volume']:
                args_docker.extend(['--volume', volume_path])
        # * ---docker image
        if docker:
            args_docker.append(docker)
        else:
            args_docker.append(setting_obj['docker']['docker_image'])
        args_docker.append('-c')
    else:
        if docker:
            if volume:
                args_docker.extend(['--volume', volume])
            args_docker.append(docker)
            args_docker.append('-c')
        else:
            args_docker = []
    args_pandoc = ['pandoc', str(input_file), '-t', preset, '-o',
                   str(output_file), '-d', str(defaults_file)]
    for variable in variables:
        args_pandoc.extend(['--variable', variable])
    args = ' '.join(args_docker) + f" \"{' '.join(args_pandoc)}\""

    # * ---コマンドの実行
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

    if result.returncode == 0:
        return 0
    else:
        return 1


def init_config():
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir()
    if not CONFIG_DIR.exists():
        CONFIG_DIR.mkdir()
    for file_name in ['setting.yml', 'defaults.yml']:
        file_path = (CONFIG_DIR / file_name)
        if not file_path.exists():
            file_path.touch()
            with open(Path(__file__).parent / 'default_config' / file_name) as f:
                content_raw = f.read()
                content_obj = yaml.safe_load(content_raw)
            file_path.write_text(content_raw)
            del content_raw
            # * ---.tex
            if file_name == 'defaults.yml':
                for tex_file_name in content_obj['latex']['include-in-header']:
                    tex_file_path = CONFIG_DIR / \
                        ''.join(tex_file_name.split('/')[-1:])
                    if not tex_file_path.exists():
                        tex_file_path.touch()
                        with open(Path(__file__).parent / 'default_config' / tex_file_path.name) as f:
                            content_raw = f.read()
                        tex_file_path.write_text(content_raw)
                        del content_raw
    del file_name


def init_setting() -> dict:
    setting_file_path = CONFIG_DIR / 'setting.yml'
    with open(setting_file_path, 'r') as f:
        setting_obj = yaml.safe_load(f)
    return setting_obj


if __name__ == "__main__":
    pandoc_pdf()
