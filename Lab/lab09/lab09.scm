(define (over-or-under num1 num2) (cond ((< num1 num2) -1)
                                        ((= num1 num2) 0)
                                        (else 1)))

(define (make-adder num) (lambda (inc) (+ num inc)))

(define (composed f g) (lambda (x) (f (g x))))

(define (repeat f n) (lambda (x) (cond ((= n 1) (f x))
                                        (else (f ((repeat f (- n 1)) x)) ))
                                        ))

(define (max a b)
  (if (> a b)
      a
      b))

(define (min a b)
  (if (> a b)
      b
      a))

(define (gcd a b) 
                  (define big (max a b))
                  (define sml (min a b))
                  (define mol (modulo big sml))
                  (cond ((= mol 0) sml)
                        (else (gcd mol sml)))
                        )
