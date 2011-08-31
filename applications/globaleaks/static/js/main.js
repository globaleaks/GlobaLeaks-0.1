$(document).ready(function(){
	
	$(".notimplemented").click(function() {
		$.fancybox(
			'<div style=\"background:#444;width:300px;height:60px;padding:40px;text-transform:uppercase;font-size:28px;font-weight:bold;text-align:center\"><h1 style=\"color:#fff\">This function is not implemented!</h1></div>',
			{

			});
	
		return false;
	});
	
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