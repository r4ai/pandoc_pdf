# pandoc_pdf
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
>>> Succeeded to generate README.pdf from README.md by latex.

$ ls
>>> input.md input.pdf
```

## Requirements
### with docker
- docker

### without docker
- [pandoc](https://github.com/jgm/pandoc)
- [pandoc-crossref](https://github.com/lierdakil/pandoc-crossref)
- [pandoc-easy-templates](https://github.com/ryangrose/easy-pandoc-templates)

## Installation
For now, you need to clone this repository and then build with `poetry build`, and `pip install`.

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
TODO  

## Config
The config file is stored in `~/.config/pandoc_pdf/`. 

- `defaults.yml` allows you to save pandoc defaults for each preset(html5 & latex). 
- `settings.yml` allows you to configure whether docker is used or not.

TODO
