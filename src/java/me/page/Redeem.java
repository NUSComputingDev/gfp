/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.page;

import Entity.Player;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import me.func.GeneralMethods;

/**
 *
 * @author JmTiong
 */
public class Redeem extends HttpServlet {

  /**
   * Processes requests for both HTTP <code>GET</code> and <code>POST</code>
   * methods.
   *
   * @param request servlet request
   * @param response servlet response
   * @throws ServletException if a servlet-specific error occurs
   * @throws IOException if an I/O error occurs
   */
  protected void processRequest(HttpServletRequest request, HttpServletResponse response)
          throws ServletException, IOException {
    response.setContentType("text/html;charset=UTF-8");
    if (!request.getParameterNames().hasMoreElements()) {
      System.out.println("Nothing end it now, user trying to access it directly.");
      response.sendRedirect("index.jsp"); //redirect user to the login page
      return;
    }
    GeneralMethods m = new GeneralMethods();
    String code = request.getParameter("code");
    HttpSession session = request.getSession();
    if (session.getAttribute("username") == null) {
      System.out.println("Session is invalid");
      response.sendError(406);
      return;
    }
    String username = session.getAttribute("username").toString();
    int result = m.redeemCode(code, username);
    String output = "";
    Player p = m.getProfile(username);
    if (result == 1) {
      session.setAttribute("points", p.getPoints());
      output = "Code successfully redeemed.";
    } else {
      output = "Code is redeemed/invalid.";
    }
    response.setContentType("application/json");
    PrintWriter out = response.getWriter();
    out.print("{\"result\":\"" + output + "\",\"points\":\"" + p.getPoints() + "\"}");
    out.flush();
  }

  // <editor-fold defaultstate="collapsed" desc="HttpServlet methods. Click on the + sign on the left to edit the code.">
  /**
   * Handles the HTTP <code>GET</code> method.
   *
   * @param request servlet request
   * @param response servlet response
   * @throws ServletException if a servlet-specific error occurs
   * @throws IOException if an I/O error occurs
   */
  @Override
  protected void doGet(HttpServletRequest request, HttpServletResponse response)
          throws ServletException, IOException {
    processRequest(request, response);
  }

  /**
   * Handles the HTTP <code>POST</code> method.
   *
   * @param request servlet request
   * @param response servlet response
   * @throws ServletException if a servlet-specific error occurs
   * @throws IOException if an I/O error occurs
   */
  @Override
  protected void doPost(HttpServletRequest request, HttpServletResponse response)
          throws ServletException, IOException {
    processRequest(request, response);
  }

  /**
   * Returns a short description of the servlet.
   *
   * @return a String containing servlet description
   */
  @Override
  public String getServletInfo() {
    return "Short description";
  }// </editor-fold>

}
