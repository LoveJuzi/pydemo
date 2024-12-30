package arithmetic

import (
	"demo300/complex"
	"demo300/rat"
	"demo300/utils"
	"strconv"
)

type Arithmetic interface {
	Tag() string
	Display() string
}

func MakeArithmetic(tag string, params ...interface{}) Arithmetic {
	return makeTable[tag](params...)
}

type arithmeticComplex struct {
	_complex complex.Complex
}

func (obj *arithmeticComplex) Tag() string {
	return "Complex"
}

func (obj *arithmeticComplex) Display() string {
	return "Complex: "
}

func (obj *arithmeticComplex) Object() complex.Complex {
	return obj._complex
}

type arithmeticRat struct {
	_rat rat.Rat
}

func (o *arithmeticRat) Tag() string {
	return "Rat"
}

func (o *arithmeticRat) Display() string {
	return "Rat"
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
	return "Integer: " + strconv.FormatInt(obj._integer, 10)
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
	return "Number: " + strconv.FormatFloat(obj._number, 'f', 2, 64)
}

func (obj *arithmeticNumber) Object() float64 {
	return obj._number
}

type makeFunc func(...interface{}) Arithmetic

var makeTable = make(map[string]makeFunc)

func init() {
	makeTable["Complex"] = func(params ...interface{}) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.MakeComplex(params[0].(string), params[1:]...),
		}
	}
	makeTable["Rat"] = func(params ...interface{}) Arithmetic {
		v1, ok1 := utils.ConvInt64(params[0])
		v2, ok2 := utils.ConvInt64(params[1])
		if !ok1 && !ok2 {
			return nil
		}
		return &arithmeticRat{
			_rat: rat.MakeRat(v1, v2),
		}
	}
	makeTable["Integer"] = func(params ...interface{}) Arithmetic {
		v, ok := utils.ConvInt64(params[0])
		if !ok {
			return nil
		}
		return &arithmeticInteger{_integer: v}
	}
	makeTable["Number"] = func(params ...interface{}) Arithmetic {
		v, ok := utils.ConvFloat64(params[0])
		if !ok {
			return nil
		}
		return &arithmeticNumber{_number: v}
	}
}
