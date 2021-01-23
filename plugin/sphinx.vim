if exists('g:loaded_sphinx')
  finish
endif

let g:sphinx_default_role = get(g:, 'sphinx_default_role', 'any')
let g:sphinx_default_dirs = get(g:, 'sphinx_default_dirs', 1)
let s:default_html_output_dirs = [
      \ '_build/html', 'build/html',
      \ '../_build/html', '../build/html',
      \ '_build/dirhtml', 'build/dirhtml',
      \ '../_build/dirhtml', '../build/dirhtml',
      \]
let s:default_doctrees_output_dirs = [
      \ '_build/doctrees', 'build/doctrees',
      \ '../_build/doctrees', '../build/doctrees',
      \ '_build/html/.doctrees', 'build/html/.doctrees',
      \ '../_build/html/.doctrees', '../build/html/.doctrees',
      \ '_build/dirhtml/.doctrees', 'build/dirhtml/.doctrees',
      \ '../_build/dirhtml/.doctrees', '../build/dirhtml/.doctrees',
      \]

let g:sphinx_html_output_dirs = get(g:, 'sphinx_html_output_dirs', [])
let g:sphinx_doctrees_output_dirs = get(g:, 'sphinx_doctrees_output_dirs', [])

if g:sphinx_default_dirs
  call extend(g:sphinx_html_output_dirs, s:default_html_output_dirs)
  call extend(g:sphinx_doctrees_output_dirs, s:default_doctrees_output_dirs)
endif

let g:sphinx_include_intersphinx_data = get(g:, 'sphinx_include_intersphinx_data', 1)
let g:sphinx_always_use_scoped_targets = get(g:, 'sphinx_always_use_scoped_targets', 1)

" FZF integration
let s:prefix = get(g:, 'fzf_command_prefix', '')
let s:command = s:prefix . 'Sphinx'
execute 'command! -bang -nargs=? -complete=custom,sphinx#complete_roles ' . s:command . ' call sphinx#list(<bang>0, <q-args>)'


let g:loaded_sphinx = 1
