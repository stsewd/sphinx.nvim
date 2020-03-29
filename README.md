# sphinx.nvim

Sphinx integrations for Neovim.

# Available integrations

## [coc.nvim](https://github.com/neoclide/coc.nvim/)

# Coming soon

- Support for Intersphinx
- Integration with (fzf)[https://github.com/junegunn/fzf/]

# Installation

Install using [vim-plug](https://github.com/junegunn/vim-plug).
Put this in your `init.vim`.

```vim
Plug 'stsewd/sphinx.nvim'
```

**Note:** You need to have `coc.nvim` installed to use the `coc.nvim` integration.
See <https://github.com/neoclide/coc.nvim/#quick-start>.

# Configuration

Default values are shown in the code blocks.

## g:sphinx_output_dirs

Where to search for the local inventory file (`objects.inv`).
The directories are relativa to the `conf.py` file.

```vim
let g:sphinx_output_dirs = ['_build/html', 'build/html', '../_build/html', '../build/html']
```

## g:sphinx_local_only

Fetch all inventory files from intersphinx or just the local inventory file.

```vim
let g:sphinx_local_only = 0
```
