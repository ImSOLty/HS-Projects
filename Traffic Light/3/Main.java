import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static int isNumeric(String strNum) {
        if (strNum == null) {
            return -1;
        }
        int i;
        try {
            i = Integer.parseInt(strNum);
        } catch (NumberFormatException nfe) {
            return -1;
        }
        return i;
    }
    public static int readNumericString(Scanner scanner, String error){
        String str;
        int result;
        while(true){
            str = scanner.nextLine();
            result = isNumeric(str);
            if(result>0){
                break;
            }
            System.out.print(error);
        }
        return result;
    }

    public static void main(String[] args){
        Scanner scanner = new Scanner(System.in);
        System.out.println("Welcome to the traffic management system!");

        System.out.print("Input the number of roads: ");
        int amount = readNumericString(scanner, "Error: Incorrect input. Try again: ");
        System.out.print("Input the interval: ");
        int interval = readNumericString(scanner, "Error: Incorrect input. Try again: ");

        while(true) {
            try {
                if (System.getProperty("os.name").contains("Windows"))
                    new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
                else
                    Runtime.getRuntime().exec("clear");
            } catch (IOException | InterruptedException e) {
            }
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
                default:
                    System.out.println("Incorrect option");
                    break;
            }
            String x = scanner.nextLine();
        }
    }
}
