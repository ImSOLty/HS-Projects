package battleship;

import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Player 1, place your ships on the game field");
        Player player1 = new Player();
        System.out.println("Press Enter and pass the move to another player");
        scanner.nextLine();
        System.out.println("Player 2, place your ships on the game field");
        Player player2 = new Player();
        System.out.println("Press Enter and pass the move to another player");
        scanner.nextLine();

        player1.SetOpponent(player2.field);
        player2.SetOpponent(player1.field);

        int status;
        boolean turn = true;
        while (true) {
            status = turn ? player1.Shoot() : player2.Shoot();
            if (status == 1) {
                break;
            }
            System.out.println("Press Enter and pass the move to another player");
            scanner.nextLine();
            turn = !turn;
        }
    }
}
