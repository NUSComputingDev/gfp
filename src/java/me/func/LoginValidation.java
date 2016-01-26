/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.func;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 * @author JmTiong
 */
public class LoginValidation {

  private Connection conn;
  private static final String EMAIL_PATTERN
          = "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@"
          + "[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$";

  public boolean emailCheck(String email) {
    Pattern p = Pattern.compile(EMAIL_PATTERN);
    Matcher m = p.matcher(email);
    return m.matches();
  }

  public boolean validateInput(String username, String password) {
    //if the password = "randomString" means it is from validateInput() by forgotPassword();
    boolean result = false;
    if (emailCheck(username)) {
      result = true;
    }
    if (password.length() < 6) {
      result = false;
    }

    return result;
  }

  //need to validate
  public boolean validateUser(String username, String password) {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      String salt, dbHash;
      try (ResultSet rs = cd.retrievePlayer(username)) {
        if (rs == null) {
          return false;
        }
        salt = "0";
        dbHash = "";
        if (rs.next()) {
          salt = rs.getString("salt");
          dbHash = rs.getString("password");
        } else {
          System.out.println("No such user");
        }
        rs.close();
      }
      cd.closeConnection();
      GeneralMethods m = new GeneralMethods();
      return (dbHash.contentEquals(m.generatePassHash(password, salt)));
    } catch (SQLException ex) {
      Logger.getLogger(ConnectDatabase.class.getName()).log(Level.SEVERE, null, ex);
      return false;
    }
  }
  
}
