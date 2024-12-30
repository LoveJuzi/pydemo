package arithmetic

import "demo300/rat"
import "demo300/complex"

func Add(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	return addTable[getTagPair(o1, o2)](o1, o2)
}

func Sub(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	return subTable[getTagPair(o1, o2)](o1, o2)
}

func Mul(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	return mulTable[getTagPair(o1, o2)](o1, o2)
}

func Div(o1 Arithmetic, o2 Arithmetic) Arithmetic {
	return divTable[getTagPair(o1, o2)](o1, o2)
}

func Equal(o1 Arithmetic, o2 Arithmetic) bool {
	return equalTable[getTagPair(o1, o2)](o1, o2)
}

func getTagPair(o1 Arithmetic, o2 Arithmetic) string {
	return o1.Tag() + " " + o2.Tag()
}

type ariOpFunc func(Arithmetic, Arithmetic) Arithmetic

var addTable = make(map[string]ariOpFunc)

var subTable = make(map[string]ariOpFunc)

var mulTable = make(map[string]ariOpFunc)

var divTable = make(map[string]ariOpFunc)

type equalFunc func(Arithmetic, Arithmetic) bool

var equalTable = make(map[string]equalFunc)

func init() {
	addTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
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
	equalTable["Integer Integer"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return o1.(*arithmeticInteger).Object() == o2.(*arithmeticInteger).Object()
	}

	addTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
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
	equalTable["Number Number"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return o1.(*arithmeticNumber).Object() == o2.(*arithmeticNumber).Object()
	}

	addTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
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
	equalTable["Rat Rat"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return rat.Equal(o1.(*arithmeticRat).Object(), o2.(*arithmeticRat).Object())
	}

	addTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) Arithmetic {
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
	equalTable["Complex Complex"] = func(o1 Arithmetic, o2 Arithmetic) bool {
		return complex.Equal(
			o1.(*arithmeticComplex).Object(),
			o1.(*arithmeticComplex).Object())
	}
}
