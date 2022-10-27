; extends

;; Directives with nested content

((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#any-of?
  @_type
  "toctree"
  "versionadded" "versionchanged" "deprecated" "seealso" "centered" "hlist"
  "glossary"
  "index"
  "productionlist"))

((directive
   name: (type) @_type
   body: (body (arguments) @rst))
 (#any-of? @_type "sectionauthor" "codeauthor"))

;; Code highlight directives
((directive
   name: (type) @_type
   body: (body (arguments) @language (content) @content))
 (#eq? @_type "highlight"))

;; Most directives from domains accept nested content
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#match? @_type "^(py|c|cpp|js|rst):"))

((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#any-of? @_type "default-domain" "option" "envar" "program" "describe" "object"))

;; Directives from common extensions

;;; Sphinx docs
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#eq? @_type "confval"))

;;; sphinx-tabs
;;; https://github.com/executablebooks/sphinx-tabs
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#any-of? @_type "tabs" "tab" "group-tab"))

((directive
   name: (type) @_type
   body: (body (arguments) @language (content) @content))
 (#eq? @_type "code-tab"))

;;; http domain
;;; https://sphinxcontrib-httpdomain.readthedocs.io/
((directive
   name: (type) @_type
   body: (body (content) @rst))
 (#match? @_type "^(http):"))

((directive
   name: (type) @_type
   body: (body (arguments) @language (content) @content))
 (#eq? @_type "sourcecode"))

;;; sphinx-prompt
;;; https://github.com/sbrunner/sphinx-prompt
((directive
   name: (type) @_type
   body: (body (arguments) @language (content) @content))
 (#eq? @_type "prompt"))
