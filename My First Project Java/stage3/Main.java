package calculator;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int income = 202 + 118 + 2250 + 1680 + 1075 + 80;
        System.out.printf("""
                Earned amount:
                Bubblegum: $202
                Toffee: $118
                Ice cream: $2250
                Milk chocolate: $1680
                Doughnut: $1075
                Pancake: $80
                
                Income: $%s%n""", income);
        System.out.print("Staff expenses: ");
        int staff = scanner.nextInt();
        System.out.print("Other expenses: ");
        int other = scanner.nextInt();
        System.out.printf("Net income: $%s%n", income - staff - other);
    }
}