$(document).ready(function () {
  $("form").submit(function (event) {
    event.preventDefault();

    var userInput = $("#user-input").val();
    displayUserMessage(userInput);
    sendQuestion(userInput);
  });
});

function displayUserMessage(message) {
  var messageContainer = $('<div class="message-container"></div>');
  var userMessage = $('<div class="user-message"></div>').text(message);
  messageContainer.append(userMessage);
  $("#chat-container").append(messageContainer);
  $("#user-input").val("");
  scrollToBottom();
}

function displayBotMessage(message) {
  var messageContainer = $('<div class="message-container"></div>');
  var botMessage = $('<div class="bot-message"></div>').text(message);
  messageContainer.append(botMessage);
  $("#chat-container").append(messageContainer);
  scrollToBottom();
}

function sendQuestion(question) {
  var loadingSpinner = $('<div class="loading-spinner"></div>');
  $("#chat-container").append(loadingSpinner);
  scrollToBottom();

  $.ajax({
    type: "POST",
    url: "/answer",
    data: { question: question },
    success: function (response) {
      var botResponse = response.answer;
      $(".loading-spinner").remove();
      displayBotMessage(botResponse);
    },
    error: function () {
      $(".loading-spinner").remove();
      displayBotMessage("An error occurred. Please try again.");
    },
  });
}

function scrollToBottom() {
  $("#chat-container").scrollTop($("#chat-container")[0].scrollHeight);
}
