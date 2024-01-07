package asciimirror;

import java.io.File;
import java.io.IOException;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Input the file path:");

        String path;
        Scanner inputScanner = new Scanner(System.in);
        path = inputScanner.nextLine();

        File file = new File(path);

        try(Scanner scanner = new Scanner(file)) {
            while(scanner.hasNext()){
                System.out.println(scanner.nextLine());
            }
        } catch (IOException io){
            System.out.print("File not found!");
        }
    }
}