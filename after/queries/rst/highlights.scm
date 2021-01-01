((role) @function.builtin
 (#match?
  @function.builtin
  ; https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html
  "^:(any|ref|doc|download|numref|envar|token|keyword|option|term|math|eq|abbr|command|dfn|file|guilabel|kbd|mailheader|makevar|manpage|menuselection|mimetype|newsgroup|program|regexp|samp|pep|rfc):$"))

((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  ; https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
  "^(toctree)|(versionadded|versionchanged|deprecated|seealso|centered|hlist)|(highlight|code-block|literalinclude)|(glossary)|(sectionauthor|codeauthor)|(index)|(only)|(tabularcolumns)|(productionlist)$"))

; https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#substitutions
; TODO: replace this with #match? when figure out how to make it work with `|`
((substitution_reference) @constant.builtin
 (#eq? @constant.builtin "|release|"))
((substitution_reference) @constant.builtin
 (#eq? @constant.builtin "|version|"))
((substitution_reference) @constant.builtin
 (#eq? @constant.builtin "|today|"))
