package main

import (
	"testing"
	"reflect"
)


func TestInputToElves(t *testing.T) {
	sample_input := `
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
`
	var expected = []Elf{
		Elf{[]int64{1000, 2000, 3000}},
		Elf{[]int64{4000}},
		Elf{[]int64{5000, 6000}},
		Elf{[]int64{7000, 8000, 9000}},
		Elf{[]int64{10000}},
	}
	actual := inputToElves(sample_input)
	if !reflect.DeepEqual(expected, actual) {
		t.Fail()
	}
}


func TestTotalCalories(t *testing.T) {
	var expected int64 = 6000
	actual := totalCalories(Elf{[]int64{1000, 2000, 3000}})
	if expected != actual {
		t.Fail()
	}
}
