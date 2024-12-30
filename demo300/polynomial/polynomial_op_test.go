package polynomial

import (
	"demo300/arithmetic"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestPolynamial(t *testing.T) {
	o1 := MakePolynomial("X",
		[]Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})
	o2 := MakePolynomial("X",
		[]Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Number", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Number", 3))})
	assert.True(t, Equal(o1, o2))
}

func TestPolynamialAdd(t *testing.T) {
	o1 := MakePolynomial("X",
		[]Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})
	o2 := MakePolynomial("X",
		[]Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Number", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Number", 3))})
	o3 := Add(o1, o2)
	o4 := MakePolynomial("X",
		[]Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 2)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 6))})
	assert.True(t, Equal(o3, o4))
}
