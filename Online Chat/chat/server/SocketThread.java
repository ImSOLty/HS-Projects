package chat.server;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class SocketThread extends Thread {

  enum Command {
    REGISTRATION, AUTH, LIST, CHAT, KICK, GRANT, REVOKE, UNREAD, STATS, HISTORY, NONE, MESSAGE
  }

  boolean running = true;
  DataInputStream input;
  DataOutputStream output;
  SocketThread chattingThread;
  String username = "", role = "user";
  Server server;

  SocketThread(Socket socket, Server server) throws IOException {
    input = new DataInputStream(socket.getInputStream());
    output = new DataOutputStream(socket.getOutputStream());
    this.server = server;
  }

  public void run() {
    try {
      this.output.writeUTF("Server: authorize or register");
      while (running) {
        String str = this.input.readUTF();
        if (str.equals("/exit")) {
          username = "";
          running = false;
          break;
        }

        Command command = manageCommand(str);
        if (command == Command.NONE) {
          this.output.writeUTF("Server: incorrect command!");
          continue;
        }
        if (username == "" && command != Command.REGISTRATION && command != Command.AUTH) {
          this.output.writeUTF("Server: you are not in the chat!");
          continue;
        }
        if (username == "") {
          Pattern patternReg = Pattern.compile("/registration (.*) (.*)");
          Matcher matcherReg = patternReg.matcher(str);
          Pattern patternAuth = Pattern.compile("/auth (.*) (.*)");
          Matcher matcherAuth = patternAuth.matcher(str);

          if (matcherReg.matches()) {
            register(matcherReg.group(1), matcherReg.group(2));
          } else if (matcherAuth.matches()) {
            authenticate(matcherAuth.group(1), matcherAuth.group(2));
          } else {
            this.output.writeUTF("Server: incorrect command!");
          }
          continue;
        }

        switch (command) {
          case REGISTRATION:
          case AUTH:
            this.output.writeUTF("Server: incorrect command!");
            break;
          case LIST:
            list();
            break;
          case CHAT:
            Pattern patternChat = Pattern.compile("/chat (.*)");
            Matcher matcherChat = patternChat.matcher(str);
            if (matcherChat.matches()) {
              chat(matcherChat.group(1));
            } else {
              this.output.writeUTF("Server: incorrect command!");
            }
            break;
          case KICK:
            Pattern patternKick = Pattern.compile("/kick (.*)");
            Matcher matcherKick = patternKick.matcher(str);
            if (matcherKick.matches()) {
              kick(matcherKick.group(1));
            } else {
              this.output.writeUTF("Server: incorrect command!");
            }
            break;
          case GRANT:
            Pattern patternGrant = Pattern.compile("/grant (.*)");
            Matcher matcherGrant = patternGrant.matcher(str);
            if (matcherGrant.matches()) {
              grant(matcherGrant.group(1));
            } else {
              this.output.writeUTF("Server: incorrect command!");
            }
            break;
          case REVOKE:
            Pattern patternRevoke = Pattern.compile("/revoke (.*)");
            Matcher matcherRevoke = patternRevoke.matcher(str);
            if (matcherRevoke.matches()) {
              revoke(matcherRevoke.group(1));
            } else {
              this.output.writeUTF("Server: incorrect command!");
            }
            break;
          case UNREAD:
            unread();
            break;
          case STATS:
            stats();
            break;
          case HISTORY:
            Pattern patternHistory = Pattern.compile("/history (.*)");
            Matcher matcherHistory = patternHistory.matcher(str);
            if (matcherHistory.matches()) {
              history(matcherHistory.group(1));
            } else {
              this.output.writeUTF("Server: incorrect command!");
            }
            break;
          default:
            if (chattingThread != null) {
              if (chattingThread.chattingThread == this) {
                this.output.writeUTF(username + ": " + str);
                this.chattingThread.output.writeUTF(username + ": " + str);
                server.messages.add(new Server.Message(username, chattingThread.username, str, true));
                server.writeMessageToFile(username + "~" + chattingThread.username + "~" + str + "~" + "true");
              } else {
                this.output.writeUTF(username + ": " + str);
                server.messages.add(new Server.Message(username, chattingThread.username, str, false));
                server.writeMessageToFile(username + "~" + chattingThread.username + "~" + str + "~" + "false");
              }
            } else {
              this.output.writeUTF("Server: use /list command to choose a user to text!");
            }
        }
      }
    } catch (IOException ignored) {
    }
  }

  Command manageCommand(String str) {
    if (str.startsWith("/")) {
      switch (str.split(" ")[0]) {
        case "/registration":
          return Command.REGISTRATION;
        case "/auth":
          return Command.AUTH;
        case "/list":
          return Command.LIST;
        case "/chat":
          return Command.CHAT;
        case "/kick":
          return Command.KICK;
        case "/grant":
          return Command.GRANT;
        case "/revoke":
          return Command.REVOKE;
        case "/unread":
          return Command.UNREAD;
        case "/stats":
          return Command.STATS;
        case "/history":
          return Command.HISTORY;
        default:
          return Command.NONE;
      }
    }
    return Command.MESSAGE;
  }

  void register(String login, String password) throws IOException {
    for (Server.Account acc : server.accounts) {
      if (acc.name.equals(login)) {
        this.output.writeUTF("Server: this login is already taken! Choose another one.");
        return;
      }
    }
    if (password.length() < 8) {
      this.output.writeUTF("Server: the password is too short!");
      return;
    }
    this.output.writeUTF("Server: you are registered successfully!");
    username = login;
    role = "user";
    server.accounts.add(new Server.Account(login, password, "user"));
    server.writeUsersToFile();
  }

  void authenticate(String login, String password) throws IOException {
    for (Server.Account acc : server.accounts) {
      if (acc.name.equals(login)) {
        if (acc.kicked) {
          this.output.writeUTF("Server: you are banned!");
          return;
        }
        if (!acc.password.equals(password)) {
          this.output.writeUTF("Server: incorrect password!");
          return;
        }
        this.output.writeUTF("Server: you are authorized successfully!");
        username = login;
        role = acc.role;
        return;
      }
    }
    this.output.writeUTF("Server: incorrect login!");
  }

  void list() throws IOException {
    List<String> online = new ArrayList<>();
    for (SocketThread socketThread : server.threads) {
      if (socketThread != this && !socketThread.username.equals("") && socketThread.running) {
        online.add(socketThread.username);
      }
    }
    if (online.isEmpty()) {
      this.output.writeUTF("Server: no one online");
    } else {
      this.output.writeUTF("Server: online: " + String.join(" ", online));
    }
  }

  void chat(String s) throws IOException {
    boolean found = false;
    for (SocketThread socketThread : server.threads) {
      if (socketThread.username.equals(s)) {
        chattingThread = socketThread;
        found = true;
        for (String message : getLastMessages(10, false)) {
          this.output.writeUTF(message);
        }
        break;
      }
    }

    if (!found) {
      this.output.writeUTF("Server: the user is not online!");
    }
  }

  void kick(String s) throws IOException {
    if (s.equals(username)) {
      this.output.writeUTF("Server: you can't kick yourself!");
      return;
    }
    if (role.equals("user")) {
      this.output.writeUTF("Server: you are not a moderator or an admin!");
      return;
    }
    SocketThread target = null;
    for (SocketThread socketThread : server.threads) {
      if (socketThread.username.equals(s)) {
        target = socketThread;
      }
    }
    if (target == null) {
      this.output.writeUTF("Server: the user is not online!");
      return;
    }
    if (role.equals("mod") && (target.role.equals("mod") || target.role.equals("admin"))) {
      this.output.writeUTF("Server: you can not kick another mod");
      return;
    }
    this.output.writeUTF("Server: " + s + " was kicked!");

    for (Server.Account account : server.accounts) {
      if (account.name.equals(s)) {
        account.Kick();
        server.writeUsersToFile();
        break;
      }
    }
    target.output.writeUTF("Server: you have been kicked out of the server!");
    target.username="";
  }

  void grant(String s) throws IOException {
    if (!role.equals("admin")) {
      this.output.writeUTF("Server: you are not an admin!");
      return;
    }
    SocketThread target = null;
    for (SocketThread socketThread : server.threads) {
      if (socketThread.username.equals(s)) {
        target = socketThread;
      }
    }
    if (target == null) {
      this.output.writeUTF("Server: the user is not online!");
      return;
    }
    if (target.role.equals("mod")) {
      this.output.writeUTF("Server: this user is already a moderator!");
      return;
    }
    this.output.writeUTF("Server: " + s + " is the new moderator!");
    target.output.writeUTF("Server: you are the new moderator now!");
    for (Server.Account account : server.accounts) {
      if (account.name == target.username) {
        account.role = "mod";
        target.role = "mod";
        server.writeUsersToFile();
        break;
      }
    }
  }

  void revoke(String s) throws IOException {
    if (!role.equals("admin")) {
      this.output.writeUTF("Server: you are not an admin!");
      return;
    }
    SocketThread target = null;
    for (SocketThread socketThread : server.threads) {
      if (socketThread.username.equals(s)) {
        target = socketThread;
      }
    }
    if (target == null) {
      this.output.writeUTF("Server: the user is not online!");
      return;
    }
    if (!target.role.equals("mod")) {
      this.output.writeUTF("Server: this user is not a moderator!");
      return;
    }
    this.output.writeUTF("Server: " + s + " is no longer a moderator!");
    target.output.writeUTF("Server: you are no longer a moderator!");
    for (Server.Account account : server.accounts) {
      if (account.name == target.username) {
        account.role = "user";
        target.role = "user";
        server.writeUsersToFile();
        break;
      }
    }
  }

  void unread() throws IOException {
    List<String> unread = new ArrayList<>();
    for (Server.Message m : server.messages) {
      if (m.to.equals(username) && !m.read && !unread.contains(m.from)) {
        unread.add(m.from);
      }
    }

    if (unread.isEmpty()) {
      this.output.writeUTF("Server: no one unread");
    } else {
      unread.sort(Comparator.naturalOrder());
      this.output.writeUTF("Server: unread from: " + String.join(" ", unread));
    }
  }

  void stats() throws IOException {
    int fromYou = 0, toYou = 0;
    if (chattingThread != null) {
      for (Server.Message m : server.messages) {
        if (m.to.equals(username) && m.from.equals(chattingThread.username)) {
          toYou++;
        }
        if (m.from.equals(username) && m.to.equals(chattingThread.username)) {
          fromYou++;
        }
      }
      this.output.writeUTF("Server:\n" +
              "Statistics with " + chattingThread.username + ":\n" +
              "Total messages: " + (fromYou + toYou) + "\n" +
              "Messages from " + username + ": " + fromYou + "\n" +
              "Messages from " + chattingThread.username + ": " + toYou);
    }
  }

  void history(String s) throws IOException {
    int n=0;
    try {
      n = Integer.parseInt(s);
    }catch(Exception e){
      this.output.writeUTF("Server: "+ s+" is not a number!");
      return;
    }
    this.output.writeUTF("Server:");
    for (String message : getLastMessages(n, true)) {
      this.output.writeUTF(message);
    }
  }

  List<String> getLastMessages(int n, boolean history) {

    int amountOfNew = 0;
    List<String> ret = new ArrayList<>();
    for (Server.Message message : server.messages) {
      if (message.to.equals(chattingThread.username) && message.from.equals(username)) {
        ret.add(message.toString());
      }
      if (message.to.equals(username) && message.from.equals(chattingThread.username)) {
        if (!message.read) {
          ret.add("(new) " + message.toString());
          amountOfNew++;
          message.read = true;
        } else {
          ret.add(message.toString());
        }
      }
    }
    if(!history) {
      if (amountOfNew < 15) {
        return ret.subList(Math.max(ret.size() - (n + amountOfNew),0), ret.size());
      } else {
        return ret.subList(Math.max(ret.size() - 25,0), ret.size());
      }
    }else{
      return ret.subList(Math.max(ret.size() - n,0), ret.size()-n+25);
    }
  }
}
