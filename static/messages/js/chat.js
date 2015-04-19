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

var SET_INTERVAL;

$(document).ready(function(){
   // hit submit button on 'enter' keypress
  $('#message-input-box').keypress(function (e) {
    if (e.which == 13) {
      $('#btn-send-message').submit();
      return false;
    }

  });

  window.onload = function() {
    // TODO don't fadeout if person was nudged
    $("#alert-message").delay(3000).fadeOut();
  }

  // start all threads as hidden
  $('.thread').each(function() {
    $(this).hide();
  });

  function updateModal(data) {
      if(data){
        $("#modal-intro")[0].innerHTML = data.intro
        $("#new-thread-form").attr('otherid', data.id)    
        $('#newMatchModal').modal('show');
      } else {
        $('#noNewMatchModal').modal('show');
      }
  }

  $("#match-me").submit(function(event) {
    event.preventDefault();
    deferred = $.get("/match/", {})

    deferred.success(function (response) {
      possibles = response.possibles
      current_index = 0
      updateModal(possibles[current_index])
      $("#leftMatch")[0].setAttribute("disabled", true)
      if (current_index >= possibles.length-1) {
        $("#rightMatch")[0].setAttribute("disabled", true)
      }
    });

    deferred.error(function (response) {});

  });

  manageButtons = function(current_index) {
    if(current_index == possibles.length-1) {
      $("#rightMatch")[0].setAttribute("disabled", true)
    } else {
      $("#rightMatch")[0].removeAttribute("disabled")
    }

    if(current_index == 0) {
      $("#leftMatch")[0].setAttribute("disabled", true)
    } else {
      $("#leftMatch")[0].removeAttribute("disabled")
    }
  }

  $("#leftMatch").click(function(event) {
    current_index -= 1;
    updateModal(possibles[current_index]);
    manageButtons(current_index);
  });

  $("#rightMatch").click(function(event) {
    current_index += 1;
    updateModal(possibles[current_index]);
    manageButtons(current_index);
  });


  $("#new-match-accept").submit(function(event) {
    deferred.success(function (response) {
      // $('#newMatchModal').modal('hide');
    });

    deferred.error(function (response) {});
  })

  $("#new-thread-form").submit(function(event) {
    event.preventDefault();
    requestdict = {
      message: event.target.elements[0].value,
      otherid: event.target.getAttribute("otherid")
    }

    disable_btn("new-match-accept");

    deferred = $.post("new_thread/", requestdict)

    deferred.success(function (response) {
      location.reload();
    });

    deferred.error(function (response) {
    });

  });

  // get id of first thread
  // TODO: Throws error if there are no messages
  if ($('.thread-messages').first().length != 0){
    var firstThreadId = $('.thread-messages').first().attr("id").split("-")[1];
  }

  // open first thread
  populateThread(firstThreadId);

  // send message button functionality
  $("#send-message-form").on('submit', function(event) {
    event.preventDefault(); // prevent page refresh
    sendMessage();
    var message = $('#message-input-box').val();
    var prev_messages = $('#message-content').html();

    $("#addPersonToThread").modal('hide');

    return false;
  });  

  // add user
  $("#add-person-to-thread-form").on('submit', function(event) {
	  event.preventDefault();
	  addToThread();

	  return false;
  });

  // report person members population
  $("#reportAPersonModal").on('show.bs.modal', function() {
	  getDropdownMembersOfThread("#members-to-report");
  });

  // nudge person members population
  $("#nudgeAPersonModal").on('show.bs.modal', function() {
	  getDropdownMembersOfThread("#members-to-nudge");
  });

  $("#aboutYourMatchModal").on('show.bs.modal', function() {
    // get id of the thread that is activated
    var selectedThreadId = $(".active-link").attr("id");
    
    // ensure that there is a thread activated
    if (typeof selectedThreadId == "undefined") {
      alert("Please select a thread to send your message in!");
    }
    else {
      selectedThreadId = selectedThreadId.split("-")[2];
    }

    $.ajax({
      url : "/about_match/", // the endpoint
        type : "GET", // http method
        data : { thread_id : selectedThreadId }, // data sent with the post request
    
        // handle a successful response
        success : function(json) {
          if(json.about){
            $("#about-your-match-modal-body")[0].innerHTML = json.about
            $('#aboutYourMatchModal').modal('show');
          }
        },
    
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
        }
  });
    getDropdownMembersOfThread("#members-to-nudge");
  });

  // scroll down!
  scrollDown();

  // long polling to query for new messages in current thread
  longPollForThread(firstThreadId);

  // turn on auto-resizing text box for outgoing messages
  //  init_textarea();
  init();

  // autocomplete for adding more ppl to threads
  var substringMatcher = function(strs) {
    return function findMatches(q, cb) {      
  	  var matches, substrRegex;
  	  
  	  // an array that will be populated with substring matches
  	  matches = [];
  	  
  	  // regex used to determine if a string contains the substring `q`
  	  substrRegex = new RegExp(q, 'i');
  	  // iterate through the pool of strings and for any string that
  	  // contains the substring `q`, add it to the `matches` array
  	  $.each(strs, function(i, str) {
  		  if (substrRegex.test(nameFunc(str))) {
  		      // the typeahead jQuery plugin expects suggestions to a
  		      // JavaScript object, refer to typeahead docs for more info
  		      matches.push(valueFunc(str));
  		}});

      cb(matches);
    };
  };
  
  var emails = getMatchedUserEmails();
  var names = getMatchedUserNames();

  $('#add-person-to-thread-input').typeahead({
	  hint: true,
	      highlight: true,
	      minLength: 1
	      },
      { name: 'emails',
        displayKey: 'value',
        source: substringMatcher(emails)
    });
  
  $('#switch-to-chat-input').typeahead({
    hint: true,
        highlight: true,
        minLength: 1
        },
    { name: 'names',
      displayKey: 'value',
      source: substringMatcher(names),
      templates: {
        suggestion: function(data){
          return '<div class="new-chat" value="' + data.value.id + '"> ' + data.value.name + '</div>';
      }},         
      }).on('typeahead:selected', function(event, element) {
        populateThread(element.value.id)
    });

  if(!is_college_user() && names.length == 0) {
    $("#btn-match-me")[0].click()
  }

  $("#reset-counter").click(function(event) {
    $.ajax({
        url : "reset_counter/",
        type : "POST",
        data : {},

        success : function(json) {

        },

        error : function(xhr, errmsg, err) {

        }
      });   
  })

  $(".btn-reset-counter").click(function(event) {
    $("#waitingForMatchModal").modal('show'); 
  });

  $('#waitingForMatchModal').on('hidden.bs.modal', function () {
    location.reload();
  })
});

function _poll(threadId) {
    $.ajax({
	    url : "check_for_new_messages/",
		type : "POST",
		data : { thread_id : threadId },

		success : function(json) {
		var messages_html = "";
		// for each message
		$.each(json, function(index, val) {
			text = val[0];
			sender_email = val[1];

			messages_html += '<div class="row" style="margin-top: 10px">';
			if (sender_email == getLoggedInUserEmail()) 
			    messages_html += '<p class="chat-message sent pull-right">';
			else
			    messages_html += '<p class="chat-message received">';			    
			messages_html += text + '</p></div>';
		    });

		$("#thread-" + threadId).html(messages_html);
		console.log("checked...");
	    },

		error : function(xhr, errmsg, err) {
		$('#message-content').html("<div class= 'alert-box alert radius' data-alert>Oops! We have encountered an error!  Try refreshing the page. "+errmsg+
					   " </div>");
		console.log(xhr.status + ": " + xhr.responseText);
	    }
	});    
}

function longPollForThread(threadId) {
    if (typeof SET_INTERVAL != 'undefined')
	clearInterval(SET_INTERVAL);

    SET_INTERVAL = setInterval(_poll, 500, threadId);
    scrollDown();
}

function scrollDown() {
    // scroll to bottom of chat screen
    var chat_box = $('#message-box');
    var height = chat_box[0].scrollHeight;
    chat_box.scrollTop(height);
    //    chat_box.scrollIntoViewIfNeeded();
}

function populateThread(threadId) {
    // hide all threads
    $('.thread').each(function() {
	    $(this).hide();
	});
    
    // show individual thread
    id = "#thread-" + threadId;
    $(id).show();
    id = id + "-members";
    $(id).show();
    id = "#members-in-thread-" + threadId;
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

    // begin long polling for the newly selected thread
    longPollForThread(threadId);
}

function sendMessage() {
    // get id of the thread that is activated
    var selectedThreadId = $(".active-link").attr("id");
    
    // ensure that there is a thread activated
    if (typeof selectedThreadId == "undefined") {
	alert("Please select a thread to send your message in!");
    }
    else {
	selectedThreadId = selectedThreadId.split("-")[2];
    }
    
    // get text of message to be sent
    var message_text = $("#message-input-box").val();

    // get timestamp to apply to message to be sent
    var date = new Date();
    var timestamp = date.getTime();

    console.log("MESSAGE BEING SENT AT:" + timestamp);
    
    // clear text of input
    $("#message-input-box").val('');

    $.ajax({
	    url : "send_chat_message/", // the endpoint
		type : "POST", // http method
		data : { message_text : message_text,
		    timestamp : timestamp,
		    thread_id : selectedThreadId }, // data sent with the post request
		
	      // handle a successful response
	      success : function(json) {
		if (typeof json.ignore != "undefined") return;
		_sentMessageToDjango(json, selectedThreadId);
		// scroll down!
		scrollDown();
	    },
		
	      // handle a non-successful response
	      error : function(xhr,errmsg,err) {
		$('#message-content').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
					   " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	    }
	});
}

function _sentMessageToDjango(json, selectedThreadId) {
    // restart longpoll
    longPollForThread(selectedThreadId);

    $('#message-content').html();
    console.log(json); // log the returned json to the console
    console.log("huzzah"); // another sanity check
    
    scrollDown();
}

function _addedToThread(addedUserName) {
    // close addPersonToThread modal
    $('#addPersonToThread').modal('hide');
    
    // update thread to reflect new member yeehaw!
    //prev = $("#list-of-members").html();
    //    append = ", " + addedUserName;
    //    $("#list-of-members").html(prev+append);
    var selectedThreadId = $(".active-link").attr("id").split("-")[2];
    var old = $("#list-of-members-" + selectedThreadId).html();
    var append = " " + addedUserName;
    $("#list-of-members-"+selectedThreadId).html(old+append);
    populateThread(selectedThreadId);

    // add to button
    old = $("#thread-link-" + selectedThreadId).html();
    append = ", " + addedUserName;
    $("#thread-link-" + selectedThreadId).html(old+append);

    // clear out solo chat message
    $("#solo-chat").html("");
    
}

function getDropdownMembersOfThread(divName) {
    var selectedThreadId = $(".active-link").attr("id");
    if (typeof selectedThreadId == "undefiend") {
      alert("Please select a thread to report someone from!");
    }
    else {
      selectedThreadId =selectedThreadId.split("-")[2];
    }
    
    var members = $("#thread-link-" + selectedThreadId).html().split(",");

    var result;
    if (members.length == 1) { 
        result = '<input type="hidden"  name="reported-name" value="' + members[0].trim() + '">';
        result += '<input type="hidden"  name="selected-thread-id" value="' + selectedThreadId + '">'
        $(divName).html(result + members[0].trim());
        return;
    }
    
    result = '<select class="form-control" name="reported-name">';
    for (var index=0; index < members.length; index++) {
        result += '<option value="' + members[index].trim() + '">' + members[index].trim() + "</option>";
    }
    result += "</select>";
    result += '<input type="hidden"  name="selected-thread-id" value="' + selectedThreadId + '">'

    $(divName).html(result);
}

function addToThread() {
    var selectedThreadId = $(".active-link").attr("id");
    if (typeof selectedThreadId == "undefined") {
      alert("Please select a thread to send your message in!");
    }
    else {
      selectedThreadId = selectedThreadId.split("-")[2];
    }

    var userEmail = $("#add-person-to-thread-input").val();

    $.ajax({
        url : "add_user_to_thread/", // the endpoint
		    type : "POST", // http method
		    data : { user_email : userEmail,
		    thread_id : selectedThreadId }, // data sent with the post request
		
	      // handle a successful response
	      success : function(json) {
		if (typeof json.ignore != "undefined") return;
		console.log("huzzah, the zoombinies have reached castle rock!");
		_addedToThread(json.new_user_name);
		// scroll down!
		scrollDown();
	    },
		
	      // handle a non-successful response
	      error : function(xhr,errmsg,err) {
		$('#message-content').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
					   " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
		console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
	    }
	});
}

// functions for autoresizing textbox for outgoing messages
if (window.attachEvent) {
    observe = function (element, event, handler) {
        element.attachEvent('on'+event, handler);
    };
}
else {
    observe = function (element, event, handler) {
        element.addEventListener(event, handler, false);
    };
}
function init () {
    var text = document.getElementById('message-input-box');
    var send_button = document.getElementById('btn-send-message');

    function resize () {
        text.style.height = 'auto';
        text.style.height = text.scrollHeight+'px';
	send_button.style.height = text.style.height;
    }
    /* 0-timeout to get the already changed text */
    function delayedResize () {
        window.setTimeout(resize, 0);
    }
    observe(text, 'change',  resize);
    observe(text, 'cut',     delayedResize);
    observe(text, 'paste',   delayedResize);
    observe(text, 'drop',    delayedResize);
    observe(text, 'keydown', delayedResize);

    text.focus();
    text.select();
    resize();
}


/**
 * This tiny script just helps us demonstrate
 * what the various example callbacks are doing
 * from: http://bootboxjs.com/
 */
var Example = (function() {
    "use strict";

    var elem,
        hideHandler,
        that = {};

    that.init = function(options) {
        elem = $(options.selector);
    };

    that.show = function(text) {
        clearTimeout(hideHandler);

        elem.find("span").html(text);
        elem.delay(200).fadeIn().delay(4000).fadeOut();
    };

    return that;
}());

disable_btn = function(id) {
  $("#" + id)[0].disabled = true
}

// Example.show("something plz happen");








