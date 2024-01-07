import java.io.IOException;

public class QueueThread extends Thread {
    int SIZE;
    int seconds;
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

                if (!isEmpty()) {
                    int j;
                    for (j = front; j != rear; j = (j + 1) % SIZE) {
                        System.out.println("Road \"" + items[j] + "\"");
                    }
                    System.out.println("Road \"" + items[j] + "\"");
                }

                System.out.println("\nPress \"Enter\" to open menu");
            }
        }
    }
}
