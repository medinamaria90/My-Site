
//<!--    Script for fade H1 and H2-->


function fadeIn(element) {
    try {
        var opacity = 0;
        var timer = setInterval(function() {
            if (opacity >= 1) {
                clearInterval(timer);
            }
            element.style.opacity = opacity;
            opacity += 0.05;
        }, 30);
    } catch (error) {
        // do nothing (pass)
    }
}

//Script for showing title
function showTitle() {
    var title1 = document.getElementById("title1");
    var title2 = document.getElementById("title2");
    var subtitle = document.getElementById("subtitle");
    fadeIn(title1);
    fadeIn(title2);
    setTimeout(function() {
        fadeIn(subtitle);
    }, 400);
}


  // close navbar on click
$(document).ready(function() {
  $('.navbar-nav>li>a').on('click', function(){
    $('.navbar-collapse').collapse('hide');
  });
});

//<!--SCRIPT TO SEND THE CHAT OF THE USER-->

$(document).ready(function() {
  $("#message_area").on("submit", function(event) {
    event.preventDefault();
    var rawText = $("#message-input").val();
    var userHtml = '<div class="media-chat media-chat-reverse"><div class="media-body"><p class="chat_font">' + rawText + '</p><p class="meta"></p></div></div>';
    $("#message-input").val("");
    $("#chat-content").append(userHtml);
    // Show the loader element
    $("#loader").show();
    $("#text_now").hide();
    $("#message-input").prop("disabled", true);
    var token = $("input[name='csrf_token']").attr('value')
    //En el HTML he generado un token csrf, en un input oculto. Ahora lo envío como header del ajax request.
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });
    $.ajax({
      data: {
        msg: rawText
      },
      type: "POST",
      url: "/chatting",
    }).done(function(data) {
      var botHtml = '<div class="media-chat"><img class="avatar" src="../static/images/robot.png" alt="..."><div class="media-body"><p class="chat_font">' + data + '</p><p class="meta"></p></div></div>';
      $("#chat-content").append($.parseHTML(botHtml));
      $("#loader").hide();
      $("#text_now").show();
      $("#message-input").prop("disabled", false);
    });
  });
});




