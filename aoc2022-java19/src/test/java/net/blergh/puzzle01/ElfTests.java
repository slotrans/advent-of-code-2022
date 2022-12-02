package net.blergh.puzzle01;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ElfTests
{
    final String SAMPLE_INPUT =
    """
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
    """;

    @Test
    void constructElfFromChunk()
    {
        String chunk = "1000\n2000\n3000";
        Elf expected = new Elf(List.of(1000, 2000, 3000));
        Elf actual = new Elf(chunk);
        assertEquals(expected, actual);
    }

    @Test
    void constructElvesFromSampleInput()
    {
        List<Elf> expected = List.of(
                new Elf(List.of(1000, 2000, 3000)),
                new Elf(List.of(4000)),
                new Elf(List.of(5000, 6000)),
                new Elf(List.of(7000, 8000, 9000)),
                new Elf(List.of(10000))
        );
        List<Elf> actual = Elf.elvesFromInputString(SAMPLE_INPUT);
        assertEquals(expected, actual);
    }
}
