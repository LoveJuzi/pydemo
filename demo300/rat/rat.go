package rat

type Rat interface {
	Numer() int64
	Denom() int64
}

func MakeRat(numer int64, denom int64) Rat {
	rat := &ratImpl{}
	rat.SetNumer(numer)
	rat.SetDenom(denom)
	return rat
}

type ratImpl struct {
	numer int64
	denom int64
}

func (o *ratImpl) SetNumer(numer int64) {
	o.numer = numer
}

func (o *ratImpl) SetDenom(denom int64) {
	o.denom = denom
}

func (o *ratImpl) Numer() int64 {
	return o.numer
}

func (o *ratImpl) Denom() int64 {
	return o.denom
}
