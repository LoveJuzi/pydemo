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
    ((number? exp) (EXPRESSION_OP 'EVAL (EXPRESSION 'LITERAL exp) env))
    ((string? exp) (EXPRESSION_OP 'EVAL (EXPRESSION 'LITERAL exp) env))
    ((symbol? exp) (EXPRESSION_OP 'EVAL (EXPRESSION 'VAR exp) env))
    ((list? exp)
     (cond
       ((eq? (car exp) 'quote) 
        (EXPRESSION_OP 'EVAL (EXPRESSION 'SYMBOL (cadr exp)) env))
       ((eq? (car exp) 'lambda) 
        (EXPRESSION_OP 'EVAL (EXPRESSION 'LAMBDA (cadr exp) (caddr exp)) env))
       ((eq? (car exp) 'begin) 
        (EXPRESSION_OP 'EVAL (EXPRESSION 'BEGIN (cdr exp)) env))
       ((eq? (car exp) 'cond)
        (EXPRESSION_OP 'EVAL (EXPRESSION 'COND (cdr exp)) env))
       (else (EXPRESSION_OP 'EVAL (EXPRESSION 'APPLICATION (car exp) (cdr exp)) env))))
    (else (EXPRESSION_OP 'EVAL exp env))))

(define (APPLY procedure arguments)
  (PROCEDURE_OP 'APPLY procedure arguments))

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
(define EXP_VAR_OP
  ((lambda ()
     (define (EVAL obj env)
       (EXP_ENV_OP 'lookup_value (obj 'var) env))
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'VAR (cons EXP_VAR_OP 'EVAL))

(define (EXP_VAR var)
  (DISPATCH (cons 'var (lambda () var))))

(EXPRESSION_FACTORY 'install 'VAR EXP_VAR)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_ENV_OP
  ((lambda ()
     (define (lookup_value var env)
       (cond
         ((env 'has_var? var) (env 'get var))
         ((not (null? (env 'parent_env))) (lookup_value var (env 'parent_env)))
         (else (display "ERROR")
               '())))
     (define (list_of_values vars env)
       (cond
         ((null? vars) '())
         (else (cons (EVAL (car vars) env)
                     (list_of_values (cdr vars) env)))))
     (define (extend_enviroment params arguments env)
       (define newenv (EXP_ENV env))
       (define (add! params arguments)
         (cond 
           ((and (null? params) (null? arguments)) newenv)
           ((null? params) (display "ERROR") newenv)
           ((null? arguments) (display "ERROR") newenv)
           (else (newenv 'add! (car params) (car arguments))
                 (add! (cdr params) (cdr arguments)))))
       (add! params arguments))

     (DISPATCH (cons 'lookup_value lookup_value)
               (cons 'list_of_values list_of_values)
               (cons 'extend_enviroment extend_enviroment)))))

(define (EXP_ENV parent_env)
  (define var_table (make-hash))
  (define (add! var val) (hash-set! var_table var val))
  (define (has_var? var) (hash-has-key? var_table var))
  (define (get var) (hash-ref var_table var))
  (DISPATCH (cons 'add! add!)
            (cons 'get get)
            (cons 'has_var? has_var?)
            (cons 'parent_env (lambda () parent_env))))

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
       (PROCEDURE 'CLOURSE (obj 'params) (obj 'body) env))
     (DISPATCH (cons 'EVAL EVAL)))))

(EXPRESSION_OP 'install-func 'EVAL 'LAMBDA (cons EXP_LAMBDA_OP 'EVAL))

(define (EXP_LAMBDA params body)
  (DISPATCH (cons 'params (lambda () params))
            (cons 'body (lambda () body))))

(EXPRESSION_FACTORY 'install 'LAMBDA EXP_LAMBDA)

(define PROCEDURE_OP
  ((lambda ()
     (define func_tables (FUNCTABLES))
     (define (APPLY procedure arguments)
       (APPLYEXT (func_tables 'get 'APPLY (procedure 'tag)) (procedure 'obj) arguments))
     (DISPATCH (cons 'install-func (INSTALLFUNC func_tables))
               (cons 'APPLY APPLY)))))

(define (PROCEDURE tag . args)
  (define obj (apply PROCEDURE_FACTORY 'make tag args))
  (DISPATCH (cons 'tag (lambda () tag))
            (cons 'obj (lambda () obj))))

(define PROCEDURE_FACTORY (FACTORY))

(define PRIMITIVE_OP
  ((lambda ()
     (define (APPLY obj arguments) 
       (apply (obj 'name) arguments))
     (DISPATCH (cons 'APPLY APPLY)))))

(PROCEDURE_OP 'install-func 'APPLY 'PRIMITIVE (cons PRIMITIVE_OP 'APPLY))

(define (PRIMITIVE name)
  (DISPATCH (cons 'name (lambda () name))))

(PROCEDURE_FACTORY 'install 'PRIMITIVE PRIMITIVE)

(define CLOURSE_OP
  ((lambda ()
     (define (APPLY obj arguments) 
       (EVAL (obj 'body) 
             (EXP_ENV_OP 'extend_enviroment 
                         (obj 'params) 
                         arguments 
                         (obj 'env))))
     (DISPATCH (cons 'APPLY APPLY)))))

(PROCEDURE_OP 'install-func 'APPLY 'CLOURSE (cons CLOURSE_OP 'APPLY))

(define (CLOURSE params body env)
  (DISPATCH (cons 'params (lambda () params))
            (cons 'body (lambda () body))
            (cons 'env (lambda () env))))

(PROCEDURE_FACTORY 'install 'CLOURSE CLOURSE)

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
     (define (EVAL_COND obj env)
       (cond 
         ((obj 'empty?) '())
         ((eq? (obj 'predicate) 'else)
          (EXPRESSION_OP 'EVAL (EXPRESSION 'BEGIN (obj 'exps)) env))
         ((EVAL (obj 'predicate) env)
          (EXPRESSION_OP 'EVAL (EXPRESSION 'BEGIN (obj 'exps)) env))
         (else (EVAL_COND (obj 'rest_conds) env))))
     (DISPATCH (cons 'EVAL EVAL_COND)))))

(EXPRESSION_OP 'install-func 'EVAL 'COND (cons EXP_COND_OP 'EVAL))

(define (EXP_COND conds)
  (define (empty?) (null? conds))
  (define (predicate) (caar conds))
  (define (exps) (cdar conds))
  (define (rest_conds) (EXP_COND (cdr conds)))
  (DISPATCH (cons 'empty? empty?)
            (cons 'predicate predicate)
            (cons 'exps exps)
            (cons 'rest_conds rest_conds)))

(EXPRESSION_FACTORY 'install 'COND EXP_COND)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_APPLICATION_OP
  ((lambda ()
     (define (EVAL_OBJ obj env)
       (APPLY (EVAL (obj 'operator) env) (EXP_ENV_OP 'list_of_values (obj 'operands) env)))
     (DISPATCH (cons 'EVAL EVAL_OBJ)))))

(EXPRESSION_OP 'install-func 'EVAL 'APPLICATION (cons EXP_APPLICATION_OP 'EVAL))

(define (EXP_APPLICATION operator operands)
  (DISPATCH (cons 'operator (lambda () operator))
            (cons 'operands (lambda () operands))))

(EXPRESSION_FACTORY 'install 'APPLICATION EXP_APPLICATION)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define EXP_GLOBAL_ENV
  ((lambda ()
     (define env (EXP_ENV '()))
     (begin
       (env 'add! '+ (PROCEDURE 'PRIMITIVE +))
       (env 'add! '- (PROCEDURE 'PRIMITIVE -))
       (env 'add! '* (PROCEDURE 'PRIMITIVE *))
       (env 'add! '/ (PROCEDURE 'PRIMITIVE /))
       (env 'add! 'cons (PROCEDURE 'PRIMITIVE cons))
       (env 'add! 'car (PROCEDURE 'PRIMITIVE car))
       (env 'add! 'cdr (PROCEDURE 'PRIMITIVE cdr))
       (env 'add! 'eq? (PROCEDURE 'PRIMITIVE eq?))
       env))))

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

(define input2 '(begin 1 2 3))
(car input2)
(cdr input2)

(check-equal? (EVAL '(begin 1 2 3 "HELLO") '()) "HELLO")

(define testenv (EXP_ENV '()))

(testenv 'add! 'a "HELLO WORLD")
(testenv 'has_var? 'a)
(testenv 'get 'a)
(EXP_ENV_OP 'lookup_value 'a testenv)
(EVAL 'a testenv)

(define input '(cond ((eq? 1 1) (+ 1 1) (+ 1 2))))
(car input)
(cadr input) ; first seq
(caadr input) ; pred
(cdadr input) ; begin
(cadadr input) ; seq

(define input3 '(begin (+ 1 2) (+ 3 4)))
(car input3)
(cdr input3)

;(APPLY + '(2 3))
;(apply + '(2 3))

(define input4 '(+ 2 3))
(car input4)
(cdr input4)

;(define env (EXP_ENV '()))
;(env 'add! '+ +) 
;
;;(EVAL '(+ 1 2) env)
;;(EVAL '+ env)
;;(EVAL (EVAL '+ env) '(1 2))
;;(EVAL '(+ 1 2) env)
;
;;(APPLY (EVAL '+ env) '(10 20))
;
;;(EXP_APPLICATION_OP 'EVAL (EXP_APPLICATION '+ '(1 2)) env)
;
;(EVAL ((EXP_APPLICATION '+ '(1 2)) 'operator) env)
;;((EXP_APPLICATION '+ '(1 2)) 'operands)
;(EXP_ENV_OP 'list_of_values ((EXP_APPLICATION '+ '(1 2)) 'operands) env)
;
;;(apply (EVAL ((EXP_APPLICATION '+ '(1 2)) 'operator) env) (EXP_ENV_OP 'list_of_values ((EXP_APPLICATION '+ '(1 2)) 'operands) env))
;
;;(APPLY (EVAL ((EXP_APPLICATION '+ '(1 2)) 'operator) env) (EXP_ENV_OP 'list_of_values ((EXP_APPLICATION '+ '(1 2)) 'operands) env))
;
;(define obj (EXP_APPLICATION '+ '(1 2)))
;(obj 'operator)
;(obj 'operands)
;(EVAL (obj 'operator) env)
;(EXP_ENV_OP 'list_of_values (obj 'operands) env)
;;(APPLY (EVAL (obj 'operator) env) (EXP_ENV_OP 'list_of_values (obj 'operands) env))
;
;;(define (EVAL2 obj env)
;;  (APPLY (EVAL (obj 'operator) env) (EXP_ENV_OP 'list_of_values (obj 'operands) env)))
;;(EVAL2  obj env)
;
;;(EXP_APPLICATION_OP 'EVAL obj env)
;;(EXP_APPLICATION_OP 'EVAL obj env)

(define env (EXP_ENV '()))

(env 'add! '+ (PROCEDURE 'PRIMITIVE +))

(PRIMITIVE_OP 'APPLY (PROCEDURE_FACTORY 'make 'PRIMITIVE +) '(2 3 4))

(PROCEDURE_OP 'APPLY (PROCEDURE 'PRIMITIVE +) '(2 3 4))

(APPLY (PROCEDURE 'PRIMITIVE +) '(2 3 4))

(EVAL '+ env)

(APPLY (EVAL '+ env) '(2 3 4))
(EXP_APPLICATION_OP 'EVAL (EXP_APPLICATION '+ '(2 3)) env)

;(EVAL '(+ 1 2) env)
(EVAL '(+ 1 2) EXP_GLOBAL_ENV)
(EVAL '(- 1 2) EXP_GLOBAL_ENV)

;(EXP_GLOBAL_ENV 'get '+)

(define env2 (EXP_ENV_OP 'extend_enviroment '(add) '("add") EXP_GLOBAL_ENV))
env2

(env2 'has_var? '-)
(not (null? (env2 'parent_env)))

;(EXP_ENV_OP 'lookup_value '+ env2)

(env2 'has_var? '-) ;(env2 'get '-)

(not (null? (env2 'parent_env)))

(EXP_ENV_OP 'lookup_value '- (env2 'parent_env))

(EXP_ENV_OP 'lookup_value '- env2)

;(env2 'has_var? 'add)
;(env2 'add! 'add "add")
;(env2 'get 'add)
;((env2 'parent_env) 'get '+)
;(EXP_ENV_OP 'lookup_value 'add env2)
;(EXP_ENV_OP 'lookup_value '+ env2)
;(EXP_ENV_OP 'lookup_value '- env2)
;(EXP_ENV_OP 'lookup_value 'add env2)

(define clourse (CLOURSE '(a b) '(+ a b) EXP_GLOBAL_ENV))

(CLOURSE_OP 'APPLY clourse '(1 2))

(EVAL '((lambda (a b) (+ a b)) 1 2) EXP_GLOBAL_ENV)

;(EVAL '(cond ((eq? 1 1) 1) (else 2)) EXP_GLOBAL_ENV) 

(define condexp '(cond ((eq? 1 1) 1 2 3) (else 2)))

((EXP_COND (cdr condexp)) 'predicate)

((EXP_COND (cdr condexp)) 'exps)
(((EXP_COND (cdr condexp)) 'rest_conds) 'predicate)
(((EXP_COND (cdr condexp)) 'rest_conds) 'exps)

(define condobj (EXP_COND (cdr condexp)))

(EVAL (condobj 'predicate) EXP_GLOBAL_ENV)

;(EVAL condexp EXP_GLOBAL_ENV) 

(EXPRESSION_OP 'EVAL (EXPRESSION 'COND (cdr condexp)) EXP_GLOBAL_ENV)
;(((EXPRESSION 'COND (cdr condexp)) 'obj) 'predicate)
;(((EXPRESSION 'COND (cdr condexp)) 'obj) 'empty?)
;(EVAL (((EXPRESSION 'COND (cdr condexp)) 'obj) 'predicate) EXP_GLOBAL_ENV)

(define input-prompt ";;; M-Eval input:")
(define output-prompt ";;; M-Eval output")
(define (driver-loop)
  (prompt-for-input input-prompt)
  (define input (read))
  (define output (EVAL input EXP_GLOBAL_ENV))
  (begin
    (annouce-output output-prompt)
    (display output)
    (driver-loop)))

(define (newline) (display "\n"))

(define (prompt-for-input string)
  (newline) (newline) (display string) (newline))

(define (annouce-output string)
  (newline) (display string) (newline))
  
;(driver-loop)
