# sphinx.nvim

[![CI](https://github.com/stsewd/sphinx.nvim/workflows/CI/badge.svg)](https://github.com/stsewd/sphinx.nvim/actions?query=workflow%3ACI)

[Sphinx](https://www.sphinx-doc.org/) integrations for Neovim.

**This plugin is still under development, some functionalities may change.**

![sphinx-nvim-coc](https://user-images.githubusercontent.com/4975310/105564899-353d8f80-5cf2-11eb-8f05-63b1ed5c3106.gif)

# Contents

* [Installation](#installation)
* [Available integrations](#available-integrations)
  - [coc.nvim](#cocnvim)
  - [nvim-treesitter](#nvim-treesitter)
* [Coming soon](#coming-soon)
* [Configuration](#configuration)

# Installation

Install using [vim-plug](https://github.com/junegunn/vim-plug).
Put this in your `init.vim`.

```vim
Plug 'stsewd/sphinx.nvim', { 'do': ':UpdateRemotePlugins' }
```

# Available integrations

## [coc.nvim](https://github.com/neoclide/coc.nvim/)

Source for [cross-referencing roles](https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#cross-referencing-syntax),
i.e `:ref:`, `:doc:`, `py:func`, etc.

**Note:** this plugin makes use of the inventory file from Sphinx,
so you need to have built your docs at least once to get suggestions,
and rebuild when your docs change to get the up to date suggestions.
You can use [sphinx-autobuild](https://github.com/GaretJax/sphinx-autobuild) to rebuild your docs automatically when there is a change.

## [nvim-treesitter](https://github.com/nvim-treesitter/nvim-treesitter)

Extra [queries](after/queries/rst/) for `rst`.
This includes highlights for Sphinx directives and roles,
and injections for directives from Sphinx and popular extensions (like ``code-block`` or ``tabs``).

# Coming soon

- Integration with [fzf](https://github.com/junegunn/fzf/)

# Configuration

Default values are shown in the code blocks.

## General settings

### g:sphinx_default_role

[Default role](https://www.sphinx-doc.org/page/usage/configuration.html#confval-default_role) (words surrounded by `` `single back-quotes` ``).

```vim
let g:sphinx_default_role = 'any'
```

### g:sphinx_html_output_dirs

Where to search for the local inventory file (`objects.inv`).
The directories are relative to the `conf.py` file.

```vim
let g:sphinx_html_output_dirs = [
      \ '_build/html', 'build/html',
      \ '../_build/html', '../build/html',
      \ '_build/dirhtml', 'build/dirhtml',
      \ '../_build/dirhtml', '../build/dirhtml',
      \]
```

### g:sphinx_default_dirs

If you want to extend the defaults values from `g:sphinx_html_output_dirs` and `g:sphinx_doctrees_output_dirs`
instead of replacing them.

```vim
let g:sphinx_default_dirs = 1
```

## Intersphinx related settings

### g:sphinx_include_intersphinx_data

If results should include information from Intersphinx.

```vim
let g:sphinx_include_intersphinx_data = 1
```

### g:sphinx_doctrees_output_dirs

Where to search for the environment file (`environment.pickle`),
this file contains the inventories from Intersphinx.
The directories are relative to the `conf.py` file.

```vim
let g:sphinx_doctrees_output_dirs = [
      \ '_build/doctrees', 'build/doctrees',
      \ '../_build/doctrees', '../build/doctrees',
      \ '_build/html/.doctrees', 'build/html/.doctrees',
      \ '../_build/html/.doctrees', '../build/html/.doctrees',
      \ '_build/dirhtml/.doctrees', 'build/dirhtml/.doctrees',
      \ '../_build/dirhtml/.doctrees', '../build/dirhtml/.doctrees',
      \]
```

### g:sphinx_always_use_scoped_targets

Always prefix the reference with the name of the target,
i.e use `` :ref:`<python:comparisons>` `` instead of `` :ref:`<comparisons>` ``
to link to the label “comparisons” in the doc set “python”.

```vim
let g:sphinx_always_use_scoped_targets = 1
```
