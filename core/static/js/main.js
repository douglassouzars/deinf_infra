$(document).ready(function(){
	$('#select-moradia').change(function(){
		if($(this).val() == 'Outros'){
			$('#div-outros').show();
		}else{
			$('#div-outros').hide();
		}
	});
});


    $(document).ready(function() {
        $('#pasta').change(function() {
            var selectedOption = $(this).val();
            if (selectedOption === 'DEINF') {
                $.ajax({
                    url: '/get_users_from_deinf/',
                    type: 'GET',
                    success: function(response) {
                        var users = response.users;
                        // Exiba a lista de usuários na página HTML como desejar
                        // Código para exibir a lista de usuários aqui
                    },
                    error: function(xhr, status, error) {
                        console.log(error);
                    }
                });
            }
        });
    });

