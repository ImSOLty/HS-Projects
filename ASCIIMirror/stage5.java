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
        List<String> strings = new ArrayList<>();

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

        int max = 0;
        for (String s : strings){
            if(s.length()>max){
                max=s.length();
            }
        }

        for (String s : strings){
            int i=0;
            for (i=0;i<s.length();i++){
                System.out.print(s.charAt(i));
            }
            for (;i<max+1;i++){
                System.out.print(" ");
            }
            System.out.print("| ");
            for (i=max;i>s.length();i--){
                System.out.print(" ");
            }
            for (i=s.length()-1;i>=0;i--){
                switch (s.charAt(i)){
                    case '(': System.out.print(")"); break;
                    case ')': System.out.print("("); break;
                    case '[': System.out.print("]"); break;
                    case ']': System.out.print("["); break;
                    case '{': System.out.print("}"); break;
                    case '}': System.out.print("{"); break;
                    case '<': System.out.print(">"); break;
                    case '>': System.out.print("<"); break;
                    case '\\': System.out.print("/"); break;
                    case '/': System.out.print("\\"); break;
                    default: System.out.print(s.charAt(i)); break;
                }
            }
            System.out.println();
        }
    }
}