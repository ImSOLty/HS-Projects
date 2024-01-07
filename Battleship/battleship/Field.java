package battleship;

import java.util.*;
import java.util.stream.Collectors;

public class Field {

    Type[][] field;
    Ship[] ships = new Ship[]{
            new Ship("Aircraft Carrier", 5),
            new Ship("Battleship", 4),
            new Ship("Submarine", 3),
            new Ship("Cruiser", 3),
            new Ship("Destroyer", 2),
    };

    List<Coordinate> attempts = new ArrayList<>();
    int SIZE = 10;

    Field() {
        field = new Type[SIZE][SIZE];
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                field[i][j] = Type.FOG;
            }
        }
    }

    void AddShip(String coordinates, String name) throws BattleshipException {
        Ship s = Arrays.stream(ships).filter(c -> c.name.equals(name)).findAny().orElse(null);
        Coordinate[] coos = Helper.ParseCoordinates(coordinates);
        Coordinate[] shipCoo = new Coordinate[s.length];

        if (Math.abs(coos[0].y - coos[1].y + coos[0].x - coos[1].x) + 1 != s.length) {
            throw new BattleshipException("Error! Incorrect length.");
        }
        Coordinate from, to;
        if (coos[0].y != coos[1].y) {
            if (coos[0].x != coos[1].x) {
                throw new BattleshipException("Error! Cannot place ships diagonally.");
            }
            from = new Coordinate(coos[0].x, Math.min(coos[0].y, coos[1].y));
            to = new Coordinate(coos[1].x, Math.max(coos[0].y, coos[1].y));
        } else {
            from = new Coordinate(Math.min(coos[0].x, coos[1].x), coos[0].y);
            to = new Coordinate(Math.max(coos[0].x, coos[1].x), coos[1].y);
        }

        for (int i = from.x; i < to.x + 1; i++) {
            for (int j = from.y; j < to.y + 1; j++) {
                if (inspectNear(i, j).contains(Type.SHIP)) {
                    throw new BattleshipException("Error! Cannot place ships near each other.");
                }
                shipCoo[i - from.y + j - from.x] = new Coordinate(i, j);
            }
        }
        if (Arrays.stream(shipCoo).anyMatch(Objects::isNull)) {
            throw new BattleshipException("Error! Incorrect coordinates.");
        }
        for (Coordinate coo : shipCoo) {
            field[coo.x][coo.y] = Type.SHIP;
        }
        s.setCoordinates(shipCoo);
    }

    public String toString() {
        StringBuilder sb = new StringBuilder("  1 2 3 4 5 6 7 8 9 10\n");
        for (int i = 0; i < SIZE; i++) {
            sb.append(Helper.indexToChar(i)).append(" ");
            sb.append(Arrays.stream(field[i]).map(Object::toString).collect(Collectors.joining(" ")));
            sb.append("\n");
        }
        return sb.toString();
    }

    public String WithFog() {
        StringBuilder sb = new StringBuilder("  1 2 3 4 5 6 7 8 9 10\n");
        for (int i = 0; i < SIZE; i++) {
            sb.append(Helper.indexToChar(i)).append(" ");
            for (int j = 0; j < SIZE; j++) {
                sb.append(Helper.cooInList(attempts, i, j) ? field[i][j] : Type.FOG.toString());
                sb.append(" ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    public List<Type> inspectNear(int x, int y) {
        List<Type> types = new ArrayList<>();
        for (int i = x - 1; i < x + 2; i++) {
            for (int j = y - 1; j < y + 2; j++) {
                try {
                    if (!types.contains(field[i][j])) {
                        types.add(field[i][j]);
                    }
                } catch (IndexOutOfBoundsException ignored) {
                }
            }
        }
        return types;
    }

    String makeShot(String coordinate) throws BattleshipException {
        Coordinate coo = Helper.ParseCoordinate(coordinate);
        attempts.add(coo);
        for (Ship s : ships) {
            int status = s.getHit(coo);
            switch (status) {
                case 0 -> {
                    field[coo.x][coo.y] = Type.HIT;
                    return "You have already hit the ship! Try again:";
                }
                case 1 -> {
                    field[coo.x][coo.y] = Type.HIT;
                    return "You hit a ship! Try again:";
                }
                case 2 -> {
                    field[coo.x][coo.y] = Type.HIT;
                    if (Arrays.stream(ships).allMatch(p -> p.length <= p.hitTimes)) {
                        return "You sank the last ship. You won. Congratulations!";
                    }
                    return "You sank a ship! Specify a new target:";
                }
            }
        }
        field[coo.x][coo.y] = Type.MISS;
        return "You missed! Try again:";
    }
}
