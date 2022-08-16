import sys
import tomlkit
import re


def main():
    pyproject_path = sys.argv[1]
    version = re.search(r'\d+\.\d+\.\d+', sys.argv[2]).group()
    with open(pyproject_path, 'r') as f:
        pyproject_obj = tomlkit.parse(f.read())
    # ! LOG
    print(
        f"chenged the pyproject version from {pyproject_obj['tool']['poetry']['version']} to {version}"
    )
    pyproject_obj['tool']['poetry']['version'] = version
    with open(pyproject_path, 'w') as f:
        tomlkit.dump(pyproject_obj, f)


if __name__ == '__main__':
    main()
