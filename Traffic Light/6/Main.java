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

        QueueThread t = new QueueThread(amount, interval);
        t.setName("QueueThread");

        t.start();

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
            switch (chose) {
                case "1":
                    System.out.print("Input road name: ");
                    String name =scanner.nextLine();
                    t.enQueue(name);
                    scanner.nextLine();
                    break;
                case "2":
                    t.deQueue();
                    scanner.nextLine();
                    break;
                case "3":
                    t.menu=false;
                    while(true){
                        String x = scanner.nextLine();
                        if(x==""){
                            t.menu=true;
                            break;
                        }
                    }
                    break;
                case "0":
                    t.exit=true;
                    System.out.println("Bye!");
                    return;
                default:
                    System.out.println("There is no such option in list");
                    scanner.nextLine();
                    break;
            }
        }
    }
}
