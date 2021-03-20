$('#id_without_conference').on('click', function () {
    if ( $(this).is(':checked') ) {
            $('#div_id_date').show();
            $('#div_id_time_start').show();
            $('#div_id_time_end').show();
            $('#div_id_conference').hide();
    } else {
            $('#div_id_date').hide();
            $('#div_id_time_start').hide();
            $('#div_id_time_end').hide();
            $('#div_id_conference').show();
    }
});
$(document).ready( function () {
    if ( $('#id_without_conference').is(':checked') ) {
            $('#div_id_date').show();
            $('#div_id_time_start').show();
            $('#div_id_time_end').show();
            $('#div_id_conference').hide();
    } else {
            $('#div_id_date').hide();
            $('#div_id_time_start').hide();
            $('#div_id_time_end').hide();
            $('#div_id_conference').show();

    }
});