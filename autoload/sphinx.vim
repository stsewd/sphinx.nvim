" # SphinxRefs

function! sphinx#copy_ref(lines) abort
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


function! sphinx#list_refs(bang, role) abort
  let l:role = trim(a:role)

  let l:prompt = 'SphinxRefs> '
  if !empty(l:role)
    let l:prompt .= l:role . '> '
  endif

  let l:results = SphinxListRefs(l:role)
  " For some reason some times the first call returns null
  if type(l:results) == type(v:null)
    let l:results = SphinxListRefs(l:role)
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
        \ 'SphinxRefs',
        \ {
        \   'source': l:results,
        \   'sink*': function('sphinx#copy_ref'),
        \   'options': l:fzf_options,
        \ },
        \ a:bang,
        \))
endfunction


function! sphinx#complete_ref_roles(arglead, cmdline, cursorpos) abort
  let l:cmdlist = split(a:cmdline)
  if len(l:cmdlist) > 2 || len(l:cmdlist) > 1 && empty(a:arglead)
    return ''
  endif

  let l:results =  SphinxRefRoles()
  " For some reason some times the first call returns null
  if type(l:results) == type(v:null)
    let l:results = SphinxRefRoles()
  endif
  return join(l:results, "\n")
endfunction


" # SphinxFiles

function! sphinx#open_file(lines) abort
  if len(a:lines) <= 2
    return
  endif

  let l:key = a:lines[1]
  let l:files = map(a:lines[2:], 'split(v:val)[-1]')
  for l:file in l:files
    execute 'edit ' . l:file
  endfor
endfunction


function! sphinx#list_files(bang) abort
  let l:prompt = 'SphinxFiles> '

  let l:results = SphinxListFiles()
  " For some reason some times the first call returns null
  if type(l:results) == type(v:null)
    let l:results = SphinxListFiles()
  endif

  let l:keybindings = ['enter']
  let l:valid_keys = join(l:keybindings, ',')
  let l:fzf_options = [
        \ '--prompt', l:prompt,
        \ '--expect', l:valid_keys,
        \ '--multi',
        \ '--ansi',
        \ '--nth', '..-3,-1',
        \ '--print-query',
        \]
  call fzf#run(fzf#wrap(
        \ 'SphinxFiles',
        \ {
        \   'source': l:results,
        \   'sink*': function('sphinx#open_file'),
        \   'options': l:fzf_options,
        \ },
        \ a:bang,
        \))
endfunction
