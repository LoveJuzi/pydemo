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

(define ARITHMETIC_OP
  ((lambda ()
     (define func_tables (FUNCTABLES))
     (define (get_op_type ari1 ari2)
       (cons (ari1 'tag) (ari2 'tag)))
     (define (add ari1 ari2) 
       (TAGOBJ (ari1 'tag)
               (APPLYEXT (func_tables 'get 'add (get_op_type ari1 ari2)) 
                         (ari1 'object)
                         (ari2 'object))))
     (define (sub ari1 ari2)
       (TAGOBJ (ari1 'tag)
               (APPLYEXT (func_tables 'get 'sub (get_op_type ari1 ari2))
                         (ari1 'object)
                         (ari2 'object))))
     (define (mul ari1 ari2)
       (TAGOBJ (ari1 'tag)
               (APPLYEXT (func_tables 'get 'mul (get_op_type ari1 ari2))
                         (ari1 'object)
                         (ari2 'object))))
     (define (div ari1 ari2)
       (TAGOBJ (ari1 'tag)
               (APPLYEXT (func_tables 'get 'div (get_op_type ari1 ari2))
                         (ari1 'object)
                         (ari2 'object))))
     (define (equal ari1 ari2)
       (APPLYEXT (func_tables 'get 'equal (get_op_type ari1 ari2))
                 (ari1 'object)
                 (ari2 'object)))
     (DISPATCH (cons 'install-func (INSTALLFUNC func_tables))
               (cons 'add add)
               (cons 'sub sub)
               (cons 'mul mul)
               (cons 'div div)
               (cons 'equal equal)))))

(define (ARITHMETIC tag . args)
  (define obj (apply ARITHMETIC_FACTORY 'make tag args))
  (TAGOBJ tag obj))

(define ARITHMETIC_FACTORY (FACTORY))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define INTEGER_OP
  ((lambda ()
     (define (add num1 num2) (INTEGER (+ (num1 'val) (num2 'val))))
     (define (sub num1 num2) (INTEGER (- (num1 'val) (num2 'val))))
     (define (mul num1 num2) (INTEGER (* (num1 'val) (num2 'val))))
     (define (div num1 num2) (INTEGER (/ (num1 'val) (num2 'val))))
     (define (equal num1 num2) (= (num1 'val) (num2 'val)))
     (DISPATCH (cons '+ add)
               (cons '- sub)
               (cons '* mul)
               (cons '/ div)
               (cons '= equal)))))

(ARITHMETIC_OP 'install-func 'add (cons 'INTEGER 'INTEGER) (cons INTEGER_OP '+))
(ARITHMETIC_OP 'install-func 'sub (cons 'INTEGER 'INTEGER) (cons INTEGER_OP '-))
(ARITHMETIC_OP 'install-func 'mul (cons 'INTEGER 'INTEGER) (cons INTEGER_OP '*))
(ARITHMETIC_OP 'install-func 'div (cons 'INTEGER 'INTEGER) (cons INTEGER_OP '/))
(ARITHMETIC_OP 'install-func 'equal (cons 'INTEGER 'INTEGER) (cons INTEGER_OP '=))

(define (INTEGER num)
  (DISPATCH (cons 'val (lambda () num))))

(ARITHMETIC_FACTORY 'install 'INTEGER INTEGER)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define RAT_OP
  ((lambda ()
    (define (add rat1 rat2)
      (RAT (+ (* (rat1 'numer) (rat2 'denom))
              (* (rat1 'denom) (rat2 'numer)))
           (* (rat1 'denom) (rat2 'denom))))
    (define (sub rat1 rat2)
      (RAT (- (* (rat1 'numer) (rat2 'denom))
              (* (rat1 'denom) (rat2 'numer)))
           (* (rat1 'denom) (rat2 'denom))))
    (define (mul rat1 rat2)
      (RAT (* (rat1 'numer) (rat2 'numer))
           (* (rat1 'denom) (rat2 'denom))))
    (define (div rat1 rat2)
      (RAT (* (rat1 'numer) (rat2 'denom))
           (* (rat1 'denom) (rat2 'numer))))
    (define (equal rat1 rat2)
      (= (* (rat1 'numer) (rat2 'denom))
         (* (rat1 'denom) (rat2 'numer))))
    (DISPATCH (cons '+ add) 
              (cons '- sub)
              (cons '* mul) 
              (cons '/ div) 
              (cons '= equal)))))

(ARITHMETIC_OP 'install-func 'add (cons 'RAT 'RAT) (cons RAT_OP '+))
(ARITHMETIC_OP 'install-func 'sub (cons 'RAT 'RAT) (cons RAT_OP '-))
(ARITHMETIC_OP 'install-func 'mul (cons 'RAT 'RAT) (cons RAT_OP '*))
(ARITHMETIC_OP 'install-func 'div (cons 'RAT 'RAT) (cons RAT_OP '/))
(ARITHMETIC_OP 'install-func 'equal (cons 'RAT 'RAT) (cons RAT_OP '=))

(define (RAT n d)
  (define rat (cons n d))
  (define (numer) (car rat))
  (define (denom) (cdr rat))
  (define (dispatch op . args)
    (cond ((eq? op 'numer) (apply numer args))
      ((eq? op 'denom) (apply denom args))))
  dispatch)

(ARITHMETIC_FACTORY 'install 'RAT RAT)


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define COMPLEX_OP
  ((lambda ()
     (define (equal z1 z2)
       (and (= (z1 'real_part) (z2 'real_part))
            (= (z1 'imag_part) (z2 'imag_part))))
     (DISPATCH (cons 'equal equal)))))


(define (COMPLEX tag . args)
  (define complex (apply COMPLEX_FACTORY 'make tag args))
  (define (real_part) (complex 'real_part))
  (define (imag_part) (complex 'imag_part))
  (define (magnitude_part) (complex 'magnitude))
  (define (angle_part) (complex 'angle))
  (DISPATCH (cons 'real_part real_part)
            (cons 'imag_part imag_part)
            (cons 'magnitude magnitude_part)
            (cons 'angle angle_part)))

(ARITHMETIC_FACTORY 'install 'COMPLEX COMPLEX)

(define COMPLEX_FACTORY (FACTORY))

(define (COMPLEX_RECTANGULAR x y)
  (define complex (cons x y))
  (define (real_part) (car complex))
  (define (imag_part) (cdr complex))
  (define (magnitude_part)
    (sqrt (+ (* (real_part) (real_part))
             (* (imag_part) (imag_part)))))
  (define (angle_part)
    (atan (imag_part) (real_part)))
  (DISPATCH (cons 'real_part real_part)
            (cons 'imag_part imag_part)
            (cons 'magnitude magnitude_part)
            (cons 'angle angle_part)))

(COMPLEX_FACTORY 'install 'RECTANGULAR COMPLEX_RECTANGULAR)

(define (COMPLEX_POLAR x y)
  (define complex (cons x y))
  (define (real_part)
    (* (magnitude_part) (cos (angle_part))))
  (define (imag_part)
    (* (magnitude_part) (sin (angle_part))))
  (define (magnitude_part) (car complex)) 
  (define (angle_part) (cdr complex))
  (DISPATCH (cons 'real_part real_part)
            (cons 'imag_part imag_part)
            (cons 'magnitude magnitude_part)
            (cons 'angle angle_part)))

(COMPLEX_FACTORY 'install 'POLAR COMPLEX_POLAR)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(require rackunit)

(check-equal? ((RAT 1 2) 'numer) 1)

(check-true (RAT_OP '= (RAT_OP '+ (RAT 1 2) (RAT 1 2)) (RAT 1 1)))

(define complex1 (COMPLEX 'RECTANGULAR 1 2))
(define complex2 (COMPLEX 'RECTANGULAR 1 2))

(check-true (COMPLEX_OP 'equal complex1 complex2))

(define complex3 (COMPLEX 'POLAR 1 2))
(define complex4 (COMPLEX 'POLAR 1 3))
(check-true (COMPLEX_OP 'equal complex3 complex3))
;(complex3 'real_part)
;(complex3 'imag_part)
(check-false (COMPLEX_OP 'equal complex3 complex4))

(define rat1 (ARITHMETIC_FACTORY 'make 'RAT 1 2))
(define rat2 (ARITHMETIC_FACTORY 'make 'RAT 1 2))
(check-true (RAT_OP '= rat1 rat2))

(define ari1 (ARITHMETIC 'RAT 1 2))
(define ari2 (ARITHMETIC 'RAT 1 2))

(ari1 'tag)
(ari1 'object)

(ari2 'tag)
(ari2 'object)

(ARITHMETIC_OP 'add ari1 ari2)

((ARITHMETIC_OP 'add ari1 ari2) 'tag)
(((ARITHMETIC_OP 'add ari1 ari2) 'object) 'numer)
(((ARITHMETIC_OP 'add ari1 ari2) 'object) 'denom)

(ARITHMETIC_OP 'equal
               (ARITHMETIC_OP 'mul (ARITHMETIC 'INTEGER 3) (ARITHMETIC 'INTEGER 3))
               (ARITHMETIC 'INTEGER 9))

(ARITHMETIC_OP 'equal
               (ARITHMETIC 'INTEGER 3)
               (ARITHMETIC 'INTEGER 9))

(INTEGER_OP '= (INTEGER 3) (INTEGER 3))

(ARITHMETIC_OP 'add 1 2)


;check-equal?: 检查两个值是否相等。
;check-true / check-false: 检查表达式是否为真/假。
;check-< / check->: 检查大小比较。
;check-exn: 检查表达式是否抛出异常。

