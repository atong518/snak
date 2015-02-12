// -------------------------------------------------------------------------------------------------
// CODE SNIPPET TAKEN FROM: https://gist.github.com/broinjc/db6e0ac214c355c887e5
// -------------------------------------------------------------------------------------------------

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

/*
The functions below will create a header with csrftoken
*/

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
	    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	}
    });

// -------------------------------------------------------------------------------------------------
// END CODE SNIPPET
// -------------------------------------------------------------------------------------------------

$(document).ready(function(){
  
  // disable scroll on this page
	//  $('#chat-room').on({
	  //     'mousewheel': function(e) {
	 //       if (e.target.id == 'el') return;
       //       e.preventDefault();
       //       e.stopPropagation();
       //     }
     // });

  // hit submit button on 'enter' keypress
  $('#message-input-box').keypress(function (e) {
    if (e.which == 13) {
      $('#btn-send-message').click();
      $('#message-input-box').val("");
    }
  });


  // start all threads as hidden
  $('.thread').each(function() {
    $(this).hide();
  });

  // open first thread
  populateThread($('.thread').first().attr("id").split("-")[1]);

  // send message
  $("#send-message-form").on('submit', function(event) {
    event.preventDefault(); // prevent page refresh
    sendMessage();
    var message = $('#message-input-box').val();
    var prev_messages = $('#message-content').html();

    return false;
  });  

  // listen for received messages
  //  setInterval(function() {
  // url: "send_chat_message/", // the endpoint
	 // type: "POST", // the http method
		//
  //
  //});


  // scroll down!
  scrollDown();
});

function scrollDown() {
    // scroll to bottom of chat screen
    var chat_box = $('#message-box');
    var height = chat_box[0].scrollHeight;
    chat_box.scrollTop(height);
}
