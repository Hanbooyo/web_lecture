$(document).ready(function() {
    // 메시지를 추가하는 함수
    function addMessage(role, content) {
        let chatMessages = $(".chat-messages");
        let message = $("<div>").addClass("message").appendTo(chatMessages);
        let messageContent = $("<div>").addClass(`message-content ${role}`).text(content).appendTo(message);
    }

    // form 제출 이벤트 리스너
    $("#chat-form").submit(function(e) {
        e.preventDefault(); // 기본 제출 이벤트 방지
        let inputBox = $("#chat_input");
        let inputText = inputBox.val().trim();
        if (inputText.length > 0) { // 입력값이 있는 경우
            addMessage("user", inputText); // 유저 메시지를 추가
            inputBox.val(""); // 입력값 초기화

            // ChatGPT API 호출
            $.ajax({
                url: "/get-response",
                method: "POST",
                data: {chat_input: inputText},
                success: function(response) {
                    addMessage("system", response.bot_response); // 시스템 메시지를 추가
                },
                error: function(xhr, status, error) {
                    console.log(error);
                }
            });
        }
    });
});
