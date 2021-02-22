$('#id_without_conference').on('click', function () {
    if ( $(this).is(':checked') ) {
            $('#id_time_start').prop('readonly', false)
            $('#id_time_start').css('background', 'white')
            $('#id_time_end').prop('readonly', false)
            $('#id_time_end').css('background', 'white')
            $('#id_conference').prop('readonly', true)
            $('#id_conference').prop('disabled', true)
            $('#id_conference').css('background', 'lightgray')
            $('#id_conference').val('')
    } else {
            $('#id_time_start').prop('readonly', true)
            $('#id_time_start').css('background', 'lightgray')
            $('#id_time_start').val('')
            $('#id_time_end').prop('readonly', true)
            $('#id_time_end').css('background', 'lightgray')
            $('#id_time_end').val('')
            $('#id_conference').prop('readonly', false)
            $('#id_conference').prop('disabled', false)
            $('#id_conference').css('background', 'white')

    }
});
$(document).ready( function () {
    if ( $('#id_without_conference').is(':checked') ) {
            $('#id_time_start').prop('readonly', false)
            $('#id_time_start').css('background', 'white')
            $('#id_time_end').prop('readonly', false)
            $('#id_time_end').css('background', 'white')
            $('#id_conference').prop('readonly', true)
            $('#id_conference').prop('disabled', true)
            $('#id_conference').css('background', 'lightgray')
    } else {
            $('#id_time_start').prop('readonly', true)
            $('#id_time_start').css('background', 'lightgray')
            $('#id_time_end').prop('readonly', true)
            $('#id_time_end').css('background', 'lightgray')
            $('#id_conference').prop('readonly', false)
            $('#id_conference').prop('disabled', false)
            $('#id_conference').css('background', 'white')

    }
});