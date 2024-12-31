package polynomial

import (
	"demo300/arithmetic"
)

func Equal(o1 Polynomial, o2 Polynomial) bool {
	if o1.Variable() != o2.Variable() {
		return false
	}
	tlist1 := o1.TermList()
	tlist2 := o2.TermList()
	if len(tlist1) != len(tlist2) {
		return false
	}

	for i := 0; i < len(tlist1); i++ {
		if tlist1[i].Times() != tlist2[i].Times() {
			return false
		}
		if !arithmetic.Equal(tlist1[i].Coeff(), tlist2[i].Coeff()) {
			return false
		}
	}

	return true
}

func getVariable(o1 Polynomial, o2 Polynomial) (string, bool) {
	if o1.Variable() == o2.Variable() {
		return o1.Variable(), true
	}

	if o1.Variable() == "" {
		return o2.Variable(), true
	}

	if o2.Variable() == "" {
		return o1.Variable(), true
	}

	return "", false
}

func Add(o1 Polynomial, o2 Polynomial) Polynomial {
	variable, ok := getVariable(o1, o2)
	if !ok {
		return nil
	}
	tlist1 := o1.TermList()
	tlist2 := o2.TermList()
	tlist1Len := len(tlist1)
	tlist2Len := len(tlist2)
	termList := []Term{}
	i, j := 0, 0
	for {
		if i >= tlist1Len && j >= tlist2Len {
			break
		}
		if i >= tlist1Len {
			termList = append(termList, tlist2[j])
			j++
			continue
		}
		if j >= tlist2Len {
			termList = append(termList, tlist1[i])
			i++
			continue
		}
		if tlist1[i].Times() > tlist2[j].Times() {
			termList = append(termList, tlist1[i])
			i++
			continue
		}
		if tlist1[i].Times() < tlist2[j].Times() {
			termList = append(termList, tlist2[j])
			j++
			continue
		}
		term := MakeTerm(tlist1[i].Times(),
			arithmetic.Add(tlist1[i].Coeff(), tlist2[j].Coeff()))
		termList = append(termList, term)
		i++
		j++
	}
	return MakePolynomial(variable, termList)
}
