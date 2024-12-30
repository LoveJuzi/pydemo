package rat

func Add(r1 Rat, r2 Rat) Rat {
	return MakeRat(
		r1.Numer()*r2.Denom()+r2.Numer()*r1.Denom(),
		r1.Denom()*r2.Denom())
}

func Sub(r1 Rat, r2 Rat) Rat {
	return MakeRat(
		r1.Numer()*r2.Denom()-r2.Numer()*r1.Denom(),
		r1.Denom()*r2.Denom())
}

func Mul(r1 Rat, r2 Rat) Rat {
	return MakeRat(r1.Numer()*r2.Numer(), r1.Denom()*r2.Denom())
}

func Div(r1 Rat, r2 Rat) Rat {
	return MakeRat(r1.Numer()*r2.Denom(), r1.Denom()*r2.Numer())
}

func Equal(r1 Rat, r2 Rat) bool {
	return r1.Numer()*r2.Denom() == r1.Denom()*r2.Numer()
}
