$(document).ready(function(){
	
	$(".notimplemented").click(function() {
		$.fancybox(
			'<div style=\"background:#444;width:500px;height:200px;font-size:28px;padding:28px;font-weight:bold;\"><h1 style=\"color:#F20056\">This function is not yet implemented.</h1><br/><p style=\"color: white;font-size:20px;\">Help us implement it?<br/><a style=\"color:white\" href=\"https://blueprints.launchpad.net/globaleaks\">Take a look at the blueprints</a></p></div>',
			{

			});
	
		return false;
	});
	
    /* $(".disabled").click(function() {
		$.fancybox(
			'<div style=\"background:#444;width:500px;height:200px;font-size:28px;padding:28px;font-weight:bold;\"><h1 style=\"color:#F20056\">This function is DISABLED in demo...</h1>',
			{

			});
	
		return false;
	});
	*/
	$("#content .box").hover(
	  function () {
	    $(this).addClass("box-hover");
	  }, 
	  function () {
	    $(this).removeClass("box-hover");
	  }
	);
	
});

Cufon.replace("h1,h2,h3");
