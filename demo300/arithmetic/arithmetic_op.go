package arithmetic

import "demo300/rat"
import "demo300/complex"

func Add(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	o1, o2, ok := convInnerType(o1, o2)
	if !ok {
		return nil
	}
	return AddTable[getTagPair(o1, o2)](o1, o2)
}

func Sub(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	o1, o2, ok := convInnerType(o1, o2)
	if !ok {
		return nil
	}
	return subTable[getTagPair(o1, o2)](o1, o2)
}

func Mul(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	o1, o2, ok := convInnerType(o1, o2)
	if !ok {
		return nil
	}
	return mulTable[getTagPair(o1, o2)](o1, o2)
}

func Div(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	o1, o2, ok := convInnerType(o1, o2)
	if !ok {
		return nil
	}
	return divTable[getTagPair(o1, o2)](o1, o2)
}

func Equal(o1 Arithmetic, o2 Arithmetic) bool {
	o1, o2, ok := convInnerType(o1, o2)
	if !ok {
		return false
	}
	return EqualTable[getTagPair(o1, o2)](o1, o2)
}

func getTagPair(o1 Arithmetic, o2 Arithmetic) string {
	return o1.Tag() + " " + o2.Tag()
}

func convInnerType(o1 Arithmetic, o2 Arithmetic) (Arithmetic, Arithmetic, bool) {
	f1 := ConvTable[o1.Tag()+"->"+o2.Tag()]
	f2 := ConvTable[o2.Tag()+"->"+o1.Tag()]
	if f1 != nil {
		o1 = f1(o1)
	}
	if f2 != nil {
		o2 = f2(o2)
	}
	if o1.Tag() != o2.Tag() {
		return o1, o2, false
	}
	return o1, o2, true
}

type ariOpFunc func(Arithmetic, Arithmetic) Arithmetic

var AddTable = make(map[string]ariOpFunc)

var subTable = make(map[string]ariOpFunc)

var mulTable = make(map[string]ariOpFunc)

var divTable = make(map[string]ariOpFunc)

type equalFunc func(Arithmetic, Arithmetic) bool

var EqualTable = make(map[string]equalFunc)

type convFunc func(Arithmetic) Arithmetic

var ConvTable = make(map[string]convFunc)

func init() {
	AddTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Integer",
			o1.(*arithmeticInteger).Object()+
				o2.(*arithmeticInteger).Object())
	}
	subTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Integer",
			o1.(*arithmeticInteger).Object()-
				o2.(*arithmeticInteger).Object())
	}
	mulTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Integer",
			o1.(*arithmeticInteger).Object()*
				o2.(*arithmeticInteger).Object())
	}
	divTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		n1 := o1.(*arithmeticInteger).Object()
		n2 := o2.(*arithmeticInteger).Object()
		if n2 == 0 {
			return nil
		}
		if n1 < n2 {
			return MakeArithmetic("Rat", n1, n2)
		}
		if n1%n2 != 0 {
			return MakeArithmetic("Rat", n1, n2)
		}
		return MakeArithmetic("Integer",
			o1.(*arithmeticInteger).Object()/
				o2.(*arithmeticInteger).Object())
	}
	EqualTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return o1.(*arithmeticInteger).Object() == o2.(*arithmeticInteger).Object()
	}

	AddTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Number",
			o1.(*arithmeticNumber).Object()+o2.(*arithmeticNumber).Object())
	}
	subTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Number",
			o1.(*arithmeticNumber).Object()-o2.(*arithmeticNumber).Object())
	}
	mulTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Number",
			o1.(*arithmeticNumber).Object()*o2.(*arithmeticNumber).Object())
	}
	divTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return MakeArithmetic("Number",
			o1.(*arithmeticNumber).Object()/o2.(*arithmeticNumber).Object())
	}
	EqualTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return o1.(*arithmeticNumber).Object() == o2.(*arithmeticNumber).Object()
	}

	AddTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticRat{
			_rat: rat.Add(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object()),
		}
	}
	subTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticRat{
			_rat: rat.Sub(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object()),
		}
	}
	mulTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticRat{
			_rat: rat.Mul(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object()),
		}
	}
	divTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticRat{
			_rat: rat.Div(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object()),
		}
	}
	EqualTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return rat.Equal(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object())
	}

	AddTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.Add(
				o1.(*arithmeticComplex).Object(),
				o2.(*arithmeticComplex).Object()),
		}
	}
	subTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.Sub(
				o1.(*arithmeticComplex).Object(),
				o2.(*arithmeticComplex).Object()),
		}
	}
	mulTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.Mul(
				o1.(*arithmeticComplex).Object(),
				o2.(*arithmeticComplex).Object()),
		}
	}
	divTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
		return &arithmeticComplex{
			_complex: complex.Div(
				o1.(*arithmeticComplex).Object(),
				o2.(*arithmeticComplex).Object()),
		}
	}
	EqualTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return complex.Equal(
			o1.(*arithmeticComplex).Object(),
			o1.(*arithmeticComplex).Object())
	}

	ConvTable["Integer->Rat"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic("Rat", o.(*arithmeticInteger).Object(), 1)
	}
	ConvTable["Integer->Number"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic("Number", o.(*arithmeticInteger).Object())
	}
	ConvTable["Integer->Complex"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic("Complex", "Rectangular", o.(*arithmeticInteger).Object(), 0)
	}
	ConvTable["Rat->Number"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic(
			"Number",
			float64(o.(*arithmeticRat).Object().Numer())/
				float64(o.(*arithmeticRat).Object().Denom()))
	}
	ConvTable["Rat->Complex"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic("Complex",
			float64(o.(*arithmeticRat).Object().Numer())/
				float64(o.(*arithmeticRat).Object().Denom()),
			0)
	}
	ConvTable["Number->Complex"] = func(o Arithmetic) Arithmetic {
		return MakeArithmetic("Complex",
			o.(*arithmeticNumber).Object(), 0)
	}
}
