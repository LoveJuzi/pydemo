package polynomial

import "demo300/arithmetic"

type Polynomial interface {
	Variable() string
	TermList() []Term
}

type Term interface {
	Times() int
	Coeff() arithmetic.Arithmetic
}

func MakePolynomial(variable string, termList []Term) Polynomial {
	return &polynomial{_variable: variable, _termList: termList}
}

func MakeTerm(times int, coeff arithmetic.Arithmetic) Term {
	return &term{_times: times, _coeff: coeff}
}

type polynomial struct {
	_variable string
	_termList []Term
}

func (o *polynomial) Variable() string { return o._variable }

func (o *polynomial) TermList() []Term { return o._termList }

type term struct {
	_times int
	_coeff arithmetic.Arithmetic
}

func (o *term) Times() int { return o._times }

func (o *term) Coeff() arithmetic.Arithmetic { return o._coeff }
