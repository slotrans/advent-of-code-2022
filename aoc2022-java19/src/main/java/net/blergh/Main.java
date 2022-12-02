package net.blergh;

import net.blergh.puzzle01.Solution01;

public class Main
{
    public static void main(String[] args) throws Exception
    {
        switch(args[0])
        {
            case "01":
                Solution01.run();
                break;
            default:
                System.err.println("please specify a known puzzle solution to run");
                System.exit(1);
        }

        System.exit(0);
    }
}