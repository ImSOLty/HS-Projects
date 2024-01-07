package battleship;

public class Coordinate {
    int x, y;
    Type type = Type.FOG;

    Coordinate(int xCoo, int yCoo) {
        this.x = xCoo;
        this.y = yCoo;
    }

    void setType(Type type){
        this.type = type;
    }
}
