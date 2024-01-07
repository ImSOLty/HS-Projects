import java.util.Scanner;

public class Main {
    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the traffic management system!");

        System.out.print("Input the number of roads: ");
        int amount = scanner.nextInt();
        System.out.print("Input the interval: ");
        int interval = scanner.nextInt();
        String x = scanner.nextLine();

        while(true) {
            System.out.println("Options:\n" +
                    "1. Add road\n" +
                    "2. Delete road\n" +
                    "3. Open system\n" +
                    "0. Quit");
            String chose = scanner.nextLine();
            switch(chose){
                case "1":
                    System.out.println("Road added");
                    break;
                case "2":
                    System.out.println("Road deleted");
                    break;
                case "3":
                    System.out.println("System opened");
                    break;
                case "0":
                    System.out.println("Bye!");
                    return;
            }
        }
    }
}
