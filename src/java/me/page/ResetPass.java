/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package me.page;

import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import me.func.ResetMethods;

/**
 *
 * @author JmTiong
 */
public class ResetPass extends HttpServlet {

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
    try (PrintWriter out = response.getWriter()) {
      /* TODO output your page here. You may use following sample code. */
      ResetMethods rm = new ResetMethods();
      String hash = request.getParameter("hash");
      String pass = request.getParameter("pass");
      String pass1 = request.getParameter("pass1");
      System.out.println(hash + "  " + pass + "  " + pass1);
      if (pass.length() < 6 || pass1.length() < 6) {
        response.setContentType("text/plain");
        response.getWriter().write("Passwords must be more than 6 characters.");
        response.sendError(401);
        return;
      }
      if (!pass.equals(pass1)) {
        response.setContentType("text/plain");
        response.getWriter().write("Passwords do not match");
        response.sendError(401);
        return;
      }
      if (hash.equals("")) {
        response.setContentType("text/plain");
        response.getWriter().write("Invalid link.");
        response.sendError(401);
        return;
      }
      int succ = rm.requestActivate(hash, pass, pass1);

      if (succ == 0) {
        response.setContentType("text/plain");
        response.getWriter().write("Invalid request");
        response.sendError(401);
        return;
      }
      
      if(succ==1){
        response.setContentType("text/plain");
        response.getWriter().write("Password successfully changed. Redirecting to main page...");
      }

    }
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

  public void displayPage(PrintWriter out) {
    out.println("<!DOCTYPE html>");
    out.println("<html>");
    out.println("<head>");
    out.println("<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\">");
    out.println("<title>Reset Password</title>");
    out.println("<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, user-scalable=yes\">");
    out.println("<link rel='stylesheet prefetch' href='http://fonts.googleapis.com/css?family=Open+Sans'>");
    out.println("<link rel=\"stylesheet\" href=\"css/style.css\">");
    out.println("</head>");
    out.println("<body>");
    out.println("<div class=\"cont\">");
    out.println("<div class=\"demo\">");
    out.println("<div class=\"login\">");
    out.println("<div class=\"login__check\"></div>");
    out.println("<div class=\"login__form\">");
    out.println("<div class=\"login__row\">");
    out.println("<p class='login__signup' id='error'>Invalid Request... redirecting to main page in 5</p>");
    out.println("</div>");
    out.println("</div>");
    out.println("</div>");
    out.println("</div>");
    out.println("<script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>");

    out.println("    <script src=\"js/index.js\"></script>");
    out.println("<script>");
    out.println("$(document).ready(function () {"
            + "var counter = 5;"
            + "window.setTimeout(function(){\n"
            + "\n"
            + "        // Move to a new location or you can do something else\n"
            + "        window.location.replace(\"/GFP16GF/index.jsp\");\n"
            + "\n"
            + "    }, 5000);"
            + "window.setInterval(function(){\n"
            + "\n"
            + "        // Move to a new location or you can do something else\n"
            + "counter = counter - 1;\n"
            + "        $(\"#error\").text(\"Invalid Request... redirecting to main page in \"+counter+\"\");\n"
            + "\n"
            + "    }, 1000);"
            + "});");
    out.println("</script>");
    out.println("</body>");
    out.println("</html>");
  }
}
