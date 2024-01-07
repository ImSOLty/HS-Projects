package battleship;

import java.util.Scanner;

public class Player {
    Field field;
    Field opponent;
    Scanner scanner;

    Player() {
        scanner = new Scanner(System.in);
        field = initialize();
    }

    public int Shoot() {
        String result;
        while (true) {
            try {
                System.out.print(opponent.WithFog());
                System.out.println("---------------------");
                System.out.print(field);
                System.out.println("Player 1, it's your turn:");
                String inp = scanner.nextLine();
                result = opponent.makeShot(inp);
                System.out.println(result);
                break;
            } catch (BattleshipException e) {
                System.out.println(e.getMessage() + " Try again:");
            }
        }
        if(result.contains("last")){
            return 1;
        }else{
            return 0;
        }
    }

    void StartGame() {
        System.out.println("The game starts!");
        System.out.print(field.WithFog());
    }

    void SetOpponent(Field field) {
        opponent = field;
    }

    public Field initialize() {
        Field field = new Field();
        System.out.println(field);
        for (Ship s : field.ships) {
            while (true) {
                System.out.printf("Enter the coordinates of the %s (%d cells):%n", s.name, s.length);
                String inp = scanner.nextLine();
                try {
                    field.AddShip(inp, s.name);
                    System.out.print(field);
                    break;
                } catch (BattleshipException e) {
                    System.out.println(e.getMessage());
                }
            }
        }
        return field;
    }
}
