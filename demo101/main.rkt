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

(define (APPLYEXT func . args)
  (apply (car func) (cdr func) args))

(define (FUNCTABLE)
  (define func_table (make-hash))
  (define (install_func k v) (hash-set! func_table k v))
  (define (get_func k) (hash-ref func_table k))
  (DISPATCH (cons 'install install_func)
            (cons 'get get_func)))

(define (INSTALLFUNC table)
  (lambda (k v) (table 'install k v)))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (OPERATION tag)
  (define op (OPERATION_FACTORY 'make tag))
  (define (get_result args) (apply op 'get_result args))
  (DISPATCH (cons 'get_result get_result)))

(define OPERATION_FACTORY (FACTORY))

(define (OPERATION_ARGS)
  (define number1 1)
  (define number2 2)
  (define (set_number1 num) (set! number1 num))
  (define (set_number2 num) (set! number2 num))
  (define (get_op_type) (cons 'int 'int))
  (DISPATCH (cons 'number1 (lambda () number1))
            (cons 'number2 (lambda () number2))
            (cons 'set_number1 set_number1)
            (cons 'set_number2 set_number2)
            (cons 'get_op_type get_op_type)))

(define (OPERATION_ADD)
  (define (get_result tag . args) (apply (OPERATION_ADD_FACTORY 'make tag) args))
  (DISPATCH (cons 'get_result get_result)))

(define OPERATION_ADD_FACTORY (FACTORY))

(OPERATION_FACTORY 'install "+" OPERATION_ADD)

(define (OPERATION_SUB)
  (define (get_result args) (- (args 'number1) (args 'number2)))
  (DISPATCH (cons 'get_result get_result)))

(OPERATION_FACTORY 'install "-" OPERATION_SUB)

(define (OPERATION_ADD_RAT)
  (define (get_result rat1 rat2) '())
  (DISPATCH (cons 'get_result get_result)))

(OPERATION_ADD_FACTORY 'install (const 'RAT 'RAT) OPERATION_ADD_RAT)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(require rackunit)

(define ARGS (OPERATION_ARGS))
(ARGS 'set_number1 1)
(ARGS 'set_number2 2)

(define OP1 (OPERATION "+"))
(check-equal? (OP1 'get_result ARGS) 3)
(define OP2 (OPERATION "-"))
(check-equal? (OP2 'get_result ARGS) -1)

