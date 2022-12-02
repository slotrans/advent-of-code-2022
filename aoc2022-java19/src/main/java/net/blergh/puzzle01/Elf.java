package net.blergh.puzzle01;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class Elf
{
    private List<Integer> snacks;

    public Elf(List<Integer> snacks)
    {
        this.snacks = snacks;
    }

    public Elf(String chunk)
    {
        this.snacks = new ArrayList<>();
        for(String snackString : chunk.split("\n"))
        {
            snacks.add(Integer.parseInt(snackString));
        }
    }

    public List<Integer> getSnacks()
    {
        return snacks;
    }

    public Integer totalCalories()
    {
        return this.snacks.stream().reduce(0, Integer::sum);
    }

    public static List<Elf> elvesFromInputString(String input)
    {
        return Arrays.stream(input.split("\n\n")).map(Elf::new).collect(Collectors.toList());
    }

    @Override
    public boolean equals(Object o)
    {
        if (this == o)
        {
            return true;
        }
        if (o == null || getClass() != o.getClass())
        {
            return false;
        }
        Elf elf = (Elf) o;
        return Objects.equals(snacks, elf.snacks);
    }

    @Override
    public int hashCode()
    {
        return Objects.hash(snacks);
    }
}
