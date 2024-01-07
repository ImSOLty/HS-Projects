package memorizingtool;

import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

class FileReaderInteger {
  static ArrayList<Integer> list = new ArrayList<>();

  public ArrayList<Integer> read(String fileName) {
    list.clear();
    try {
      List<String> lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
      for (String s : lines) {
        list.add(Integer.parseInt(s));
      }
    } catch (IOException e) {
      System.out.println("Error while performing command \"/readFile\"!\nDescription: File not found!");
    }
    return list;
  }
}

class FileWriterInteger {
  public void write(String fileName, ArrayList<Integer> data) {
    try {
      FileWriter fileWriter = new FileWriter(fileName);
      PrintWriter printWriter = new PrintWriter(fileWriter);
      for (Integer i : data) {
        printWriter.println(i);
      }
      printWriter.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}

class FileReaderWords {
  private final ArrayList<String> list = new ArrayList<>();

  public ArrayList<String> read(String fileName) {
    list.clear();
    try {
      List<String> lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
      for (String s : lines) {
        list.add(s);
      }
    } catch (IOException e) {
      System.out.println("Error while performing command \"/readFile\"!\nDescription: File not found!");
    }
    return list;
  }
}

class FileWriterWords {
  public void write(String fileName, ArrayList<String> data) {
    try {
      FileWriter fileWriter = new FileWriter(fileName);
      PrintWriter printWriter = new PrintWriter(fileWriter);
      for (String i : data) {
        printWriter.println(i);
      }
      printWriter.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}

class FileReaderBoolean {
  private final ArrayList<Boolean> list = new ArrayList<>();

  public ArrayList<Boolean> read(String fileName) {
    list.clear();
    try {
      List<String> lines = Files.readAllLines(Paths.get(fileName), StandardCharsets.UTF_8);
      for (String s : lines) {
        list.add(Boolean.parseBoolean(s));
      }
    } catch (IOException e) {
      System.out.println("Error while performing command \"/readFile\"!\nDescription: File not found!");
    }
    return list;
  }
}

class FileWriterBoolean {
  public void write(String fileName, ArrayList<Boolean> data) {
    try {
      FileWriter fileWriter = new FileWriter(fileName);
      PrintWriter printWriter = new PrintWriter(fileWriter);
      for (Boolean i : data) {
        printWriter.println(i);
      }
      printWriter.close();
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}