from .env import CONFIG_DIR, CACHE_DIR
import yaml
from pathlib import Path
import shutil

#! エラー defaults.ymlの内容がコピーされてない
def init_config() -> None:
    for dir_i in [CACHE_DIR, CONFIG_DIR]:
        if not dir_i.exists():
            dir_i.mkdir()
    for file_name in ['setting.yml', 'defaults.yml']:
        config_file_path = (CONFIG_DIR / file_name)
        if not config_file_path.exists():
            config_file_path.touch()
            with open(Path(__file__).parent / 'default_config' / file_name) as f:
                content_raw = f.read()
                content_obj = yaml.safe_load(content_raw)
            config_file_path.write_text(content_raw)
            del content_raw
            # * ---.tex
            if file_name == 'defaults.yml':
                for tex_file_name in content_obj['latex']['include-in-header']:
                    config_tex_file_path = CONFIG_DIR / \
                        ''.join(tex_file_name.split('/')[-1:])
                    if not config_tex_file_path.exists():
                        config_tex_file_path.touch()
                        with open(Path(__file__).parent / 'default_config' / config_tex_file_path.name) as f:
                            content_raw = f.read()
                        config_tex_file_path.write_text(content_raw)
                        del content_raw
    del file_name


def generate_defaults_file_by_preset() -> None:
    with open(CONFIG_DIR / 'defaults.yml') as f:
        defaults_obj: dict = yaml.safe_load(f)
    for preset_i in defaults_obj:
        defaults_by_preset: Path = CACHE_DIR / f'defaults_{preset_i}.yml'
        if not defaults_by_preset.exists():
            defaults_by_preset.touch()
        with open(defaults_by_preset, 'w') as f:
            yaml.dump(defaults_obj[preset_i], f,
                      encoding='utf-8', allow_unicode=True)
        # * ---.tex
        if 'include-in-header' in defaults_obj[preset_i]:
            for tex_file_name in [''.join(tex_file_path.split('/')[-1:]) for tex_file_path in defaults_obj[preset_i]['include-in-header']]:
                shutil.copy(CONFIG_DIR / tex_file_name,
                            CACHE_DIR / tex_file_name)


def init_setting(opt_docker, opt_volumes) -> dict:
    setting_file_path = CONFIG_DIR / 'setting.yml'
    with open(setting_file_path, 'r') as f:
        setting_obj = yaml.safe_load(f)

    setting_obj['docker'].setdefault('volumes', [])
    setting_obj['docker'].setdefault('other_option', "")
    if opt_docker:
        setting_obj['docker']['use_docker'] = True
        setting_obj['docker']['docker_image'] = opt_docker
    if opt_volumes:
        if opt_docker:
            setting_obj['docker']['volumes'] = opt_volumes
        else:
            setting_obj['docker']['volumes'].extend(opt_volumes)

    return setting_obj


def generate_command(input_file, output_file, setting_obj, opt_preset, opt_docker, opt_volumes, opt_variables, opt_metadatas) -> str:

    # * ---generate docker command
    setting_obj['docker'].setdefault('volumes', [])
    setting_obj['docker'].setdefault('other_option', "")
    args_docker = ['docker', 'run', '--rm', '-it', '--volume',
                   f'{CACHE_DIR}:/cache', '--entrypoint', '/bin/bash']

    if opt_docker:
        setting_obj['docker']['use_docker'] = True
        setting_obj['docker']['docker_image'] = opt_docker
    if opt_volumes:
        if opt_docker:
            setting_obj['docker']['volumes'] = opt_volumes
        else:
            setting_obj['docker']['volumes'].extend(opt_volumes)

    if setting_obj['docker']['use_docker'] == True:
        # 1. volumesをargs_dockerへ追加
        # 2. docker_imageをargs_dockerへ追加
        defaults_file = Path(f'/cache/defaults_{opt_preset}.yml')
        for volume_i in setting_obj['docker']['volumes']:
            args_docker.extend(['--volume', volume_i])
        args_docker.append(setting_obj['docker']['other_option'])
        args_docker.append(setting_obj['docker']['docker_image'])
        args_docker.append('-c')
    else:
        defaults_file = CACHE_DIR / f'defaults_{opt_preset}.yml'
        args_docker = []

    # * ---generate pandoc command
    args_pandoc = ['pandoc', str(input_file), '-t', opt_preset, '-o',
                   str(output_file), '-d', str(defaults_file)]
    for variable in opt_variables:
        args_pandoc.extend(['-V', variable])
    for metadata in opt_metadatas:
        args_pandoc.extend(['-M', metadata])

    return ' '.join(args_docker) + f" \"{' '.join(args_pandoc)}\""


def generate_command_docker(setting_obj):
    setting_obj['docker'].setdefault('volumes', [])
    setting_obj['docker'].setdefault('other_option', "")
    args_docker = ['docker', 'run', '--rm', '--volume',
                   f'{CACHE_DIR}:/cache', '--entrypoint', '/bin/bash']
    if setting_obj['docker']['use_docker'] == True:
        for volume_i in setting_obj['docker']['volumes']:
            args_docker.extend(['--volume', volume_i])
        args_docker.append(setting_obj['docker']['other_option'])
        args_docker.append(setting_obj['docker']['docker_image'])
        args_docker.append('-c')
    else:
        args_docker = []
    return args_docker


def generate_command_pandoc(setting_obj, defaults_file, input_file, output_file, opt_preset, opt_variables, opt_metadatas):
    args_pandoc = ['pandoc', str(input_file), '-t', opt_preset, '-o',
                   str(output_file), '-d', str(defaults_file)]
    for variable in opt_variables:
        args_pandoc.extend(['-V', variable])
    for metadata in opt_metadatas:
        args_pandoc.extend(['-M', metadata])
    return args_pandoc
