$(document).ready(function() {
	// There is no parallel for "oninput" in jQuery, so JS is used here 



	$('#SignUp').click(function(){
   		window.location.href='http://localhost:5000/signup';
	})

	/*
	let signupbutton = document.getElementById("SignIn");
	signupbutton.click(function(){

		$.ajax({
			url: "http://localhost/signup",
			//data: { "value" : $("#search-string").val() }
		})
		.done(function(data) {
			//if no errors redirect to 
			$("#possible-query").text(data);
		});

	});
	*/
});