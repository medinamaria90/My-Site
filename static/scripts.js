
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
    console.log("Before AJAX request"); // Print a message before making the AJAX request
    $("#loader").show();
    $("#text_now").hide();
    $("#message-input").prop("disabled", true);
    var token = $("input[name='csrf_token']").attr('value')
    console.log(token); // Print the token so we check it works
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
      console.log("Received response from server:", data); // Print the response from the server
      var botHtml = '<div class="media-chat"><img class="avatar" src="../static/images/robot.png" alt="..."><div class="media-body"><p class="chat_font">' + data + '</p><p class="meta"></p></div></div>';
      $("#chat-content").append($.parseHTML(botHtml));
      $("#loader").hide();
      $("#text_now").show();
      $("#message-input").prop("disabled", false);
    });
  });
});




//Script to display some text
function displaytext(){
const programmingHeading = document.getElementById("programming_h5");
  const moreProjectsHeading = document.getElementById("more_projects_");
  const programmingText = "Back-end development (Flask, MySql), Front-end development (HTML, CSS, Javascript). GUI apps with python. Web scraping, automating and more. I can also design a Chatbot for you. Go check my projects and try my chatbot! :)";
  const moreProjectsText = "More projects on the way =)";
  let iProgramming = 0;
  let iMoreProjects = 0;
  let delay = 60; // Delay in milliseconds
  function displayProgrammingText() {
    if (iProgramming < programmingText.length) {
      programmingHeading.textContent = programmingText.substring(0, iProgramming+1);
      iProgramming++;
      setTimeout(displayProgrammingText, delay);
    } else {
      // Reset text when done
      setTimeout(() => {
        programmingHeading.textContent = "";
        iProgramming = 0;
        displayProgrammingText();
      }, 2500); // Delay before resetting in milliseconds
    }
  }
  function displayMoreProjectsText() {
    if (iMoreProjects < moreProjectsText.length) {
      moreProjectsHeading.textContent = moreProjectsText.substring(0, iMoreProjects+1);
      iMoreProjects++;
      setTimeout(displayMoreProjectsText, delay);
    } else {
      // Reset text when done
      setTimeout(() => {
        moreProjectsHeading.textContent = "";
        iMoreProjects = 0;
        displayMoreProjectsText();
      }, 2500); // Delay before resetting in milliseconds
    }
  }
  displayProgrammingText();
  displayMoreProjectsText();
}

