package chat.client;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.InetAddress;
import java.net.Socket;

public class Client extends Thread {
  public static void main(String[] args) {
    Client thread = new Client();
    System.out.println("Client started!");
    thread.start();
    try {
      thread.join();
    } catch (Exception e) {
    }
  }

  public void run() {
    String address = "127.0.0.1";
    int port = 23456;
    Socket socket = null;
    try {
      socket = new Socket(InetAddress.getByName(address), port);
      DataInputStream input = new DataInputStream(socket.getInputStream());
      DataOutputStream output = new DataOutputStream(socket.getOutputStream());

      InputThread inputThread = new InputThread(input);
      OutputThread outputThread = new OutputThread(output, this);

      inputThread.start();
      outputThread.start();
      outputThread.join();

      inputThread.running=false;
      input.close();

    } catch (Exception e) {
    }
  }
}
