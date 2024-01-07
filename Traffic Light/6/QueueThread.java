import java.io.IOException;

public class QueueThread extends Thread {
    int SIZE;
    int seconds;
    int open;
    int fromStart = 0;
    int front, rear;
    String items[];
    boolean menu = true;
    boolean exit = false;

    QueueThread(int size, int interval){
        SIZE = size;
        front = -1;
        rear = -1;
        items = new String[SIZE];
        seconds = interval;
    }

    boolean isFull(){
        return front==0 && rear==SIZE-1 || front == rear+1;
    }
    boolean isEmpty(){
        return front==-1;
    }
    void enQueue(String element){
        if(isFull()){
            System.out.println("Road \"" + element + "\" was not added, queue is full!");
        }else {
            if(isEmpty()){
                front=0;
            }
            rear = (rear+1) % SIZE;
            items[rear] = element;
            System.out.print("Road '" + element + "' added");
        }
    }
    void deQueue(){
        String element;

        if(isEmpty()){
            System.out.println("Road can't be removed, queue is empty!");
            return;
        }

        element = items[front];
        if(front == rear){
            front=-1;
            rear=-1;
        }else{
            front=(front+1)%SIZE;
        }
        System.out.println("Road '" + element + "' deleted");
    }

    int calculateTime(int from, int to, int s){
        int result = (to-from)%SIZE;
        result += result<0?SIZE:0;
        if(to<from){
            int actSize = rear>front?rear-front:SIZE-front+rear;
            actSize++;
            result-=(SIZE-actSize);
        }
        result=result*seconds-(seconds-s);
        return result;
    }

    @Override
    public void run() {
        open = -1;
        int s = -1;
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
            }
            if (!isEmpty()) {
                if(s==0 || s==-1) {
                    open = open == rear ? front : (open + 1) % SIZE;
                    s = seconds;
                }
                if(!menu) {
                    int j;
                    for (j = front; j != rear; j = (j + 1) % SIZE) {
                        if (open != j) {
                            int time = calculateTime(open, j, s);
                            String color = time == 1 ? "\u001B[33m" : "\u001B[31m";
                            System.out.println(color + "Road \"" + items[j] + "\" is closed for " + time + "s." + "\u001B[0m");
                        } else {
                            System.out.println("\u001B[32m" + "Road \"" + items[j] + "\" is open for " + s + "s." + "\u001B[0m");
                        }
                    }
                    if (open != j) {
                        int time = calculateTime(open, j, s);
                        String color = time == 1 ? "\u001B[33m" : "\u001B[31m";
                        System.out.println(color + "Road \"" + items[j] + "\" is closed for " + time + "s." + "\u001B[0m");
                    } else {
                        System.out.println("\u001B[32m" + "Road \"" + items[j] + "\" is open for " + s + "s." + "\u001B[0m");
                    }
                }
                s--;
            }
            if(!menu){
                System.out.println("\nPress \"Enter\" to open menu");
            }
        }
    }
}
