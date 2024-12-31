package polynomial

import "demo300/arithmetic"
import "fmt"

type arithmeticPolynomial struct {
	_polynomial Polynomial
}

func (o *arithmeticPolynomial) Tag() string {
	return "Polynomial"
}

func (o *arithmeticPolynomial) Display() string {
	res := ""
	for i := 0; i < len(o._polynomial.TermList()); i++ {
		if i > 0 {
			res += " + "
		}
		res += fmt.Sprintf("%s %s ^ %d",
			o._polynomial.TermList()[i].Coeff().Display(),
			o._polynomial.Variable(),
			o._polynomial.TermList()[i].Times())
	}
	return res
}

func (o *arithmeticPolynomial) Object() Polynomial {
	return o._polynomial
}

func init() {
	arithmetic.MakeTable["Polynomial"] = func(params ...interface{}) arithmetic.Arithmetic {
		return &arithmeticPolynomial{
			_polynomial: MakePolynomial(params[0].(string), params[1].([]Term)),
		}
	}

	arithmetic.AddTable["Polynomial Polynomial"] = func(o1 arithmetic.Arithmetic,
		o2 arithmetic.Arithmetic) arithmetic.Arithmetic {
		return &arithmeticPolynomial{
			_polynomial: Add(o1.(*arithmeticPolynomial).Object(),
				o2.(*arithmeticPolynomial).Object()),
		}
	}
	arithmetic.EqualTable["Polynomial Polynomial"] = func(o1 arithmetic.Arithmetic,
		o2 arithmetic.Arithmetic) bool {
		return Equal(o1.(*arithmeticPolynomial).Object(),
			o2.(*arithmeticPolynomial).Object())
	}
	arithmetic.ConvTable["Integer->Polynomial"] =
		func(o arithmetic.Arithmetic) arithmetic.Arithmetic {
			return arithmetic.MakeArithmetic(
				"Polynomial",
				"X",
				[]Term{MakeTerm(0, o)})
		}
	arithmetic.ConvTable["Rat->Polynomial"] =
		func(o arithmetic.Arithmetic) arithmetic.Arithmetic {
			return arithmetic.MakeArithmetic(
				"Polynomial",
				"X",
				[]Term{MakeTerm(0, o)})
		}
	arithmetic.ConvTable["Number->Polynomial"] =
		func(o arithmetic.Arithmetic) arithmetic.Arithmetic {
			return arithmetic.MakeArithmetic(
				"Polynomial",
				"X",
				[]Term{MakeTerm(0, o)})
		}
	arithmetic.ConvTable["Complex->Polynomial"] =
		func(o arithmetic.Arithmetic) arithmetic.Arithmetic {
			return arithmetic.MakeArithmetic(
				"Polynomial",
				"X",
				[]Term{MakeTerm(0, o)})
		}
}
