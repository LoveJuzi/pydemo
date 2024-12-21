#lang racket

; BASE ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (DISPATCH . args)
  (define table (make-hash))
  (define (call func . args)
    (apply (hash-ref table func) args))
  (define (add-item item) (hash-set! table (car item) (cdr item)))
  (define (build-table args)
    (cond ((eq? args '()) call)
          (else (add-item (car args))
                (build-table (cdr args)))))
  (build-table args))

(define (FACTORY)
  (define table (make-hash))
  (define (install tag func) (hash-set! table tag (lambda rest (apply func rest))))
  (define (make tag . args)
    (cond ((hash-has-key? table tag) (apply (hash-ref table tag) args))))
  (DISPATCH (cons 'install install)
            (cons 'make make)))

(define (TAGOBJ tag obj)
  (define (tag-name) tag)
  (define (object) obj)
  (DISPATCH (cons 'tag tag-name)
            (cons 'object object)))

(define (FUNCTABLES)
  (define (DISPATCHFUNC)
    (define func_table (make-hash))
    (define (install k v) (hash-set! func_table k v))
    (define (get k) (hash-ref func_table k))
    (DISPATCH (cons 'install install)
              (cons 'get get)))
  (define func_tables (make-hash))
  (define (install k1 k2 v)
    (cond 
      ((hash-has-key? func_tables k1) ((hash-ref func_tables k1) 'install k2 v))
      (else (hash-set! func_tables k1 (DISPATCHFUNC))
            (install k1 k2 v))))
  (define (get k1 k2) ((hash-ref func_tables k1) 'get k2))
  (DISPATCH (cons 'install install)
            (cons 'get get)))
          
(define (INSTALLFUNC tables)
  (lambda (k1 k2 v) (tables 'install k1 k2 v)))

(define (APPLYEXT func . args)
  (cond 
    ((pair? func) (apply (car func) (cdr func) args)) ; means object call
    (else (apply func args)))) ;means func call

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (EVAL exp env)
  (cond 
    ((number? exp) (EVAL (EXPRESSION 'LITERAL exp) env))
    ((string? exp) (EVAL (EXPRESSION 'LITERAL exp) env))
    ((symbol? exp) "symbol")
    ((list? exp)
     (cond
       ((eq? (car exp) 'quote) (EVAL (EXPRESSION 'SYMBOL (cadr exp)) env))
       ((eq? (car exp) 'lambda) (EVAL (EXPRESSION 'LAMBDA (cadr exp) (caddr exp)) env))
       ((eq? (car exp) 'begin) (EVAL (EXPRESSION 'BEGIN (cdr exp)) env))))
    (else (EXPRESSION_OP 'EVAL exp env))))
    

(define (APPLY procedure arguments)
  '())

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXPRESSION_OP
  ((lambda ()
     (define func_tables (FUNCTABLES))
     (define (get_exp_tag exp) (exp 'tag))
     (define (EVAL exp env)
       (APPLYEXT (func_tables 'get 'EVAL (get_exp_tag exp)) (exp 'obj) env))
     (DISPATCH (cons 'install-func (INSTALLFUNC func_tables))
               (cons 'EVAL EVAL)))))

(define (EXPRESSION tag . args)
  (define obj (apply EXPRESSION_FACTORY 'make tag args))
  (DISPATCH (cons 'tag (lambda () tag))
            (cons 'obj (lambda () obj))))

(define EXPRESSION_FACTORY (FACTORY))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_LITERAL_OP
  ((lambda ()
     (define (EVAL obj env)
       (obj 'literal))
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'LITERAL (cons EXP_LITERAL_OP 'EVAL))

(define (EXP_LITERAL literal)
  (DISPATCH (cons 'literal (lambda () literal))))

(EXPRESSION_FACTORY 'install 'LITERAL EXP_LITERAL)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_SYMBOL_OP
  ((lambda ()
     (define (EVAL obj env) 
       (obj 'symbol))
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'SYMBOL (cons EXP_SYMBOL_OP 'EVAL))

(define (EXP_SYMBOL symbol)
  (DISPATCH (cons 'symbol (lambda () symbol))))

(EXPRESSION_FACTORY 'install 'SYMBOL EXP_SYMBOL)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_LAMBDA_OP
  ((lambda ()
     (define (EVAL obj env)
       (CLOURSE (obj 'params) (obj 'body) env))
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'LAMBDA (cons EXP_LAMBDA_OP 'EVAL))

(define (EXP_LAMBDA params body)
  (DISPATCH (cons 'params (lambda () params))
            (cons 'body (lambda () body))))

(EXPRESSION_FACTORY 'install 'LAMBDA EXP_LAMBDA)

(define (CLOURSE params body env)
  (DISPATCH (cons 'params (lambda () params))
            (cons 'body (lambda () body))
            (cons 'env (lambda () env))))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_BEGIN_OP
  ((lambda ()
     (define (empty? exps) (null? exps))
     (define (first-exp exps) (car exps))
     (define (rest-exp exps) (cdr exps))
     (define (EVAL_EXP_IMPL exps env) 
       (cond
         ((empty? exps) '())
         ((empty? (rest-exp exps)) (EVAL (first-exp exps) env))
         (else (EVAL (first-exp exps) env)
               (EVAL_EXP_IMPL (rest-exp exps) env))))
     (define (EVAL_EXP obj env)
       (EVAL_EXP_IMPL (obj 'exps) env))
     (DISPATCH (cons 'EVAL EVAL_EXP)))))

(EXPRESSION_OP 'install-func 'EVAL 'BEGIN (cons EXP_BEGIN_OP 'EVAL))

(define (EXP_BEGIN exps)
  (DISPATCH (cons 'exps (lambda () exps))))

(EXPRESSION_FACTORY 'install 'BEGIN EXP_BEGIN)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_COND_OP
  ((lambda ()
     (define (EVAL obj env)
       '())
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'COND (cons EXP_COND_OP 'EVAL))

(define (EXP_COND seq)
  (DISPATCH (cons 'seq (lambda () seq))))

(EXPRESSION_FACTORY 'install 'COND EXP_COND)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(require rackunit)


(check-equal? (EXPRESSION_OP 'EVAL (EXPRESSION 'LITERAL 23) '()) 23)
(check-equal? (EXPRESSION_OP 'EVAL (EXPRESSION 'LITERAL "string") '()) "string")
(check-equal? (EXPRESSION_OP 'EVAL (EXPRESSION 'SYMBOL 'abc) '()) 'abc) 
(EVAL 23 '())
(EVAL "hello world" '())
(EVAL ''a '())

((EXP_LAMBDA '() '(1)) 'params)
((EXP_LAMBDA '() '(1)) 'body)

(((EXPRESSION 'LAMBDA '() '(1)) 'obj) 'params)
(((EXPRESSION 'LAMBDA '() '(1)) 'obj) 'body)

;(EVAL '(lambda () 1) '())
;(define input ''a)

(define input '(cond ((eq? 1 1) (+ 1 1) (+ 1 2))))
(car input)
(cadr input) ; first seq
(caadr input) ; pred
(cadadr input) ; seq

(define input2 '(begin 1 2 3))
(car input2)
(cdr input2)

(EVAL '(begin 1 2 3 "HELLO") '())

