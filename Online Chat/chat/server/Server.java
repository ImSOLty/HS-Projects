package chat.server;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;

public class Server extends Thread {
  static String usersdb = "usersdb.txt";
  static String messagedb = "messagedb.txt";

  static class Message {
    String from, to;
    String message;
    boolean read;

    public Message(String from, String to, String message, boolean read) {
      this.from = from;
      this.to = to;
      this.message = message;
      this.read = read;
    }

    @Override
    public String toString() {
      return from + ": " + message;
    }
  }

  static class Account {
    String name;
    String password;
    String role;
    boolean kicked;

    public Account(String name, String password, String role) {
      this.name = name;
      this.password = password;
      this.role = role;
      this.kicked = false;
    }

    public Account(String name, String password, String role, boolean kicked) {
      this.name = name;
      this.password = password;
      this.role = role;
      this.kicked = kicked;
    }

    public void Kick(){
      kicked=true;
    }
  }

  List<Message> messages = new ArrayList<>();
  List<Account> accounts = new ArrayList<>();
  List<SocketThread> threads = new ArrayList<>();

  public static void main(String[] args) {
    Server thread = new Server();
    thread.start();
    System.out.println("Server started!");
    try {
      thread.join();
    } catch (Exception e) {

    }
  }

  public void run() {
    String address = "127.0.0.1";
    int port = 23456;
    ServerSocket server = null;
    try {
      this.importFromFiles();
      server = new ServerSocket(port, 50, InetAddress.getByName(address));
      while (true) {
        Socket socket = server.accept();
        SocketThread thread = new SocketThread(socket, this);
        thread.start();
        threads.add(thread);
      }
    } catch (Exception e) {
      System.out.println(e.getMessage());
    }
  }

  public void writeUsersToFile() throws IOException {
    BufferedWriter writer = new BufferedWriter(new FileWriter(usersdb));
    for(Account acc : accounts){
      writer.write(acc.name+"~"+acc.password+"~"+acc.role+"~"+acc.kicked+"\n");
    }
    writer.close();
  }

  public void writeMessageToFile(String str) throws IOException {
    BufferedWriter writer = new BufferedWriter(new FileWriter(messagedb, true));
    writer.write(str+"\n");
    writer.close();
  }

  public void importFromFiles() throws IOException {
    try {
      Scanner scanner = new Scanner(new File(usersdb));
      while (scanner.hasNextLine()) {
        String[] data = scanner.nextLine().split("~");
        accounts.add(new Account(data[0], data[1], data[2], !data[3].equals("false")));
      }
      scanner = new Scanner(new File(messagedb));
      while (scanner.hasNextLine()) {
        String[] data = scanner.nextLine().split("~");
        messages.add(new Message(data[0], data[1], data[2], !data[3].equals("false")));
      }
    }catch(Exception e){
      accounts.add(new Account("admin","12345678", "admin"));
      writeUsersToFile();
    }
  }
}
