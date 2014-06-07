;require asdf
(require :asdf) ;(require 'asdf) (require "asdf") all CL inplementations accept except clisp (just accept "asdf")

;put shop2 in ~/experiment/shop2/ folder or in current path (not need (push))
(push "./shop2/" asdf:*central-registry*)
(asdf:oos 'asdf:load-op "shop2") 

(load "./basic") ;load shop2 domain, problem & plan which you define

;**add foo print in shop2.lisp for print out results**
