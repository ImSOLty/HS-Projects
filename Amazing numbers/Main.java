package numbers;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import java.util.stream.Stream;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("""
                Welcome to Amazing Numbers!
                                
                Supported requests:
                - enter a natural number to know its properties;
                - enter two natural numbers to obtain the properties of the list:
                  * the first parameter represents a starting number;
                  * the second parameter shows how many consecutive numbers are to be printed;
                - two natural numbers and properties to search for;
                - a property preceded by minus must not be present in numbers;
                - separate the parameters with one space;
                - enter 0 to exit.""");
        String[] req = new String[]{"-1", "-1", "DRAKE"};
        while (true) {
            System.out.print("Enter a request: ");
            String inp = scanner.nextLine().toUpperCase();
            try {
                req = inp.split(" ");
            } catch (NumberFormatException ignored) {
            }
            if (req.length == 1) {
                long data = Long.parseLong(req[0]);
                if (data == 0) {
                    break;
                }
                if (data < 0) {
                    System.out.println("The first parameter should be a natural number or zero.");
                    continue;
                }
                System.out.println("Properties of " + req[0]);
                for (Property p : Property.values()) {
                    if (!p.name().startsWith("NON"))
                        System.out.printf("\t%s: %b\n", p.name(), p.valid(data));
                }
            } else if (req.length == 2) {
                long[] data = Arrays.stream(req).mapToLong(Long::parseLong).toArray();
                if (data[0] < 0) {
                    System.out.println("The first parameter should be a natural number or zero.");
                    continue;
                }
                if (data[1] < 0) {
                    System.out.println("The second parameter should be a natural number or zero.");
                    continue;
                }
                for (long i = data[0]; i < data[0] + data[1]; i++) {
                    long checkValue = i;
                    System.out.printf("\t%d is %s\n", i,
                            String.join(", ",
                                    Arrays.stream(Property.values())
                                            .filter(p -> p.valid(checkValue) && !p.name().startsWith("NON"))
                                            .map(Enum::name)
                                            .toArray(String[]::new)));
                }
            } else {
                long from = Long.parseLong(req[0]);
                long count = Long.parseLong(req[1]);
                List<String> props = Arrays.stream(Arrays.copyOfRange(req, 2, req.length)).toList();
                List<String> wrong = new ArrayList<>();
                for (String p : props) {
                    if (!Arrays.stream(Property.values()).map(Enum::name).toList().contains(p.replace("-", "")))
                        wrong.add(p);
                }
                if (!wrong.isEmpty()) {
                    if (wrong.size() == 1) {
                        System.out.printf("The property [%s] is wrong.\nAvailable properties: [%s]", wrong.get(0),
                                Arrays.toString(Property.values()));
                    } else {
                        System.out.printf("The properties [%s] are wrong.\nAvailable properties: [%s]",
                                String.join(", ", wrong), Arrays.toString(Property.values()));
                    }
                    continue;
                }
                boolean stop = false;
                for (String p : props) {
                    List<String> listOfOpposite = List.of(p.startsWith("-")
                            ? Property.valueOf(Property.valueOf(p.replace("-", "")).opposite()[0]).opposite()
                            : Property.valueOf(p).opposite());
                    for (String opp : listOfOpposite) {
                        if (props.contains(opp)) {
                            System.out.printf("The request contains mutually exclusive properties: [%s]\n" +
                                    "There are no numbers with these properties.", p + ", " + opp);
                            stop = true;
                        }
                    }
                }
                if (stop) {
                    continue;
                }

                List<String> reprops = props.stream().map(p -> p.startsWith("-")
                        ? Property.valueOf(p.replace("-", "")).opposite()[0]
                        : p).toList();

                while (count != 0) {
                    long checkValue = from;
                    if (Arrays.stream(Property.values()).allMatch(p -> p.valid(checkValue) || !reprops.contains(p.name()))) {
                        count--;
                        System.out.printf("\t%d is %s\n", checkValue,
                                String.join(", ",
                                        Arrays.stream(Property.values())
                                                .filter(p -> p.valid(checkValue) && !p.name().startsWith("NON"))
                                                .map(Enum::name)
                                                .toArray(String[]::new)));
                    }
                    from++;
                }
            }
        }
        System.out.println("Goodbye!");
    }
}
