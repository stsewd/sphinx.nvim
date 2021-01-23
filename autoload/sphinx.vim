function! sphinx#execute(lines) abort
  " TODO: copy/insert/open link?
  " TODO: copy/insert name?
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
  "\ '--nth', '1',
  let l:fzf_options = [
        \ '--prompt', l:prompt,
        \ '--multi',
        \ '--expect', l:valid_keys,
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
