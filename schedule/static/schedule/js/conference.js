$('#id_server').change(function () {
      var typeSelected = this.options[this.selectedIndex].getAttribute("data-server-type");
      if (typeSelected === "local") {
            $('#div_id_quota').show();
            $('#div_id_link').hide();
            $('#div_id_file').hide();
            $('#div_id_description').hide();
      } else if (typeSelected === "external") {
            $('#div_id_quota').hide();
            $('#div_id_link').show();
            $('#div_id_file').show();
            $('#div_id_description').show();
      } else {
            $('#div_id_quota').hide();
            $('#div_id_link').hide();
            $('#div_id_file').hide();
            $('#div_id_description').hide();
      }
    });
$(document).ready(function () {
      var optionSelected = $("#id_server option:selected");
      var typeSelected = optionSelected.data("server-type");
      if (typeSelected === "local") {
            $('#div_id_quota').show();
            $('#div_id_link').hide();
            $('#div_id_file').hide();
            $('#div_id_description').hide();
      } else if (typeSelected === "external") {
            $('#div_id_quota').hide();
            $('#div_id_link').show();
            $('#div_id_file').show();
            $('#div_id_description').show();
      } else {
            $('#div_id_quota').hide();
            $('#div_id_link').hide();
            $('#div_id_file').hide();
            $('#div_id_description').hide();
      }
    });
