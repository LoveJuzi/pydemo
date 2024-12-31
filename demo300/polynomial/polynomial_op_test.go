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

func TestArithmeticAdd(t *testing.T) {
	o1 := arithmetic.MakeArithmetic("Polynomial",
		"X", []Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})

	o2 := arithmetic.MakeArithmetic("Polynomial",
		"X", []Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})

	o3 := arithmetic.Add(o1, o2)
	o4 := arithmetic.MakeArithmetic("Polynomial",
		"X", []Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 2)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 6))})
	assert.True(t, arithmetic.Equal(o3, o4))
}

func TestArithmeticAdd2(t *testing.T) {
	o1 := arithmetic.MakeArithmetic("Polynomial",
		"X", []Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})

	o2 := arithmetic.MakeArithmetic("Integer", 1)

	o3 := arithmetic.Add(o1, o2)
	o4 := arithmetic.MakeArithmetic("Polynomial",
		"X", []Term{
			MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3)),
			MakeTerm(0, arithmetic.MakeArithmetic("Integer", 1))})
	assert.True(t, arithmetic.Equal(o3, o4))
}
