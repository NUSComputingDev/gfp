<%-- 
    Document   : profilePage
    Created on : Jan 11, 2016, 12:17:01 PM
    Author     : JmTiong
--%>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html >
  <head>
    <meta charset="UTF-8">
    <title>Graduates' Farewell Party</title>
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
              <svg class="login__icon name svg-icon" viewBox="0 0 20 20">
              <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
              </svg>
              <input type="text" id="usern" class="login__input name" placeholder="Username"/>
            </div>
            <div class="login__row">
              <svg class="login__icon pass svg-icon" viewBox="0 0 20 20">
              <path d="M0,20 20,20 20,8 0,8z M10,13 10,16z M4,8 a6,8 0 0,1 12,0" />
              </svg>
              <input type="password" id="pass" class="login__input pass" placeholder="Password"/>
            </div>
            <button type="button" class="login__submit">Sign in</button>
            <a class="login__signup" id="forgetP" href="#">Forget Password</a>
            <p class='login__signup' id='error'></p>
          </div>
        </div>

        <div class='forgot'>
          <div class="login__check"></div>
          <div class="forget__form">
            <div class="login__row">
              <svg class="login__icon name svg-icon" viewBox="0 0 20 20">
              <path d="M0,20 a10,8 0 0,1 20,0z M10,0 a4,4 0 0,1 0,8 a4,4 0 0,1 0,-8" />
              </svg>
              <input type="text" id="fusern" class="login__input name" placeholder="Username"/>
            </div>
            <button type="button" class="forgot__submit" id='forgetSub'>Reset Password</button>
            <a class='login__signup' id='backLogin' href='#'>Back to Login</a>
            <p class='login__signup' id='error'>
              <%if (request.getAttribute("response") != null) {
                out.print("Invalid request...");
              }%></p>
          </div>
        </div>

        <div class="app">
          <div class="app__top">
            <div class="app__menu-btn">
              <span></span>
            </div>
            <div>
              <input type="text" id="redeemCode" class="app__input" placeholder="Redeem Code"/>
              <svg class="app__icon search svg-icon" viewBox="0 0 20 20" id='redeem'>
              <!-- yeap, its purely hardcoded numbers straight from the head :D (same for svg above) -->
              <path d="M20,20 15.36,15.36 a9,9 0 0,1 -12.72,-12.72 a 9,9 0 0,1 12.72,12.72" />
              </svg>

            </div>

            <p class="app__hello" id='uName'>Greetings, <%out.print(session.getAttribute("firstname"));%></p>
            <div class="app__user">
              <img src="//s3-us-west-2.amazonaws.com/s.cdpn.io/142996/profile/profile-512_5.jpg" alt="" class="app__user-photo" />
              <span class="app__user-notif">Qr Code</span>
            </div>
            <div class="app__month">
              <span class="app__month-btn left"></span>
              <p class="app__month-name" id='cType'>Character Type</p>
              <span class="app__month-btn right"></span>
            </div>
          </div>
          <div class="app__bot">
            <div class="app__days">
              <div class="app__day weekday">Points</div>
              <div class="app__day weekday">Email</div>
              <div class="app__day date" id='pts'>0</div>
              <div class="app__day date" id='email'></div>
            </div>
            <div class="app__meetings">
              <div class="app__meeting">
                <img src="//s3-us-west-2.amazonaws.com/s.cdpn.io/142996/profile/profile-512_5.jpg" alt="" class="app__meeting-photo" />
                <p class="app__meeting-name">Feed the cat!</p>
                <p class="app__meeting-info">
                  <span class="app__meeting-time">1 - 3pm</span>
                  <span class="app__meeting-place">Real-life</span>
                </p>
              </div>
              <div class="app__meeting">
                <img src="//s3-us-west-2.amazonaws.com/s.cdpn.io/142996/profile/profile-512_5.jpg" alt="" class="app__meeting-photo" />
                <p class="app__meeting-name">FEED THIS CAT ALREADY!!!</p>
                <p class="app__meeting-info">
                  <span class="app__meeting-time">This button is just for demo ></span>
                </p>
              </div>
            </div>
          </div>
          <div class="app__logout">
            <svg class="app__logout-icon svg-icon" viewBox="0 0 20 20">
            <path d="M6,3 a8,8 0 1,0 8,0 M10,0 10,12"/>
            </svg>
          </div>
        </div>
      </div>
    </div>
    <script src='http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js'></script>

    <script src="js/index.js"></script>

    <%
      if (session.getAttribute("username") != null) {
        System.out.println(session.getAttribute("username") + " has reloaded the page");
    %>
    <script>
      $(document).ready(function () {
        var $login = $(".login"),
                $app = $(".app");
        $app.show();
        $app.css("top");
        $app.addClass("active");
        $login.hide();
        $login.addClass("inactive");
        $("#email").text("<%out.print(session.getAttribute("username"));%>");
        $("#pts").text("<%out.print(session.getAttribute("points"));%>");
        $("#cType").text("<%out.print(session.getAttribute("type"));%>");
      });
    </script>
    <%
      }
    %>
  </body>
</html>

