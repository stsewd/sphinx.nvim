if exists('g:loaded_sphinx')
  finish
endif

let g:sphinx_output_dirs = ['_build/html', 'build/html', '../_build/html', '../build/html']
let g:sphinx_local_only = 0

let g:loaded_sphinx = 1
