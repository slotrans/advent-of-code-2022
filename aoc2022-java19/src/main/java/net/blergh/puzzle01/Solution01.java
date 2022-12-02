package net.blergh.puzzle01;

import net.blergh.Constants;


import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Optional;

public class Solution01
{
    public static void run() throws Exception
    {
        final String input01 = Files.readString(Path.of(Constants.INPUT_ROOT + "/input01"));

        List<Elf> elves = Elf.elvesFromInputString(input01);
        Optional<Integer> maxCalories = elves.stream().map(e -> e.totalCalories()).max(Integer::compare);
        System.out.println("(p1 answer) elf with the most calories has: " + maxCalories.get()); // 72070
    }

}
