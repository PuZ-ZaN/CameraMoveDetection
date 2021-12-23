function addinput() {
    $.ajax({
        type: "POST",
        url: "/CameraAdd",
        data: $('#frm').serialize(),
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



function SignalsSpec(id, ts) {
    console.log("SignalsSpec");
    $.ajax({
        type: "POST",
        url: "/SignalsSpec",
        data: { "CameraId": id, "TimeStamp": ts },
        type: 'POST',
        success: function (response) {
            console.log("CHAVKA")
            console.log(response[0]['Image'])
            $("#mdlda").html(`<img src='${response[0]['Image']}'>`);
            modal.classList.add('modal_vis');
            modal.classList.remove('bounceOutDown');
            body.classList.add('body_block');
        },
        error: function (error) {
            console.log(error);
        }
    });
}
var isNeedupdate = true;
var interval = NaN;
function SliderBindRunAll() {
    var span = $('#sldr');
    span.click(() => {
        if ($('#sldr').prop('checked')) {
            /*span.prop('checked', true);*/
            isNeedupdate = true;
            interval = setInterval(() => {
                 if (isNeedupdate == false)
                    clearInterval(interval);
                updateDisplays();
                console.log("WKRAWF");
            }, 3000);
            $.ajax({
                type: "POST",
                url: "/ThreadsRunAll",
                data: {},
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        } else {
            isNeedupdate = false;
            $.ajax({
                type: "POST",
                url: "/ThreadsStopAll",
                data: {},
                type: 'POST',
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.log(error);
                }
            });
        }
        console.log(span.prop('checked'));
        span.innerText += "1";
    });
}
 
SliderBindRunAll();

function updateDisplays() {
    console.log("Start func updateDisplays");
    $.ajax({
        type: "POST",
        url: "/GetImages",
        data: {},
        type: 'POST',
        success: function (response) {
            console.log("XA4A")
            console.log(response);
            var selected = document.getElementByClassName("input-info");
            console.log(selected)
            selected = select.split("]");
            for (var key in response) {
                document.getElementById(`Cam${key}`).src = "data:image/jpeg;base64,"+response[key]["Frame"];
                //Do stuff where key would be 0 and value would be the object
                if (key == selected)
                    document.getElementByClassName("video-input").src = response[key]["Frame"] ;
                console.log('Key =', key);
                console.log('Test=', response[key]);
            }

        },
        error: function (error) {
            console.log(error);
        }
    });
}

var alarmList = [];
function getAlarmList() {
    console.log("Start func getAlarmList");
    //updateDisplays();
    $.ajax({
        type: "POST",
        url: "/Signals",
        data: $('').serialize(),
        type: 'POST',
        success: function (response) {
            console.log(response);
            console.log(alarmList);
            alarmList = Object.keys(response).map((key) => response[key]);
            document.getElementById("alarmList").innerHTML = `<tr><th>Кадр</th><th>Номер камеры</th><th>Время срабатывания</th><th>IsMove</th><th>IsMoving</th></tr >`;
            for (let alarm of alarmList) {
                console.log(alarm.TimeStamp);
                dt = new Date(alarm.TimeStamp);
                //onclick = SignalsSpec(${ alarm.CameraId }, '${alarm.TimeStamp}')
                document.getElementById("alarmList").insertRow(-1).innerHTML = ` <button onclick="SignalsSpec(${alarm.CameraId}, '${alarm.TimeStamp}')">X</button></td><tr onclick=SignalsSpec(3,"23-12-2021 23:00:00")><td>${alarm.CameraId}</td><td>${alarm.TimeStamp}</td><td>${alarm.IsMoved}</td><td>${alarm.IsMoving}</td></td></tr>`;
                //console.log("ANN")
                //console.log($('#alarmList > tbody > tr:last-child'));
                //$('#alarmList > tbody > tr:last-child').onclick = console.log("awda");//SignalsSpec(alarm.CameraId, alarm.TimeStamp);
                //$('#alarmList > tbody > tr:last-child').css('background-color', '#ff0000');
                //document.getElementById("alarmList").rows[table.rows.length - 1].onclick = SignalsSpec(alarm.CameraId, alarm.TimeStamp);
                //var table = document.getElementById("alarmList")
                //console.log(table.rows[table.rows.length - 1].innerHTML)
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

