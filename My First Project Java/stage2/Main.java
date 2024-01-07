package calculator;

public class Main {
    public static void main(String[] args) {
        System.out.printf("""
                Earned amount:
                Bubblegum: $202
                Toffee: $118
                Ice cream: $2250
                Milk chocolate: $1680
                Doughnut: $1075
                Pancake: $80
                
                Income: $%s%n""", 202 + 118 + 2250 + 1680 + 1075 + 80);
    }
}