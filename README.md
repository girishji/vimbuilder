# vimbuilder

Sphinx extension to add Vim help generation support. Create Vim help files for
searching and browsing documentation inside Vim and Neovim.

## Install

```sh
pip3 install vimbuilder
```

## Usage

Add the extension to your `conf.py` file:
```python
extensions = [
    ...,
    "vimbuilder",
    ...,
]
```

Build Vim help files with `sphinx-build` command

```sh
sphinx-build -M vimhelp ./docs ./build
```

## Configurations

You can add the following configurations to your `conf.py` file:

Option|Default|Description
------|-------|-----------
`vimhelp_tag_prefix`|`''`|String to prefix all tags. Useful in separating namespaces for each type of documentation.
`vimhelp_tag_suffix`|`''`|String to suffix all tags. See above.
`vimhelp_tag_filename'|`True`|Whether to attach filename to all tags in the file.
`vimhelp_filename_suffix'|';'|First tag in a help file is filename. Suffix will distinguish from Vim native help files.

## Projects using Vimbuilder

- [Python documentation](https://github.com/girishji/pythondoc.vim) for Vim and Neovim
