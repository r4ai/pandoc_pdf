# pandoc_pdf 　[![ci](https://github.com/e9716/pandoc_pdf/actions/workflows/pandoc-build.yml/badge.svg?branch=main)](https://github.com/e9716/pandoc_pdf/actions/workflows/pandoc-build.yml)

Command to generate pdf easily with pandoc.  
If you already have docker installed, you don't even need to build an environment with pandoc. By default, the r4ai/pandoc image is used. This can be changed from `.config/pandoc_pdf/setting.yml`.

## QuickStart

Easiest command to generate pdf from markdown.

```bash
pandoc_pdf input.md
```

Here's an example of using `pandoc_pdf`.

```bash
$ ls
>>> input.md

$ pandoc_pdf input.md
>>> Succeeded to generate input.pdf from input.md by latex.

$ ls
>>> input.md input.pdf
```

## Requirements

### with docker

- python3.10^
- docker

### without docker

- python3.10^
- [pandoc](https://github.com/jgm/pandoc)
- [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)
- [pandoc-easy-templates](https://github.com/ryangrose/easy-pandoc-templates)

## Installation

```bash
pip install pandoc-pdf
```

## Usage

```txt
Usage: pandoc_pdf [OPTIONS] INPUT_FILE

  Command to generate pdf easily in pandoc.

Options:
  --debug
  -D, --docker TEXT
  -v, --volume TEXT
  -V, --variable TEXT
  -M, --metadata TEXT
  -p, --preset [html5|latex]
  -o, --output PATH
  --help                      Show this message and exit.
```

The --preset option provides the preset to be used.  
Also, the standard presets available are html5 and latex. Both presets are for Japanese, so if you want to use them in English, please edit them accordingly (you can change them from ~/.config/defaults.yml).

```bash
$ pandoc_pdf HOGE.md --preset html5
>>> Loading page (1/2)
>>> Printing pages (1/2)
>>> Done
>>> Succeeded to generate HOGE.pdf from HOGE.md by html5.
```

The "--debug" option shows the command that pandoc_pdf is actually executing.

```bash
$ pandoc_pdf HOGE.md --preset latex --debug
>>> Succeeded to generate HOGE.pdf from HOGE.md by latex.
>>>
>>> ---< DEBUG >---
>>> Executed command:
>>>   docker run --rm --volume /home/rai/.pyenv/versions/3.10.5/lib/python3.10/site-packages/pandoc_pdf_utils/cache:/cache --entrypoint /bin/bash --volume $(pwd):/build  r4ai/pandoc -c "pandoc HOGE.md -t latex -o HOGE.pdf -d /cache/defaults_latex.yml"
```

TODO

## Config

The config file is stored in `~/.config/pandoc_pdf/`.

- `defaults.yml` allows you to save pandoc defaults for each preset(html5 & latex).
- `settings.yml` allows you to configure whether docker is used or not.

TODO

## Completion

Completion is available for fish, bash, and zsh.

### Fish

Add this to `~/.config/fish/completions/pandoc_pdf.fish`:

```bash
eval (env _PANDOC_PDF_COMPLETE=fish_source pandoc_pdf)
```

### Bash

Add this to `~/.bashrc`:

```bash
eval "$(_PANDOC_PDF_COMPLETE=bash_source pandoc_pdf)"
```

### Zsh

Add this to ~/.zshrc:

```bash
eval "$(_PANDOC_PDF_COMPLETE=zsh_source pandoc_pdf)"
```

For more information, see [here](https://click.palletsprojects.com/en/8.1.x/shell-completion/).
