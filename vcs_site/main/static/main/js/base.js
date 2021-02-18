$('#id_type').change(function () {
 console.log( "Запуск скрипта" );
      var optionSelected = $("option:selected", this);
      var valueSelected = $(this).val();

      if (valueSelected === 'local') {
            $('#id_quota').prop('readonly', false)
            $('#id_quota').val('')
            $('#id_quota').css('background', 'white')
            $('#id_link_to_event').prop('readonly', true)
            $('#id_link_to_event').val('')
            $('#id_link_to_event').css('background', 'lightgray')
      } else if (valueSelected === 'external') {
            $('#id_quota').prop('readonly', true)
            $('#id_quota').val('')
            $('#id_quota').css('background', 'lightgray')
            $('#id_link_to_event').prop('readonly', false)
            $('#id_link_to_event').val('')
            $('#id_link_to_event').css('background', 'white')
      } else {
        $('#id_rooms').parent().show();
        $('#id_series').parent().show();
      }
    });
$(document).ready(function () {
 console.log( "Запуск скрипта" );
      var valueSelected = $('#id_type').val();

      if (valueSelected === 'local') {
            $('#id_quota').prop('readonly', false)
            $('#id_quota').css('background', 'white')
            $('#id_link_to_event').prop('readonly', true)
            $('#id_link_to_event').css('background', 'lightgray')
      } else if (valueSelected === 'external') {
            $('#id_quota').prop('readonly', true)
            $('#id_quota').css('background', 'lightgray')
            $('#id_link_to_event').prop('readonly', false)
            $('#id_link_to_event').css('background', 'white')
      } else {
        $('#id_rooms').parent().show();
        $('#id_series').parent().show();
      }
    });
