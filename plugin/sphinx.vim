if exists('g:loaded_sphinx')
  finish
endif

let g:sphinx_html_output_dirs = get(
      \ g:,
      \ 'sphinx_html_output_dirs',
      \ ['_build/html', 'build/html', '../_build/html', '../build/html', '_build/dirhtml', 'build/dirhtml', '../_build/dirhtml', '../build/dirhtml']
      \)
let g:sphinx_doctrees_output_dirs = get(
      \ g:,
      \ 'sphinx_doctrees_output_dirs',
      \ ['_build/doctrees', 'build/doctrees', '../_build/doctrees', '../build/doctrees',
      \  '_build/html/.doctrees', 'build/html/.doctrees', '../_build/html/.doctrees', '../build/html/.doctrees',
      \  '_build/dirhtml/.doctrees', 'build/dirhtml/.doctrees', '../_build/dirhtml/.doctrees', '../build/dirhtml/.doctrees']
      \)
let g:sphinx_include_intersphinx_data = get(g:, 'sphinx_include_intersphinx_data', 1)
let g:sphinx_always_use_scoped_targets = get(g:, 'sphinx_always_use_scoped_targets', 1)

let g:loaded_sphinx = 1
