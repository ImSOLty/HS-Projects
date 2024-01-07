package chat.client;

import java.io.DataOutputStream;
import java.io.IOException;
import java.util.Scanner;

public class OutputThread extends Thread {
  boolean running = true;
  DataOutputStream output;
  Client client;

  OutputThread(DataOutputStream stream, Client client) {
    output = stream;
    this.client = client;
  }

  public void run() {
    while (running) {
      Scanner scanner = new Scanner(System.in);
      String s = scanner.nextLine();
      if (s.equals("/exit")) {
        running = false;
      }
      try {
        output.writeUTF(s);
      } catch (IOException e) {
      }
    }
  }
}
