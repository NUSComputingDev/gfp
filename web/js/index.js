$(document).ready(function () {
  var animating = false,
          submitPhase1 = 1100,
          submitPhase2 = 400,
          logoutPhase1 = 800,
          $login = $(".login"),
          $app = $(".app"),
          $forgot = $(".forgot");

  function ripple(elem, e) {
    $(".ripple").remove();
    var elTop = elem.offset().top,
            elLeft = elem.offset().left,
            x = e.pageX - elLeft,
            y = e.pageY - elTop;
    var $ripple = $("<div class='ripple'></div>");
    $ripple.css({top: y, left: x});
    elem.append($ripple);
  }
  ;

  $(document).on("click", ".login__submit", function (e) {
    if (animating)
      return;
    animating = true;
    var that = this;
    ripple($(that), e);
    $(that).addClass("processing");
    var user = $('#usern').val(),
            pass = $('#pass').val();
    $.post("login", {usern: user, pass: pass},
    function (data, status) {
      $("#uName").text("Greetings, " + data.uName);
      $("#cType").text(data.cType);
      $("#pts").text(data.pts);
      $("#email").text(data.email);
      setTimeout(function () {
        $(that).addClass("success");
        setTimeout(function () {
          $app.show();
          $app.css("top");
          $app.addClass("active");
        }, submitPhase2 - 70);
        setTimeout(function () {
          $login.hide();
          $login.addClass("inactive");
          animating = false;
          $(that).removeClass("success processing");
        }, submitPhase2);
      }, submitPhase1);
    })
            .fail(function () {
              $(that).removeClass("processing");
              $("#error").text("Invalid username/password.");
              animating = false;
            });
  });

  $(document).on("click", ".app__logout", function (e) {
    if (animating)
      return;
    $(".ripple").remove();
    animating = true;
    var that = this;
    $(that).addClass("clicked");
    $.post("Logout", {},
            function (data, status) {
              setTimeout(function () {
                $(that).addClass("success");
                setTimeout(function () {
                  $app.removeClass("active");
                  $login.show();
                  $login.css("top");
                  $login.removeClass("inactive");
                }, 0);
                setTimeout(function () {
                  $app.hide();
                  animating = false;
                  $(that).removeClass("clicked");
                }, 0);
              }, submitPhase1 - 500);
            });
  });

  $(document).on("click", "#forgetP", function (e) {
    if (animating)
      return;
    animating = true;
    var that = this;
    $(that).addClass("clicked");
    setTimeout(function () {
      $forgot.show();
      $forgot.addClass("active");
      $login.hide();
      $login.addClass("inactive");
      animating = false;
    }, submitPhase2);
  });

  $(document).on("click", "#backLogin", function (e) {
    if (animating)
      return;
    animating = true;
    var that = this;
    $(that).addClass("clicked");
    setTimeout(function () {
      $forgot.hide();
      $forgot.css("top");
      $forgot.removeClass("active");
      $login.show();
      $login.css("top");
      $login.removeClass("inactive");
      animating = false;
    }, submitPhase2);
  });

  $(document).on("click", "#redeem", function (e) {
    var code = $("#redeemCode").val();
    $.post("Redeem", {code: code}, function (data, status) {
      alert(data.result);
      $("#pts").text(data.points);
    })
            .fail(function () {
              alert("Session invalid. Please relogin.");
            })
            ;
  });

  $(document).on("click", "#forgetSub", function (e) {
    var user = $('#fusern').val();
    $.post("forgotPassword", {usern: user},
    function (data, status) {
      
    })
            .fail(function () {
            });
  });
  
  $(document).on("click", ".login__submit1", function (e) {
    if (animating)
      return;
    animating = true;
    var that = this;
    ripple($(that), e);
    $(that).addClass("processing");
    var user = $('#pass').val(),
            pass = $('#pass1').val();
    $.post("resetPass", {pass: user, pass1: pass, hash:$('#hash').val()},
    function (data, status) {
      alert(data);
      window.location.replace("/GFP16GF/index.jsp");
    })
            .fail(function (data, status) {
              $(that).removeClass("processing");
              alert("- Make sure your passwords are the same.\n- Password is more than 6 characters and less than 10 characters. ");
              animating = false;
            });
  });
});