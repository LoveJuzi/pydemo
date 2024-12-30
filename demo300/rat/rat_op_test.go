package rat

import "testing"
import "github.com/stretchr/testify/assert"

func TestAdd(t *testing.T) {
	r1 := MakeRat(1, 2)
	r2 := MakeRat(2, 3)
	assert.True(t, Equal(Add(r1, r2), MakeRat(7, 6)))
}

func TestSub(t *testing.T) {
	r1 := MakeRat(1, 2)
	r2 := MakeRat(2, 3)
	assert.True(t, Equal(Sub(r1, r2), MakeRat(-1, 6)))
}

func TestMul(t *testing.T) {
	r1 := MakeRat(1, 2)
	r2 := MakeRat(2, 3)
	assert.True(t, Equal(Mul(r1, r2), MakeRat(2, 6)))
}

func TestDiv(t *testing.T) {
	r1 := MakeRat(1, 2)
	r2 := MakeRat(2, 3)
	assert.True(t, Equal(Div(r1, r2), MakeRat(3, 4)))
}
