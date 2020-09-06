function sendData() {
    let email = $("#emailInput").val()
    let password = $("#passwordInput").val()
    let recipient = $("#recipientInput").val()
    let content = $("#contentInput").val()
    let time = $("#timeInput").val()
    let group = $("#groupCheck").is(':checked')

    let success = $("#success")
    let error = $("#warning")
    let failure = $("#failure")

    let attachments = {}
    attachments["email"] = email
    attachments["password"] = password
    attachments["recipient"] = recipient
    attachments["content"] = content
    attachments["action_time"] = time
    attachments["group"] = group

    $.ajax({
        type: "POST",
        url: "/message/",
        data: JSON.stringify(attachments),
        contentType: "application/json; charset=utf-8",
        traditional: true,
        success: function(data){
            if (data == "Success") {
                success.show()
            } else if (data == "Missing credentials") {
                error.show().html(data)
            } else if (data == "Missing content") {
                error.show().html(data)
            } else if (data == "Recipient not found") {
                error.show().html(data)
            } else if (data == "Wrong credentials") {
                failure.show().html(data)
            }
        },
        error: function(e) {
            console.log(e)
            failure.show()
        }
    })
}

$(document).ready(function() {
    $("#sendMessageSubmit").click(function(){
        sendData()
    })
});