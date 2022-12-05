package main

import (
	"os"
	"fmt"
	"strings"
	"strconv"
	"sort"
)


type Elf struct {
	snacks []int64
}


func inputToElves(inputString string) []Elf {
	var out []Elf
	for _, chunkString := range strings.Split(inputString, "\n\n") {
		var snacks []int64
		for _, snackString := range strings.Split(chunkString, "\n") {
			if snackString == "" {
				continue
			}
			var snack int64
			snack, err := strconv.ParseInt(snackString, 10, 64)
			if err != nil {
				panic(err)
			}
			snacks = append(snacks, snack)
		}
		out = append(out, Elf{snacks})
	}
	return out
}


func totalCalories(elf Elf) int64 {
	var total int64 = 0
	for _, calories := range elf.snacks {
		total += calories
	}
	return total
}


func caloriesPerElf(elves []Elf) []int64 {
	var out []int64
	for _, elf := range elves {
		out = append(out, totalCalories(elf))
	}
	return out
}


// defined for positive values only
func findMax(vals []int64) int64 {
	var max int64 = 0
	for _, v := range vals {
		if v > max {
			max = v
		}
	}
	return max
}


func main() {
	input01Raw, err := os.ReadFile("../../input/input01")
	if err != nil {
		panic(err)
	}
	input01 := string(input01Raw)

	elves := inputToElves(input01)
	calsPerElf := caloriesPerElf(elves)
	maxCalories := findMax(calsPerElf)
	fmt.Printf("(p1 answer) elf with the most calories has: %d\n", maxCalories) // 72070

	sort.Slice(calsPerElf, func(i, j int) bool { return calsPerElf[i] > calsPerElf[j] }) // ">" to get a reversed sort
	var top3Total int64 = 0
	for i := 0; i < 3; i++ {
		top3Total += calsPerElf[i]
	}
	fmt.Printf("(p2 answer) top 3 elves' total calories: %d\n", top3Total) // 211805
}
