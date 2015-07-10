function checkPasswordMatch() {
    var password = $("#signup-password").val();
    var confirmPassword = $("#password-confirm").val();

    if (password != confirmPassword ){
        //alert('notmatch');
         $('#signup-button').attr('disabled', 'disabled');
         document.getElementById("password-confirm").setAttribute("style", "background-color: red;");
         document.getElementById("signup-password").setAttribute("style", "background-color: red;");
    	//$("#signup-password").setAttribute("class", "password-confirm-error");
    }else {
         document.getElementById("password-confirm").setAttribute("style", "background-color: rgba(250, 250, 250, 0.5);");
         document.getElementById("signup-password").setAttribute("style", "background-color: rgba(250, 250, 250, 0.5);");
    	 
    }
    if (password == '' && confirmPassword==''){
         document.getElementById("password-confirm").setAttribute("style", "background-color: rgba(250, 250, 250, 0.5);");
         document.getElementById("signup-password").setAttribute("style", "background-color: rgba(250, 250, 250, 0.5);");
    	 
    }
}

$(document).ready(function () {
	
   $("#password-confirm").keyup(checkPasswordMatch);
});

(function() {
    $('form >  input').keyup(function() {

        var empty = false;
        $('form >  input').each(function() {
            if ($(this).val() == '' || $('#description').val() == '') {
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

	if (empty) {
            $('#signup-button').attr('disabled', 'disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        } else {
            $('#signup-button').removeAttr('disabled'); // updated according to http://stackoverflow.com/questions/7637790/how-to-remove-disabled-attribute-with-jquery-ie
        }

        checkPasswordMatch();
    });
})()

$('#signup-username').blur(function() {
    $.get('/check_username_db',{username:$('#signup-username').val() },function(data){
        
        if (data.exist){
        	$('#error').html('<p class="alert alert-danger">Username is Already taken</p>');
        }else{
        	$('#error').html('<p class="alert alert-success">Username is Available</p>');
        }
    });

});

$('#email-address').blur(function() {
    $.get('/check_email_db',{email:$('#email-address').val() },function(data){
        
        if (data.exist){
        	$('#error_email').html('<p class="alert alert-danger">Email is Already taken</p>');
        }else{
        	$('#error_email').html('<p class="alert alert-success">Email is Available</p>');
        }
    });

});


function disable_field(field){
  $('#'+field+'').removeAttr('disabled');
   $('#'+field+'1').removeAttr('hidden');
}