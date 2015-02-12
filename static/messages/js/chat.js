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

function populateThread(threadId) {
    // hide all threads
    $('.thread').each(function() {
	    $(this).hide();
	});
    
    // show individual thread
    id = "#thread-" + threadId;
    $(id).show();
    
    // deactivate all thread links
    $('.inbox-message').each(function() {
	    $(this).removeClass("active-link");
	});
    
    // activate individual thread link
    thread_link = "#thread-link-" + threadId;
    $(thread_link).addClass("active-link");
    
    // scroll down
    scrollDown();
}
function sendMessage() {
    // get id of the thread that is activated
    var selectedThreadId = $(".active-link").attr("id");
    
    // ensure that there is a thread activated
    if (typeof selectedThreadId == "undefined") {
	alert(selectedThreadId);
    }
    else {
	selectedThreadId = selectedThreadId.split("-")[2];
    }
    
    // get text of message to be sent
    var message_text = $("#message-input-box").val();
    
    $.ajax({
	    url : "send_chat_message/", // the endpoint
		type : "POST", // http method
		data : { message_text : message_text,
		    thread_id : selectedThreadId }, // data sent with the post request
		
	      // handle a successful response
	      success : function(json) {
		if (typeof json.ignore != "undefined") return;
		_sendMessageToDjango(json, selectedThreadId);
	    },
		
	      // handle a non-successful response
	      error : function(xhr,errmsg,err) {
		$('#message-content').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
					   " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	    }
	});
}

function _sendMessageToDjango(json, selectedThreadId) {
    var prev_messages = $('#thread-' + selectedThreadId).html();
    var append = '<div class="row" style="margin-top: 10px;">';
    
    var userEmail = getLoggedInUserEmail();
    if (json.sender == userEmail) {
	append += '<div class="btn btn-primary pull-right disabled">';
    }
    else {
	append += '<div class="btn btn-default disabled">';
    }
    append += json.text + '</div></div>';
    console.log("append:" + append);
    $('#thread-' + selectedThreadId).html(prev_messages + append);
    
    $('#message-input-box').val(''); // remove the value from the input
    $('#message-content').html();
    console.log(json); // log the returned json to the console
    console.log("huzzah"); // another sanity check
    
    // scroll down!
    scrollDown();
}