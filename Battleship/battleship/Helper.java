package battleship;

import java.util.ArrayList;
import java.util.List;

public class Helper {


    static Coordinate ParseCoordinate(String coordinate) throws BattleshipException {
        int x = charToIndex(coordinate.charAt(0));
        int y = Integer.parseInt(coordinate.substring(1)) - 1;
        if (x < 0 || x > 9 || y < 0 || y > 9) {
            throw new BattleshipException("Error! You entered the wrong coordinates!");
        }
        return new Coordinate(x, y);
    }

    static Coordinate[] ParseCoordinates(String coordinates) throws BattleshipException {
        List<Coordinate> coo = new ArrayList<>();
        for (String c : coordinates.split(" ")) {
            coo.add(ParseCoordinate(c));
        }
        return coo.toArray(new Coordinate[0]);
    }

    public static int charToIndex(char c) {
        return (c - 65);
    }

    public static char indexToChar(int i) {
        return (char) (i + 65);
    }

    public static boolean cooInList(List<Coordinate> list, int x, int y) {
        return list.stream().filter(c -> c.x == x && c.y == y).toArray().length != 0;
    }
}
