function applyDiscount() {
    var discount = Number($("#id_coupon_discount").html());

    if (discount > .0) {
        var amount = Number(
            $(".price_radio:checked").attr("amount"));
        
        if (amount > .0) {
            $(".discount").show();
            $("#id_price_total").html(amount - discount);
        } else {
            $(".discount").hide();
        }
    }
}

function processCoupon() {
    $.ajax(coupon_validation_url, {
        data: {coupon_code: $("#id_coupon_code").val()},
        success: function(data, textStatus, jqXHR) {
            if (data.status == "ok") {
                $("#id_coupon_code_control input").after(
                    "<p>Valid coupon</p>");
                $("#id_coupon_code").hide();
                $("#id_coupon_code_button").html(
                    "<span class=\"glyphicon glyphicon-ok\"></span>");
                $("#id_coupon_discount").html(data.discount);
                $(".discount").show();
                applyDiscount();
            } else {
                $("#id_coupon_code_form_group").addClass("has-error");
                $("#id_coupon_code").attr(
                    "title",
                    "This coupon has already been claimed or is invalid.");
            }
        },
        error: ajax_error_handler
    });
}

function processTotal(price_radio) {
    var amount = price_radio.attr("amount");

    if (amount != undefined) {
        if (amount > .0) {
            $("#id_purchase_info").show();
            $("#id_price_title").html(price_radio.attr("title"));
            $("#id_price_tag").html(amount);
            $("#id_price_total").html(amount);
            if ($("#id_coupon_code").val()) processCoupon();
        } else {
            $("#id_purchase_info").hide();
        }
        $("#id_summary").show();
    }
}

$(document).ready(function() {
    var price_radio = $(".price_radio:checked");

    if (price_radio) processTotal(price_radio);
});

$(document).ready(function() {
    $(".price_radio").click(function() {
        processTotal($(this))
    });
});

$(document).ready(function() {
    $("#id_coupon_code_button>button").mouseup(processCoupon);
});

function stripeResponseHandler(status, response) {
    if (response.error) {
        $("#id_stripe_error li").html(response.error.message);
        $("#id_stripe_error").show();
        $("#id_submit").prop("disabled", false);
    } else {
        var token = response['id'];

        $("#id_stripe_token").val(token);
        $("#id_main_form").submit();
    }
}

$(document).ready(function() {
    $("#id_submit").click(function() {
        var stripe_form = $("#id_stripe_form");

        $("#id_submit").prop("disabled", true);
        Stripe.card.createToken(stripe_form, stripeResponseHandler);
        event.preventDefault();
    });
});
