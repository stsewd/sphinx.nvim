; extends

;; Directives with nested content

((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#any-of?
  @_type
  "toctree"
  "versionadded" "versionchanged" "deprecated" "seealso" "centered" "hlist"
  "glossary"
  "index"
  "productionlist")
 (#set! injection.language "rst"))

((directive
   name: (type) @_type
   body: (body (arguments) @injection.content))
 (#any-of? @_type "sectionauthor" "codeauthor")
 (#set! injection.language "rst"))

;; Code highlight directives
((directive
   name: (type) @_type
   body: (body (arguments) @injection.language (content) @injection.content))
 (#eq? @_type "highlight"))

;; Most directives from domains accept nested content
((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#match? @_type "^(py|c|cpp|js|rst):")
 (#set! injection.language "rst"))

((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#any-of? @_type "default-domain" "option" "envar" "program" "describe" "object")
 (#set! injection.language "rst"))

;; Directives from common extensions

;;; Sphinx docs
((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#eq? @_type "confval")
 (#set! injection.language "rst"))

;;; sphinx-tabs
;;; https://github.com/executablebooks/sphinx-tabs
((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#any-of? @_type "tabs" "tab" "group-tab")
 (#set! injection.language "rst"))

((directive
   name: (type) @_type
   body: (body (arguments) @injection.language (content) @injection.content))
 (#eq? @_type "code-tab"))

;;; http domain
;;; https://sphinxcontrib-httpdomain.readthedocs.io/
((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#match? @_type "^(http):")
 (#set! injection.language "rst"))

((directive
   name: (type) @_type
   body: (body (arguments) @injection.language (content) @injection.content))
 (#eq? @_type "sourcecode"))

;;; sphinx-prompt
;;; https://github.com/sbrunner/sphinx-prompt
((directive
   name: (type) @_type
   body: (body (arguments) @injection.language (content) @injection.content))
 (#eq? @_type "prompt"))

;;; sphinx-design
;;; https://sphinx-design.readthedocs.io/
((directive
   name: (type) @_type
   body: (body (content) @injection.content))
 (#any-of?
  @_type
  "grid" "grid-item" "grid-item-card"
  "card" "card-carousel"
  "dropdown"
  "tabset" "tab-set-code" "tab-item")
 (#set! injection.language "rst"))
