package complex

import "testing"
import "github.com/stretchr/testify/assert"

func TestEqual(t *testing.T) {
	r1 := MakeComplex("Polar", 1.0, 2.0)
	r2 := MakeComplex("Polar", 1.0, 2.0)
	assert.Equal(t, r1.Magnitude(), 1.0)
	assert.Equal(t, r2.Angle(), 2.0)
}
