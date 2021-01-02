;; Directives with nested content

((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#match?
  @_type
  "^(toctree)|(versionadded|versionchanged|deprecated|seealso|centered|hlist)|(glossary)|(index)|(productionlist)$"))

((directive
   name: (type) @_type
   body: (body (arguments) @rst))
 (#match? @_type "^(sectionauthor|codeauthor)$"))

;; Code highlight directives
((directive
   name: (type) @_type
   body: (body (arguments) @language (content) @content))
 (#match? @_type "^(highlight|code-block)$"))

;; Most directives from domains accept nested content
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#match? @_type "^(py|c|cpp|js|rst):$"))
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#match? @_type "^(default-domain|option|envar|program|describe|object)$"))
