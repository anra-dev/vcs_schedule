$('#id_server').change(function () {
      //var optionSelected = this.options[this.selectedIndex].text;
      var optionSelected = this.getAttribute("data-server-type")
      if (~optionSelected.indexOf("local")) {
            $('#div_id_quota').show();
            $('#div_id_link').hide();
      } else if (~optionSelected.indexOf("external")){
            $('#div_id_quota').hide();
            $('#div_id_link').show();
      } else {
            $('#div_id_quota').hide();
            $('#div_id_link').hide();
      }
    });
$(document).ready(function () {
      //var optionSelected = $("#id_server option:selected").text();
      var valueSelected = $("#id_server option:selected").getAttribute("data-server-type")
      if (~optionSelected.indexOf("local")) {
            $('#div_id_quota').show();
            $('#div_id_link').hide();
      } else if (~optionSelected.indexOf("external")){
            $('#div_id_quota').hide();
            $('#div_id_link').show();
      } else {
            $('#div_id_quota').hide();
            $('#div_id_link').hide();
      }
    });
