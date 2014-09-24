$(document).ready(function() {
    make_active($("#id_employer_profile_praxis_profile_menu"));
});

$(document).ready(function() {
    $("#id_schedule_days_control_group").show();
    $("#id_schedule_type_0").click(function (){
        $("#id_schedule_days_control_group").show();
    });
    $("#id_schedule_type_1").click(function (){
        $("#id_schedule_days_control_group").hide();
    });
});

$(document).ready(function() {
    $("#id_hourly_wage_control_group").show();
    $("#id_annualy_wage_control_group").hide();
    $("#id_compensation_type_0").click(function (){
        $("#id_hourly_wage_control_group").show();
        $("#id_annualy_wage_control_group").hide();
    });
    $("#id_compensation_type_1").click(function (){
        $("#id_hourly_wage_control_group").hide();
        $("#id_annualy_wage_control_group").show();
    });
});

$(document).ready(function() {
    var toggle_other = true;
    var benefit_other_text = $("#id_benefit_other_text");

    benefit_other_text.hide();
    $("#id_benefit_other").click(function() {
        if (toggle_other) {
            benefit_other_text.show();
        } else {
            benefit_other_text.hide();
        }
        toggle_other = !toggle_other;
    });
});
