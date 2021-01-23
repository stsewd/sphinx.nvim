function! sphinx#execute(lines) abort
  if len(a:lines) <= 2
    return
  endif

  let l:key = a:lines[1]
  let l:line = a:lines[2]

  let l:name = split(l:line, '  ')[-2]
  let l:link = split(l:line, ' ')[-1]

  if l:key == 'enter'
    let l:item = l:name
  elseif l:key == 'ctrl-f'
    let l:item = l:link
  else
    return
  endif

  let @" = l:item
  echomsg 'Copied: ' . l:item
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

  let l:keybindings = ['enter', 'ctrl-f']
  let l:valid_keys = join(l:keybindings, ',')
  let l:fzf_options = [
        \ '--prompt', l:prompt,
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
