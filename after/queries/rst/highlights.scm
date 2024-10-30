; extends

((role) @function.builtin
 (#any-of?
  @function.builtin
  ; https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html
  ":any:" ":ref:" ":doc:" ":download:" ":numref:" ":envar:" ":token:" ":keyword:" ":option:"
  ":term:" ":math:" ":eq:" ":abbr:" ":command:" ":dfn:" ":file:" ":guilabel:" ":kbd:" ":mailheader:"
  ":makevar:" ":manpage:" ":menuselection:" ":mimetype:" ":newsgroup:" ":program:" ":regexp:" ":samp:"
  ":pep:" ":rfc:"))

((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  ; https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
  "toctree"
  "versionadded" "versionchanged" "deprecated" "seealso" "centered" "hlist"
  "highlight" "code-block" "literalinclude"
  "glossary"
  "sectionauthor" "codeauthor"
  "index"
  "only"
  "tabularcolumns"
  "productionlist"))

; https://www.sphinx-doc.org/en/master/usage/restructuredtext/roles.html#substitutions
((substitution_reference) @constant.builtin
 (#any-of? @constant.builtin "|release|" "|version|" "|today|"))

; Python domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "py:module"
  "py:currentmodule"
  "py:function"
  "py:data"
  "py:exception"
  "py:class"
  "py:attribute"
  "py:method"
  "py:staticmethod"
  "py:classmethod"
  "py:decorator"
  "py:decoratormethod"))

((role) @function.builtin
 (#any-of?
  @function.builtin
  ":py:mod:"
  ":py:func:"
  ":py:data:"
  ":py:const:"
  ":py:class:"
  ":py:meth:"
  ":py:attr:"
  ":py:exc:"
  ":py:obj:"))

; C Domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-c-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "c:member"
  "c:var"
  "c:function"
  "c:macro"
  "c:struct"
  "c:union"
  "c:enum"
  "c:enumerator"
  "c:type"
  "c:alias"
  "c:namespace"
  "c:namespace-push"
  "c:namespace-pop"))

((role) @function.builtin
 (#any-of?
  @function.builtin
  ":c:member:"
  ":c:data:"
  ":c:var:"
  ":c:func:"
  ":c:macro:"
  ":c:struct:"
  ":c:union:"
  ":c:enum:"
  ":c:enumerator:"
  ":c:type:"
  ":c:expr:"
  ":c:texpr:"))

; C++ domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#cpp-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "cpp:class"
  "cpp:struct"
  "cpp:function"
  "cpp:member"
  "cpp:var"
  "cpp:type"
  "cpp:enum"
  "cpp:enum-struct"
  "cpp:enum-class"
  "cpp:enumerator"
  "cpp:union"
  "cpp:concept"
  "cpp:alias"
  "cpp:namespace"
  "cpp:namespace-push"
  "cpp:namespace-pop"))

((role) @function.builtin
 (#any-of?
  @function.builtin
  ":cpp:expr:"
  ":cpp:texpr:"
  ":cpp:any:"
  ":cpp:class:"
  ":cpp:struct:"
  ":cpp:func:"
  ":cpp:member:"
  ":cpp:var:"
  ":cpp:type:"
  ":cpp:concept:"
  ":cpp:enum:"
  ":cpp:enumerator:"))

; Standard domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-standard-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "default-domain"
  "option"
  "envar"
  "program"
  "describe"
  "object"))

; JavaScript domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-javascript-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "js:module"
  "js:function"
  "js:method"
  "js:class"
  "js:data"
  "js:attribute"))

((role) @function.builtin
 (#any-of?
  @function.builtin
  ":js:mod:"
  ":js:func:"
  ":js:meth:"
  ":js:class:"
  ":js:data:"
  ":js:attr:"))

; reStructuredtext domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-restructuredtext-domain
((directive
   name: (type) @function.builtin)
 (#any-of?
  @function.builtin
  "rst:directive"
  "rst:directive:option"
  "rst:role"))

((role) @function.builtin
 (#any-of?
  @function.builtin
  ":rst:dir:"
  ":rst:role:"))

; Math domain
; https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-math-domain
((role) @function.builtin
 (#eq?
  @function.builtin
  ":math:numref:"))

; sphinxnotes-strike
; https://sphinx.silverrainz.me/strike/
((interpreted_text
  (role) @_role
  "interpreted_text" @markup.strikethrough)
  (#any-of?
   @_role
   ":del:" ":strike:"))
