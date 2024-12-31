package main

import "demo300/arithmetic"
import "demo300/polynomial"
import "fmt"

func main() {
	o5 := arithmetic.MakeArithmetic("Polynomial",
		"X", []polynomial.Term{
			polynomial.MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			polynomial.MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})

	o6 := arithmetic.MakeArithmetic("Polynomial",
		"X", []polynomial.Term{
			polynomial.MakeTerm(5, arithmetic.MakeArithmetic("Integer", 1)),
			polynomial.MakeTerm(4, arithmetic.MakeArithmetic("Integer", 3))})

	fmt.Println(o5.Display())
	fmt.Println(arithmetic.Add(o5, o6).Display())

	o1 := arithmetic.MakeArithmetic("Integer", 2)
	fmt.Println(o1.Display())
	o2 := arithmetic.MakeArithmetic("Number", 3)
	fmt.Println(o2.Display())
	o3 := arithmetic.MakeArithmetic("Rat", 3, 4)
	fmt.Println(o3.Display())
	o4 := arithmetic.MakeArithmetic("Complex", "Rectangular", 3, 4)
	fmt.Println(o4.Display())
}
