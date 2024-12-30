package arithmetic

import "testing"
import "github.com/stretchr/testify/assert"

func TestInteger(t *testing.T) {
	num1 := MakeArithmetic("Integer", 1)
	num2 := MakeArithmetic("Integer", 2)
	num3 := Add(num1, num2)
	assert.Equal(t, "Integer", num3.Tag())
	assert.True(t, Equal(num3, MakeArithmetic("Integer", 3)))
	num4 := Div(num1, num2)
	assert.Equal(t, "Rat", num4.Tag())
	assert.True(t, Equal(num4, MakeArithmetic("Rat", 1, 2)))
}

func TestNumber(t *testing.T) {
	num1 := MakeArithmetic("Number", 1)
	num2 := MakeArithmetic("Number", 2)
	num3 := Add(num1, num2)
	assert.Equal(t, "Number", num3.Tag())
	assert.True(t, Equal(num3, MakeArithmetic("Number", 3)))
}

func TestRat(t *testing.T) {
	o1 := MakeArithmetic("Rat", 1, 2)
	o2 := MakeArithmetic("Rat", 1, 2)
	o3 := Add(o1, o2)
	assert.Equal(t, "Rat", o3.Tag())
	assert.True(t, Equal(o3, MakeArithmetic("Rat", 1, 1)))
}

func TestComplex(t *testing.T) {
	o1 := MakeArithmetic("Complex", "Rectangular", 1, 1)
	o2 := MakeArithmetic("Complex", "Rectangular", 2, 2)
	assert.Equal(t, "Complex", o1.Tag())
	o3 := Add(o1, o2)
	assert.Equal(t, "Complex", o3.Tag())
	assert.True(t, Equal(o3, MakeArithmetic("Complex", "Rectangular", 3, 3)))
}
