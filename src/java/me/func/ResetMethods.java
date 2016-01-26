/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.func;

import Entity.Secrets;
import email.EmailSender;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.Random;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.ejb.EJB;

/**
 *
 * @author JmTiong
 */
public class ResetMethods {

  @EJB
  private EmailSender es;
  private Connection conn;

  public int resetPassword(String email) {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      ResultSet rs = cd.retrievePlayer(email);
      if (rs == null) {
        System.out.println("No such user \"" + email + "\", returning...");
        return 0;
      }
      if (rs.next()) {
        Random r = new Random();
        int randomNo = r.nextInt(1000) + 100;
        String successful = cd.addResetRequest(email, randomNo);
        if (!successful.equals("")) {
          System.out.println("Added reset request to database, sending email verification.");
          //get the hash to send to user
          es = new EmailSender();
          String[] to = {email};
          Secrets s = new Secrets();
          es.sendMail(s.getDatabaseUser(), s.getDatabasePwd(), "Please go to this link and change your password www.something.com/?link=" + successful, to);
          cd.closeConnection();
          return 1;
        } else {
          System.out.println("ran here");
        }
      } else {
        System.out.println("No such user \"" + email + "\", returning...");
      }
    } catch (SQLException ex) {
      Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
    }

    return 0;
  }

  public int resetRequestCheck(String hash) {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      ResultSet rs = cd.getResetRequest(hash);
      if (rs.next()) {
        int isActivated = rs.getInt("isActivated");
        if (isActivated == 1) {
          //invalid request, code has been redeemed
          cd.closeConnection();
          return 0;
        } else {
          //a valid request
          cd.closeConnection();
          return 1;
        }
      } else {//if there is no such request
        cd.closeConnection();
        return 0;
      }
    } catch (SQLException ex) {
      Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
      return 0;
    }
  }

  public int requestActivate(String hash, String pass, String pass1) {

    int validHash = resetRequestCheck(hash);
    if (validHash == 0) {
      return 0;
    }
    ConnectDatabase cd = new ConnectDatabase();
    conn = cd.getConn();
    ResultSet rs = cd.getResetRequest(hash);
    if (pass.equals(pass1) && pass.length() > 6 && pass.length() < 10) {
      try {
        if (rs.next()) {
          String email = rs.getString("email");
          //generate new salt
          Random random = new Random();
          int salt = random.nextInt(1000) + 100;
          GeneralMethods m = new GeneralMethods();
          String passHash = m.generatePassHash(pass, Integer.toString(salt));
          int succPass = cd.resetPlayerPass(email, passHash, Integer.toString(salt));
          if (succPass == 0) {
            System.out.println("Some where error in reset Player pass..");
            return 0;
          } else {
            cd.updateResetRequest(hash, 1);
            return 1;
          }
        }
      } catch (SQLException ex) {
        Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
        return 0;
      }
    }
    return 0;
  }
}
