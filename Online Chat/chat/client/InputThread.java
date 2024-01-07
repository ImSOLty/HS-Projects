package chat.client;

import java.io.DataInputStream;
import java.io.IOException;

public class InputThread extends Thread {
  boolean running = true;
  DataInputStream input;
  InputThread(DataInputStream stream){
    input = stream;
  }
  public void run() {
    while(running){
      try {
        System.out.println(this.input.readUTF());
      } catch (IOException ignored) {
      }
    }
  }
}
