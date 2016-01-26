<%-- 
    Document   : link
    Created on : Jan 19, 2016, 2:40:15 PM
    Author     : JmTiong
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Reset Password</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=yes">
    <link rel='stylesheet prefetch' href='http://fonts.googleapis.com/css?family=Open+Sans'>
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <div class="cont">
      <div class="demo">
        <div class="login">
          <div class="login__check"></div>
          <div class="login__form">
            <div class="login__row">
              <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
              <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
              </svg>
              <input type="password" id="pass" class="login__input pass" placeholder="Enter password"/>
            </div>
            <div class="login__row">
              <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
              <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
              </svg>
              <input type="password" id="pass1" class="login__input pass" placeholder="Enter password again"/>
            </div>
            <button type="button" class="login__submit1">Reset Password</button>
            <p class='login__signup' id='error'></p>
          </div>
        </div>
      </div>
    </div>
    <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>
  </body>
</html>
