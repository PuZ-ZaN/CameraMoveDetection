function addinput() {
    $.ajax({
      type: "POST",
      url: "/addinput",
      data: $('form').serialize(),
      type: 'POST',
      success: function (response) {
        //var json = jQuery.parseJSON(response)
        //$('#len').html(json.len)
        console.log(response);
      },
      error: function (error) {
        console.log(error);
      }
    });
  }
  
  function getAlarmList() {
    $.ajax({
      type: "POST",
      url: "/getAlarmList",
      data: $('').serialize(),
      type: 'POST',
      success: function (response) {
        console.log(response);
      },
      error: function (error) {
        console.log(error);
      }
    });
  }