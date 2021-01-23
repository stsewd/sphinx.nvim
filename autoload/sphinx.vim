function! sphinx#execute(lines) abort
  " TODO: copy link?
  " TODO: copy name?
  echomsg a:lines
endfunction


function! sphinx#list(bang, role) abort
  let l:role = trim(a:role)

  let l:prompt = 'Sphinx> '
  if !empty(l:role)
    let l:prompt = 'Sphinx > ' . l:role . '> '
  endif

  let l:results = FzfSphinxList(l:role)
  " For some reason some times the first call returns null
  if type(l:results) == type(v:null)
    let l:results = FzfSphinxList(l:role)
  endif

  let l:keybindings = ['enter']
  let l:valid_keys = join(l:keybindings, ',')
  let l:fzf_options = [
        \ '--prompt', l:prompt,
        \ '--multi',
        \ '--expect', l:valid_keys,
        \ '--nth', '..-3',
        \ '--ansi',
        \ '--print-query',
        \]
  call fzf#run(fzf#wrap(
        \ 'Sphinx',
        \ {
        \   'source': l:results,
        \   'sink*': function('sphinx#execute'),
        \   'options': l:fzf_options,
        \ },
        \ a:bang,
        \))
endfunction


function! sphinx#complete_roles(arglead, cmdline, cursorpos) abort
  let l:cmdlist = split(a:cmdline)
  if len(l:cmdlist) > 2 || len(l:cmdlist) > 1 && empty(a:arglead)
    return ''
  endif

  let l:results =  SphinxRoles()
  " For some reason some times the first call returns null
  if type(l:results) == type(v:null)
    let l:results = SphinxRoles()
  endif
  return join(l:results, "\n")
endfunction
