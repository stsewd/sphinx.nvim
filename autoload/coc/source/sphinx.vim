function! coc#source#sphinx#init() abort
  return {
        \ 'priority': 1,
        \ 'shortcut': 'Sphinx',
        \ 'filtypes': ['rst'],
        \ 'triggerCharacters': ['`', '<'],
        \}
endfunction

function! coc#source#sphinx#complete(opt, cb) abort
  let l:items = CocSphinxList(a:opt)
  call a:cb(l:items)
endfunction
