package asciimirror;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        System.out.println("Input the file path:");
        List<String> strings=new ArrayList<>();
        String path;
        Scanner inputScanner = new Scanner(System.in);
        path = inputScanner.nextLine();

        File file = new File(path);

        try(Scanner scanner = new Scanner(file)) {
            while(scanner.hasNext()){
                strings.add(scanner.nextLine());
            }
        } catch (IOException io){
            System.out.print("File not found!");
            return;
        }
        int max=0;
        for (String s:strings) {
            if(s.length()>=max){
                max=s.length();
            }
        }
        for (String s:strings) {
            System.out.print(s);
            System.out.print(" ".repeat(max-s.length()));
            System.out.print(" | ");
            System.out.print(s);
            System.out.println(" ".repeat(max-s.length()));
        }
    }
}