if exists('g:loaded_sphinx')
  finish
endif

let g:sphinx_html_output_dirs = ['_build/html', 'build/html', '../_build/html', '../build/html']
let g:sphinx_doctrees_output_dirs = ['_build/doctrees', 'build/doctrees', '../_build/doctrees', '../build/doctrees']
let g:sphinx_include_intersphinx_data = 1
let g:sphinx_always_use_scoped_targets = 1

let g:loaded_sphinx = 1
