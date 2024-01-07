package battleship;

import java.util.Arrays;

public class Ship {
    String name;
    Coordinate[] coordinates;
    int length;

    int hitTimes = 0;

    Ship(String name, int length) {
        this.name = name;
        this.length = length;
    }

    void setCoordinates(Coordinate... coordinates) {
        this.coordinates = Arrays.copyOf(coordinates, this.length);
    }

    int getHit(Coordinate coo) {
        Coordinate s = Arrays.stream(coordinates).filter(c -> c.x == coo.x && c.y == coo.y).findAny().orElse(null);
        if (s == null) {
            return -1;
        } else {
            if (s.type != Type.HIT) {
                hitTimes++;
                if (hitTimes == length) {
                    return 2;
                } else {
                    return 1;
                }
            }else{
                return 0;
            }
        }
    }
}
