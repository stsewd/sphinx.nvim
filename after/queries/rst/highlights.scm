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

; Python domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^py:(module|currentmodule|function|data|exception|class|attribute|method|staticmethod|classmethod|decorator|decoratormethod)$"))

((role) @function.builtin
 (#match?
  @function.builtin
  "^:py:(mod|func|data|const|class|meth|attr|exc|obj):$"))

; C Domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-c-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^c:(member|var|function|macro|struct|union|enum|enumerator|type|alias|namespace|namespace-push|namespace-pop)$"))

((role) @function.builtin
 (#match?
  @function.builtin
  "^:c:(member|data|var|func|macro|struct|union|enum|enumerator|type|expr|texpr):$"))

; Cpp domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^cpp:(class|struct|function|member|var|type|enum|enum-struct|enum-class|enumerator|union|concept|alias|namespace|namespace-push|namespace-pop|)$"))

((role) @function.builtin
 (#match?
  @function.builtin
  "^:cpp:(expr|texpr|any|class|struct|func|member|var|type|concept|enum|enumerator):$"))

; Standard domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-standard-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^(default-domain|option|envar|program|describe|object|)$"))

; JavaScript domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-javascript-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^js:(module|function|method|class|data|attribute)$"))

((role) @function.builtin
 (#match?
  @function.builtin
  "^:js:(mod|func|meth|class|data|attr):$"))

; reStructuredtext domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-restructuredtext-domain
((directive
   name: (type) @function.builtin)
 (#match?
  @function.builtin
  "^rst:(directive|directive:option|role)$"))

((role) @function.builtin
 (#match?
  @function.builtin
  "^:rst:(dir|role):$"))

; Math domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-math-domain
((role) @function.builtin
 (#match?
  @function.builtin
  "^:math:(numref):$"))
