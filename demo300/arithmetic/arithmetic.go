package arithmetic

import (
	"demo300/complex"
	"demo300/rat"
	"demo300/utils"
	"fmt"
	"strconv"
)

type Arithmetic interface {
	Tag() string
	Display() string
}

func MakeArithmetic(tag string, params ...interface{}) Arithmetic {
	return MakeTable[tag](params...)
}

type arithmeticComplex struct {
	_complex complex.Complex
}

func (o *arithmeticComplex) Tag() string {
	return "Complex"
}

func (o *arithmeticComplex) Display() string {
	return fmt.Sprintf("%f +i %f", o._complex.RealPart(), o._complex.ImagPart())
}

func (o *arithmeticComplex) Object() complex.Complex {
	return o._complex
}

type arithmeticRat struct {
	_rat rat.Rat
}

func (o *arithmeticRat) Tag() string {
	return "Rat"
}

func (o *arithmeticRat) Display() string {
	return fmt.Sprintf("%d / %d", o._rat.Numer(), o._rat.Denom())
}

func (o *arithmeticRat) Object() rat.Rat {
	return o._rat
}

type arithmeticInteger struct {
	_integer int64
}

func (obj *arithmeticInteger) Tag() string {
	return "Integer"
}

func (obj *arithmeticInteger) Display() string {
	return strconv.FormatInt(obj._integer, 10)
}

func (obj *arithmeticInteger) Object() int64 {
	return obj._integer
}

type arithmeticNumber struct {
	_number float64
}

func (obj *arithmeticNumber) Tag() string {
	return "Number"
}

func (obj *arithmeticNumber) Display() string {
	return strconv.FormatFloat(obj._number, 'f', 2, 64)
}

func (obj *arithmeticNumber) Object() float64 {
	return obj._number
}

type makeFunc func(...interface{}) Arithmetic

var MakeTable = make(map[string]makeFunc)

func init() {
	MakeTable["Complex"] = func(params ...interface{}) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.MakeComplex(params[0].(string), params[1:]...),
		}
	}
	MakeTable["Rat"] = func(params ...interface{}) Arithmetic {
		v1, ok1 := utils.ConvInt64(params[0])
		v2, ok2 := utils.ConvInt64(params[1])
		if !ok1 && !ok2 {
			return nil
		}
		return &arithmeticRat{
			_rat: rat.MakeRat(v1, v2),
		}
	}
	MakeTable["Integer"] = func(params ...interface{}) Arithmetic {
		v, ok := utils.ConvInt64(params[0])
		if !ok {
			return nil
		}
		return &arithmeticInteger{_integer: v}
	}
	MakeTable["Number"] = func(params ...interface{}) Arithmetic {
		v, ok := utils.ConvFloat64(params[0])
		if !ok {
			return nil
		}
		return &arithmeticNumber{_number: v}
	}
}
