$('#id_server').change(function () {
      var optionSelected = $("option:selected", this);
      var valueSelected = $(this).val();
        console.log(valueSelected);
      if (valueSelected !== '1') {
            $('#id_quota').prop('readonly', false)
            $('#id_quota').val('')
            $('#id_quota').css('background', 'white')
            $('#id_link').prop('readonly', true)
            $('#id_link').val('')
            $('#id_link').css('background', 'lightgray')
      } else {
            $('#id_quota').prop('readonly', true)
            $('#id_quota').val('')
            $('#id_quota').css('background', 'lightgray')
            $('#id_link').prop('readonly', false)
            $('#id_link').val('')
            $('#id_link').css('background', 'white')
      }
    });
$(document).ready(function () {
      var valueSelected = $('#id_server').val();

      if (valueSelected !== '1') {
            $('#id_quota').prop('readonly', false)
            $('#id_quota').css('background', 'white')
            $('#id_link').prop('readonly', true)
            $('#id_link').css('background', 'lightgray')
      } else {
            $('#id_quota').prop('readonly', true)
            $('#id_quota').css('background', 'lightgray')
            $('#id_link').prop('readonly', false)
            $('#id_link').css('background', 'white')
      }
    });
