package complex

import (
	"demo300/utils"
	"math"
)

type Complex interface {
	RealPart() float64
	ImagPart() float64
	Magnitude() float64
	Angle() float64
}

func MakeComplex(tag string, params ...interface{}) Complex {
	return makeTable[tag](params...)
}

type rectangularComplex struct {
	realPart float64
	imagPart float64
}

func (complex *rectangularComplex) RealPart() float64 {
	return complex.realPart
}

func (complex *rectangularComplex) ImagPart() float64 {
	return complex.imagPart
}

func (complex *rectangularComplex) Magnitude() float64 {
	return math.Sqrt(complex.realPart*complex.realPart +
		complex.imagPart*complex.imagPart)
}

func (complex *rectangularComplex) Angle() float64 {
	return math.Atan2(complex.imagPart, complex.realPart)
}

type polarComplex struct {
	magnitude float64
	angle     float64
}

func (complex *polarComplex) RealPart() float64 {
	return complex.magnitude * math.Cos(complex.angle)
}

func (complex *polarComplex) ImagPart() float64 {
	return complex.magnitude * math.Sin(complex.angle)
}

func (complex *polarComplex) Magnitude() float64 {
	return complex.magnitude
}

func (complex *polarComplex) Angle() float64 {
	return complex.angle
}

// Factory
type makeFunc func(...interface{}) Complex

var makeTable = make(map[string]makeFunc)

func init() {
	makeTable["Rectangular"] = func(params ...interface{}) Complex {
		v1, ok1 := utils.ConvFloat64(params[0])
		v2, ok2 := utils.ConvFloat64(params[1])
		if !ok1 && !ok2 {
			return nil
		}
		return &rectangularComplex{realPart: v1, imagPart: v2}
	}
	makeTable["Polar"] = func(params ...interface{}) Complex {
		v1, ok1 := utils.ConvFloat64(params[0])
		v2, ok2 := utils.ConvFloat64(params[1])
		if !ok1 && !ok2 {
			return nil
		}
		return &polarComplex{magnitude: v1, angle: v2}
	}
}
