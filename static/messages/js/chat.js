$(document).ready(function(){

  // disable scroll on this page
	//  $('#chat-room').on({
	//      'mousewheel': function(e) {
	//          if (e.target.id == 'el') return;
	//          e.preventDefault();
	//          e.stopPropagation();
	//      }
	//  });

  // send message
  $('#send-message-form').submit(function () {
    var message = $('#message-input-box').val();
    var prev_messages = $('#message-content').html();

    if (message) {
      $('#message-content').html(prev_messages + '<div class="row" style="margin-bottom: 10px;"><div class="btn btn-primary pull-right disabled">' + message + '</div></div>');
    }

    return false;
  });

  // hit submit button on 'enter' keypress
  $('#message-input-box').keypress(function (e) {
    if (e.which == 13) {
      $('#btn-send-message').click();
      $('#message-input-box').val("");
    }
  });
});
