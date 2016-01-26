/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.func;

import Entity.Secrets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
//import javax.jms.Connection;

/**
 *
 * @author JmTiong
 */
public class ConnectDatabase {

  private final String JDBC_DRIVER = "com.mysql.jdbc.Driver";
  private final String DB_URL = "jdbc:mysql://localhost:3306/gfp";
  private PreparedStatement ps;
  private Connection conn;

  public ConnectDatabase() {
    newConnection();
    ps = null;
  }

  private void newConnection() {
    try {
      Class.forName(JDBC_DRIVER);
      System.out.println("Connecting to database");
      Secrets s = new Secrets();
      conn = DriverManager.getConnection(DB_URL, s.getDatabaseUser(), s.getDatabasePwd());
    } catch (SQLException ex) {
      System.out.println("Unable to connect to database");
    } catch (ClassNotFoundException ex) {
      System.out.println("Driver is invalid");
    }
  }

  public void closeConnection() {
    if (conn != null) {
      try {
        conn.close();
        System.out.println("Connection closed.");
      } catch (SQLException ex) {
        Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      }
    }
  }

  public Connection getConn() {
    return conn;
  }

  public boolean updateCodeTable(String code, int value) {
    try {
      ps = conn.prepareStatement("UPDATE Code SET redeemed = ? WHERE code = ?;");
      ps.setInt(1, value);
      ps.setString(2, code);
      return ps.executeUpdate() != 0;
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return false;
    }
  }

  public boolean updatePlayerPoints(String username, double points) {
    try {
      ps = conn.prepareStatement("UPDATE Player SET points = ? WHERE email = ?;");
      ps.setDouble(1, points);
      ps.setString(2, username);
      boolean success = ps.executeUpdate() != 0;
      if (success) {
        System.out.println("Points are updated successfully for: " + username);
      }
      return success;
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return false;
    }
  }

  public ResultSet retrievePlayer(String username) {
    try {
      ps = conn.prepareStatement("SELECT * FROM Player where email=?;");
      ps.setString(1, username);
      return ps.executeQuery();
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return null;
    }
  }

  public ResultSet retrieveCode(String code) {
    try {
      ps = conn.prepareStatement("SELECT * FROM Code where code=?;");
      ps.setString(1, code);
      return ps.executeQuery();
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return null;
    }
  }

  public String addResetRequest(String email, int randomNo) {
    try {
      int succ = 0;
      String hash = "";
      long time;
      do {
        time = System.currentTimeMillis();
        hash = generateRequestHash(email, randomNo, time);
        ps = conn.prepareStatement("SELECT * FROM RESETREQUEST WHERE hash = ?;");
        ps.setString(1, hash);
        try (ResultSet rs = ps.executeQuery()) {
          if (rs.next()) {
            System.out.println("aweawe " + rs.getString("hash") + "  ");
            succ = 0;
          } else {
            succ = 1;
          }
        }
      } while (succ == 0);
      ps = conn.prepareStatement("INSERT INTO resetrequest (hash, email, isActivated, timeCreated) VALUES (?,?,?,?);");
      ps.setString(1, hash);
      ps.setString(2, email);
      ps.setInt(3, 0);
      ps.setLong(4, time);
      succ = ps.executeUpdate();
      if (succ == 1) {
        return hash;
      } else {
        return "";
      }
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return "";
    }
  }

  public String generateRequestHash(String email, int randomNo, long time) {
    try {
      MessageDigest md = MessageDigest.getInstance("SHA-256");
      StringBuilder sb = new StringBuilder();
      String form = email + randomNo + time;
      byte[] newHash = md.digest(form.getBytes());
      for (byte b : newHash) {
        sb.append(String.format("%02x", b & 0xff));
      }
      System.out.println("Generate Request Hash " + sb.toString());
      return sb.toString();
    } catch (NoSuchAlgorithmException ex) {
      System.out.println("Algorithm is wrong.");
      return "";
    }
  }

  public int updateResetRequest(String hash, int value) {
    try {
      ps = conn.prepareStatement("UPDATE resetrequest SET isActivated = ? WHERE hash = ?;");
      ps.setInt(1, value);
      ps.setString(2, hash);
      return ps.executeUpdate();
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return 0;
    }
  }

  public ResultSet getResetRequest(String hash) {
    try {
      ps = conn.prepareStatement("SELECT * FROM resetrequest WHERE hash = ?;");
      ps.setString(1, hash);
      return ps.executeQuery();
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return null;
    }
  }

  public int resetPlayerPass(String email, String hash, String salt) {
    try {
      ps = conn.prepareStatement("UPDATE PLAYER SET password = ?, salt=? WHERE email = ?;");
      ps.setString(1, hash);
      ps.setString(2, salt);
      ps.setString(3, email);
      return ps.executeUpdate();
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return 0;
    }
  }

}
