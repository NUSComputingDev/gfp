package me.page;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import Entity.Player;
import me.func.GeneralMethods;
import java.io.IOException;
import java.io.PrintWriter;
import javax.servlet.ServletException;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import me.func.LoginValidation;

/**
 *
 * @author JmTiong
 */
public class Login extends HttpServlet {

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
    //System.out.println(request.getAuthType() + " |   " + request.getRemoteUser() + "  |  " + request.getRequestedSessionId() + "  |asdas! ");
    //user directly access this servlet or sends empty values to servlet
    if (!request.getParameterNames().hasMoreElements()) {
      System.out.println("Nothing end it now");
      response.sendRedirect("index.jsp"); //redirect user to the login page
      return;
    }

    LoginValidation lv = new LoginValidation();
    GeneralMethods m = new GeneralMethods();

    String user = request.getParameter("usern");
    String pass = request.getParameter("pass");
    //validating user's input
    if (!request.getParameter("usern").equals("") && !request.getParameter("pass").equals("")) {
      if (!lv.validateInput(user, pass)) {
        response.setContentType("text/plain");
        response.getWriter().write("Invalid username/password");
        response.sendError(401);
        return;
      }
    }

    //connect to database to find if user exist
    boolean allow = lv.validateUser(user, pass);
    if (!allow) {//if user does not exist or fail to login
      response.setContentType("text/plain");
      response.getWriter().write("Invalid username/password");
      response.sendError(401);
    } else {//create a session with the user
      HttpSession ses = request.getSession();
      long time = System.currentTimeMillis();
      String s = m.getSessionIDHash(time, user);
      Player p = m.getProfile(user);
      ses.setAttribute("username", user);
      ses.setAttribute("sessionID", s);
      ses.setAttribute("firstname", p.getName());
      ses.setAttribute("points", p.getPoints());
      ses.setAttribute("type", p.getType());
      ses.setMaxInactiveInterval(5 * 60);
      Cookie sessionCook = new Cookie("sc", s);
      Cookie loginCook = new Cookie("f", user);
      Cookie name = new Cookie("o", p.getName());
      //create a session record in database for future checking (need to be done)
      loginCook.setMaxAge(30 * 60);
      sessionCook.setMaxAge(30 * 60);
      name.setMaxAge(30 * 60);
      loginCook.setHttpOnly(true);
      sessionCook.setHttpOnly(true);
      name.setHttpOnly(true);
      response.addCookie(loginCook);
      response.addCookie(sessionCook);
      response.addCookie(name);
      response.setContentType("application/json");
      PrintWriter out = response.getWriter();
      out.print("{\"uName\":\"" + p.getName() + "\",\"cType\":\"" + p.getType() + "\", \"pts\":\"" + p.getPoints() + "\", \"email\":\"" + p.getEmail() + "\"}");
      out.flush();
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

}
