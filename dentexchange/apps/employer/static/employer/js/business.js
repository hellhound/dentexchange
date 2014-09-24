$(document).ready(function() {
    $("#id_number_offices").change(function() {
        if (Number($(this).val()) > 1) {
            $("#id_mso").show();
        } else {
            $("#id_mso").hide();
        }
    });
});
