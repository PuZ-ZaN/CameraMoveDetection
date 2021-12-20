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


var alarmList = [];
function getAlarmList() {
  $.ajax({
    type: "POST",
    url: "/getAlarmList",
    data: $('').serialize(),
    type: 'POST',
    success: function (response) {
      console.log(response);

      alarmList = Object.keys(response).map((key) => response[key]);
      for (let alarm of alarmList) {
        //console.log(alarm);
        document.getElementById("alarmList").insertRow(-1).innerHTML = `<td>${alarm.name}</td><td>${alarm.timestamp}</td>`;
      }
    },
    error: function (error) {
      console.log(error);
    }
  });
}

function deleteInput() {
  $.ajax({
    type: "POST",
    url: "/delete",
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

function getImage() {
  $.ajax({
    type: "POST",
    url: "/getImage",
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

