;; Directives with nested content

((directive
   name: (type) @_type
   body: (body) @rst)
 (#match?
  @_type
  "^(toctree)|(versionadded|versionchanged|deprecated|seealso|centered|hlist)|(literalinclude)|(glossary)|(sectionauthor|codeauthor)|(index)|(only)|(tabularcolumns)|(productionlist)$"))

;; Special directives
;; TODO: using @language and @content on the same capture raises an error.
;; ((directive
;;    name: (type) @_type
;;    body: (body) @language @content)
;;  (#eq? @_type "highlight"))

;; TODO: using @language and @content on the same capture raises an error.
;; ((directive
;;    name: (type) @_type
;;    body: (body) @language @content)
;;  (#eq? @_type "code-block"))
