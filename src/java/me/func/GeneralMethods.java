/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.func;

import Entity.Player;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author JmTiong
 */
public class GeneralMethods {

  private Connection conn;

  public GeneralMethods() {
    // addPlayer();
  }

  //for sessionID
  public String getSessionIDHash(long time, String email) {
    try {
      MessageDigest md = MessageDigest.getInstance("SHA-256");
      StringBuilder sb = new StringBuilder();
      String newS = email + time;
      byte[] newHash = md.digest(newS.getBytes());
      for (byte b : newHash) {
        sb.append(String.format("%02x", b & 0xff));
      }
      System.out.println("Session Cookie Id: " + sb.toString());
      return sb.toString();
    } catch (NoSuchAlgorithmException ex) {
      System.out.println("Algorithm is wrong.");
      return "";
    }
  }

  public String generateGeneralHash(String input) {
    try {
      MessageDigest md = MessageDigest.getInstance("SHA-256");
      StringBuilder sb = new StringBuilder();
      byte[] hash = md.digest(input.getBytes());
      for (byte b : hash) {
        sb.append(String.format("%02x", b & 0xff));
      }
      System.out.println("User hash generated");
      return sb.toString();
    } catch (NoSuchAlgorithmException ex) {
      System.out.println("Algoirthm is wrong");
      return "";
    }
  }

  public String generatePassHash(String pass, String salt) {
    try {
      MessageDigest md = MessageDigest.getInstance("SHA-256");
      StringBuilder sb = new StringBuilder();
      String newP = pass + salt;
      byte[] newHash = md.digest(newP.getBytes());
      for (byte b : newHash) {
        sb.append(String.format("%02x", b & 0xff));
      }
      System.out.println("generate Password Hash" + sb.toString());
      return sb.toString();
    } catch (NoSuchAlgorithmException ex) {
      System.out.println("Algorithm is wrong.");
      return "";
    }
  }

  //for public access
  public Player getProfile(String email) {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      ResultSet rs = cd.retrievePlayer(email);
      if (rs == null) {
        return null;
      }
      if (rs.next()) {
        Player p = new Player();
        p.setEmail(rs.getString("email"));
        p.setId(rs.getLong("id"));
        p.setName(rs.getString("name"));
        p.setPoints(rs.getDouble("points"));
        //p.setQrcode(rs.getString("qrLoc"));
        p.setType(rs.getString("type"));
        rs.close();
        cd.closeConnection();
        return p;
      } else {
        rs.close();
        cd.closeConnection();
        return null;
      }
    } catch (SQLException ex) {
      Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
      return null;
    }
  }
  public int redeemCode(String code, String username) {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      ResultSet rs = cd.retrieveCode(code);
      if (rs == null) {
        System.out.println("No such code " + code);
        return 0;
      }
      if (rs.next()) {
        if (rs.getInt("redeemed") == 1) {
          System.out.println(username + " tried to redeem already redeemed code: " + code);
          return 0;
        } else {
          System.out.println("Code is valid. Redeeming by: " + username);
          //check code's character type is a multipler or not
          //set code to be redeemed
          double points = rs.getDouble("points");
          //update code table
          if (cd.updateCodeTable(code, 1)) {
            rs = cd.retrievePlayer(username);
            if (rs == null) {
              System.out.println("No such user: " + username);
              return 0;
            }
            if (!rs.next()) {
              System.out.println("User " + username + " is not found! Error!!");
              cd.updateCodeTable(code, 0);
              return 0;
            } else {
              System.out.println(points);
              points += rs.getDouble("points");
              System.out.println(points);
              //update Player table
              boolean success = cd.updatePlayerPoints(username, points);
              if (success) {
                System.out.println("Code " + code + " is successfully redeemed by: " + username);
              } else {
                System.out.println("Unknown reason why code is not successfully redeemed (Investigation required.)");
                cd.updateCodeTable(code, 0);
              }
              rs.close();
              cd.closeConnection();
              return (success) ? 1 : 0;
            }
          } else {
            rs.close();
            cd.closeConnection();
            return 0;
          }
        }
      } else {
        rs.close();
        cd.closeConnection();
        return 0;
      }
    } catch (SQLException ex) {
      Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
      return 0;
    }
  }
}

/*
 Generate new password code
 //if reset request is activated, generate new password and send to user
 char[] chars = "abcdefghijklmnopqrstuvwxyz1234567890".toCharArray();
 StringBuilder sb = new StringBuilder();
 Random random = new Random();
 for (int i = 0; i < 8; i++) {
 char c = chars[random.nextInt(chars.length)];
 sb.append(c);
 }
 //generate new salt
 int salt = random.nextInt(1000) + 100;
 //update the user database
 String pwdhash = generatePassHash(sb.toString(), Integer.toString(salt));
 succ = cd.resetPlayerPass(email, pwdhash, Integer.toString(salt));
 if (succ == 1) {
 System.out.println("User " + email + " password has successfully changed.");
 es = new EmailSender();
 String[] to = {email};
 es.sendMail("jiaming0097@gmail.com", pwd, "Your password has been changed to: " + sb.toString(), to);
 cd.closeConnection();
 } else {
 System.out.println("Password error occured.");
 return 0;
 }
 */
