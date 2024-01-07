package traffic;

import java.io.IOException;

public class QueueThread extends Thread {
    int SIZE;
    int seconds;
    int fromStart = 0;
    boolean menu = true;
    boolean exit = false;

    QueueThread(int size, int interval){
        SIZE = size;
        seconds = interval;
    }

    @Override
    public void run() {

        while (!exit) {
            try {
                this.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            fromStart++;
            if(!menu) {
                try {
                    if (System.getProperty("os.name").contains("Windows"))
                        new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
                    else
                        Runtime.getRuntime().exec("clear");
                } catch (IOException | InterruptedException e) {
                }
                System.out.println("! " + fromStart + "s. have passed since system startup !");
                System.out.println("! Number of roads: " + SIZE + " !");
                System.out.println("! Interval: " + seconds + " !\n");
                System.out.println("\nPress \"Enter\" to open menu");
            }
        }
    }
}
