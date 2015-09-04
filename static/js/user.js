var is_agree=false;
function checkPasswordMatch() {
    var password = $("#signup-password").val();
    var confirmPassword = $("#password-confirm").val();

    if (password != confirmPassword ){
        //alert('notmatch');
         $('#signup-button').attr('disabled', 'disabled');
         document.getElementById("password-confirm").setAttribute("style", "background-color: rgba(250, 20, 0, 0.5);");
         document.getElementById("signup-password").setAttribute("style", "background-color: rgba(250, 20, 0, 0.5);");

    	//$("#signup-password").setAttribute("class", "password-confirm-error");
    }else {
         document.getElementById("password-confirm").setAttribute("style", "background-color: rgb(181, 231, 246);");
         document.getElementById("signup-password").setAttribute("style", "background-color: rgb(181, 231, 246);");

    }
    if (password == '' && confirmPassword==''){
         document.getElementById("password-confirm").setAttribute("style", "background-color: rgb(181, 231, 246);");
         document.getElementById("signup-password").setAttribute("style", "background-color: rgb(181, 231, 246);");


    }
}

$(document).ready(function () {

   $("#password-confirm").keyup(checkPasswordMatch);
});

(function() {
    $('form >  input').keyup(function() {

        var empty = false;
        $('form >  input').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });
        /*$('form > div > div > TextArea').each(function() {
            if ($(this).val() == '') {
                empty = true;
            }
        });
*/


	var password = $("#signup-password").val();
    var confirmPassword = $("#password-confirm").val();

 		if (password == '' || confirmPassword==''){

         $('#signup-button').attr('disabled', 'disabled');
    	}

	if (empty || is_agree==false) {
            $('#signup-button').attr('disabled', 'disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        } else {
            $('#signup-button').removeAttr('disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        }

        checkPasswordMatch();
    });
})()

$('#signup-username').blur(function() {
    $.get('/check_username_db',{username:$('#signup-username').val() },function(data){

        if (data.exist == "exist"){
        	$('#error').html('<p class="alert alert-danger">Username is Already taken</p>');
        }else if(data.exist == "available"){
        	$('#error').html('<p class="alert alert-success">Username is Available</p>');
        }else if(data.exist == "s_character"){
            $('#error').html('<p class="alert alert-warning">Your username should not contain special characters, space or Capital Letter</p>');
        }
    });

});

$('#email-address').blur(function() {
    $.get('/check_email_db',{email:$('#email-address').val() },function(data){

        if (data.exist=="exists"){
        	$('#error_email').html('<p class="alert alert-danger">Email is Already taken</p>');
        }else if (data.exist=="not"){
        	$('#error_email').html('<p class="alert alert-success">Email is Available</p>');
        }

    });

});

function validate() {
    if (document.getElementById('agree').checked) {
         $('#signup-button').removeAttr('disabled');
        is_agree=true;
    } else {
        $('#signup-button').attr('disabled', 'disabled');
        is_agree=false;

    }
}
if(is_agree){

}else{
    $('#signup-button').attr('disabled', 'disabled');
}
function disable_field(field){
  $('#'+field+'').removeAttr('disabled');
   $('#'+field+'1').removeAttr('hidden');
}