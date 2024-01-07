package battleship;

public enum Type {
    FOG("~"),
    MISS("M"),
    HIT("X"),
    SHIP("O");
    private final String repr;

    private Type(String s) {
        repr = s;
    }

    public String toString() {
        return this.repr;
    }
}
