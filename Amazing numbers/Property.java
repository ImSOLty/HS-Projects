package numbers;

import java.util.ArrayList;
import java.util.Arrays;

public enum Property {
    EVEN, ODD, BUZZ, DUCK, PALINDROMIC, GAPFUL, SPY, SQUARE, SUNNY, JUMPING, HAPPY, SAD,
    NONBUZZ, NONGAPFUL, NONPALINDROMIC, NONJUMPING, NONDUCK, NONSPY, NONSUNNY, NONSQUARE;

    public String[] opposite() {
        return switch (this) {
            case EVEN -> new String[]{ODD.name(), "-" + EVEN.name()};
            case ODD -> new String[]{EVEN.name(), "-" + ODD.name()};
            case BUZZ -> new String[]{NONBUZZ.name(), "-" + BUZZ.name()};
            case DUCK -> new String[]{NONDUCK.name(), SPY.name(), "-" + DUCK.name()};
            case PALINDROMIC -> new String[]{NONPALINDROMIC.name(), "-" + PALINDROMIC.name()};
            case GAPFUL -> new String[]{NONGAPFUL.name(), "-" + GAPFUL.name()};
            case SPY -> new String[]{NONSPY.name(), DUCK.name(), "-" + SPY.name()};
            case SQUARE -> new String[]{NONSQUARE.name(), SUNNY.name(), "-" + SQUARE.name()};
            case SUNNY -> new String[]{NONSUNNY.name(), SQUARE.name(), "-" + SUNNY.name()};
            case JUMPING -> new String[]{NONJUMPING.name(), "-" + JUMPING.name()};
            case HAPPY -> new String[]{SAD.name(), "-" + HAPPY.name()};
            case SAD -> new String[]{HAPPY.name(), "-" + SAD.name()};

            case NONBUZZ -> new String[]{BUZZ.name()};
            case NONGAPFUL -> new String[]{GAPFUL.name()};
            case NONPALINDROMIC -> new String[]{PALINDROMIC.name()};
            case NONJUMPING -> new String[]{JUMPING.name()};
            case NONDUCK -> new String[]{DUCK.name()};
            case NONSPY -> new String[]{SPY.name()};
            case NONSUNNY -> new String[]{SUNNY.name()};
            case NONSQUARE -> new String[]{SQUARE.name()};
        };
    }

    public boolean valid(long num) {
        switch (this) {

            case EVEN -> {
                return num % 2 == 0;
            }
            case ODD -> {
                return num % 2 == 1;
            }
            case BUZZ -> {
                return num % 10 == 7 || num % 7 == 0;
            }
            case DUCK -> {
                return Long.toString(num).contains("0");
            }
            case PALINDROMIC -> {
                return Long.toString(num).contentEquals(new StringBuilder(Long.toString(num)).reverse());
            }
            case GAPFUL -> {
                String str = Long.toString(num);
                return str.length() >= 3 && num % (Long.parseLong(String.valueOf(str.charAt(0))) * 10 + num % 10) == 0;
            }
            case SPY -> {
                long sum = 0, product = 1;
                while (num != 0) {
                    sum += num % 10;
                    product *= num % 10;
                    num = num / 10;
                }
                return sum == product;
            }
            case SQUARE -> {
                return Math.sqrt(num) == Math.round(Math.sqrt(num));
            }
            case SUNNY -> {
                return Math.sqrt(num + 1) == Math.round(Math.sqrt(num + 1));
            }
            case JUMPING -> {
                int prev = -1;
                while (num != 0) {
                    int cur = (int) (num % 10);
                    if (!(prev == -1 || Math.abs(cur - prev) == 1)) {
                        return false;
                    }
                    prev = cur;
                    num = num / 10;
                }
                return true;
            }
            case HAPPY -> {
                ArrayList<Long> checked = new ArrayList<>();
                while (true) {
                    if (num == 1) {
                        return true;
                    }
                    if (checked.contains(num)) {
                        return false;
                    }
                    checked.add(num);
                    num = Arrays.stream(String.valueOf(num).split("")).mapToInt(n -> (int) Math.pow(Integer.parseInt(n), 2)).sum();
                }
            }
            case SAD -> {
                ArrayList<Long> checked = new ArrayList<>();
                while (true) {
                    if (num == 1) {
                        return false;
                    }
                    if (checked.contains(num)) {
                        return true;
                    }
                    checked.add(num);
                    num = Arrays.stream(String.valueOf(num).split("")).mapToInt(n -> (int) Math.pow(Integer.parseInt(n), 2)).sum();
                }
            }
            case NONBUZZ -> {
                return !BUZZ.valid(num);
            }
            case NONGAPFUL -> {
                return !GAPFUL.valid(num);
            }
            case NONPALINDROMIC -> {
                return !PALINDROMIC.valid(num);
            }
            case NONJUMPING -> {
                return !JUMPING.valid(num);
            }
            case NONDUCK -> {
                return !DUCK.valid(num);
            }
            case NONSPY -> {
                return !SPY.valid(num);
            }
            case NONSUNNY -> {
                return !SUNNY.valid(num);
            }
            case NONSQUARE -> {
                return !SQUARE.valid(num);
            }
        }
        return false;
    }
}
