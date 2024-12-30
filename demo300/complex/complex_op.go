package complex

func Add(complex1 Complex, complex2 Complex) Complex {
	return MakeComplex(
		"Rectangular",
		complex1.RealPart()+complex2.RealPart(),
		complex1.ImagPart()+complex2.ImagPart())
}

func Sub(complex1 Complex, complex2 Complex) Complex {
	return MakeComplex(
		"Rectangular",
		complex1.RealPart()-complex2.RealPart(),
		complex1.ImagPart()-complex2.ImagPart())
}

func Mul(complex1 Complex, complex2 Complex) Complex {
	return MakeComplex(
		"Polar",
		complex1.Magnitude()*complex2.Magnitude(),
		complex1.Angle()+complex2.Angle())
}

func Div(complex1 Complex, complex2 Complex) Complex {
	return MakeComplex(
		"Polar",
		complex1.Magnitude()/complex2.Magnitude(),
		complex1.Angle()-complex2.Angle())
}

func Equal(complex1 Complex, complex2 Complex) bool {
	if complex1.RealPart() == complex2.RealPart() && complex1.ImagPart() == complex2.ImagPart() {
		return true
	}
	if complex1.Magnitude() == complex2.Magnitude() && complex1.Angle() == complex2.Angle() {
		return true
	}
	return false
}
