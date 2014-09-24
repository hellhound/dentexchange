function select_schedule_type_part_time() {
    $("#id_schedule_days_control_group").show();
}

function select_schedule_type_full_time() {
    $("#id_schedule_days_control_group").hide();
}

function select_schedule_type() {
    if ($("#id_schedule_type_0:checked").get(0)) {
        select_schedule_type_part_time();
    } else {
        select_schedule_type_full_time();
    }
}

function select_compensation_type_hourly() {
    $("#id_hourly_wage_control_group").show();
    $("#id_annualy_wage_control_group").hide();
}

function select_compensation_type_salary() {
    $("#id_hourly_wage_control_group").hide();
    $("#id_annualy_wage_control_group").show();
}

function select_compensation_type() {
    if ($("#id_compensation_type_0:checked").get(0)) {
        select_compensation_type_hourly();
    } else {
        select_compensation_type_salary();
    }
}

$(document).ready(function (){
    select_schedule_type();
    select_compensation_type();
    $("#id_schedule_type_0,#id_schedule_type_1").click(function (){
        select_schedule_type();
    });
    $("#id_compensation_type_0,#id_compensation_type_1").click(function (){
        select_compensation_type();
    });
});
