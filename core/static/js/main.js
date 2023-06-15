$(document).ready(function(){
	$('#select-moradia').change(function(){
		if($(this).val() == 'Outros'){
			$('#div-outros').show();
		}else{
			$('#div-outros').hide();
		}
	});
});

