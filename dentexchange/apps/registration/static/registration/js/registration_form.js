$(document).ready(function() {
    if ($(".registration-form .alert-error,.registration-form .has-error")
            .length > 0) {
        $(".registration-welcome").hide();
        $(".registration-form").show();
    }

    $(".sign-up-button").click(function(e) {
        $(".registration-welcome").fadeOut(200, function() {
            $(".registration-form").fadeIn();
        });
    });
});
