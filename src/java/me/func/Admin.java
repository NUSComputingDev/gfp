/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.func;

import Entity.Player;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 *
 * @author JmTiong
 */
public class Admin {

  private Connection conn;

  public void addPlayer() {
    try {
      ConnectDatabase cd = new ConnectDatabase();
      conn = cd.getConn();
      Player p = new Player();
      GeneralMethods m = new GeneralMethods();
      p.setEmail("jmtiong92@gmail.com");
      p.setName("Jimmy Tiong");
      p.setSalt("323");
      p.setType("U");
      p.setPassword(m.generatePassHash("haha123", p.getSalt()));
      PreparedStatement ps = conn.prepareStatement("INSERT INTO Player (id, name,email, type,points,salt,password) values (?,?,?,?,?,?,?);");
      ps.setInt(1, 2);
      ps.setString(2, p.getName());
      ps.setString(3, p.getEmail());
      ps.setString(4, p.getType());
      ps.setFloat(5, (float) p.getPoints());
      ps.setString(6, p.getSalt());
      ps.setString(7, p.getPassword());
      System.out.println(ps.execute());
      cd.closeConnection();
    } catch (SQLException ex) {
      Logger.getLogger(GeneralMethods.class.getName()).log(Level.SEVERE, null, ex);
    }
  }
}
