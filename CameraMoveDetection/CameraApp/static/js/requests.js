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
                console.log(response)
                $("#mdlda").html(`<img src=\'${response[0]['Image']}\'>`);
                //�������� �������� response[""]
                modal.classList.add('modal_vis'); // ��������� ��������� ����
                modal.classList.remove('bounceOutDown'); // ������� ������ ��������
                body.classList.add('body_block');
            },
            error: function (error) {
                console.log(error);
            }
        });
}

function SliderBindRunAll() {
    var span = $('#sldr');
    span.click(() => {
        if ($('#sldr').prop('checked')) {
            /*span.prop('checked', true);*/
            $.ajax({
                type: "POST",
                url: "/ThreadsRunAll",
                data: {},
                type: 'POST',
                success: function (response) {
                    console.log(response)
                },
                error: function (error) {
                    console.log(error);
                }
            });
        } else {
            $.ajax({
                type: "POST",
                url: "/ThreadsStopAll",
                data: {},
                type: 'POST',
                success: function (response) {
                    console.log(response)       
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
    console.log("awdadw");
    $.ajax({
        type: "POST",
        url: "/GetImages",
        data: {},
        type: 'POST',
        success: function (response) {
            console.log(response);
            console.log("updateDisplays")
            for (r in response) {
                console.log(r)
            }
            //for ((key, value) in response) {
            //    document.getElementById(`Cam${key}`).src = "data:image/png;base64," + value;
            //    //Do stuff where key would be 0 and value would be the object
            //}
            
        },
        error: function (error) {
            console.log(error);
        }
    });
}

var alarmList = [];
function getAlarmList() {
    updateDisplays();
    $.ajax({
        type: "POST",
        url: "/Signals",
        data: $('').serialize(),
        type: 'POST',
        success: function (response) {
            console.log(response);
            console.log(alarmList);
            alarmList = Object.keys(response).map((key) => response[key]);
            //document.getElementById("alarmList").innerHTML = `<tr><th>WatchImg</th><th>CamId</th><th>SensTime</th><th>IsMove</th><th>IsMoving</th></tr >`;
            for (let alarm of alarmList) {
                console.log(alarm.TimeStamp);
                dt = new Date(alarm.TimeStamp)
                //onclick = SignalsSpec(${ alarm.CameraId }, '${alarm.TimeStamp}')
                document.getElementById("alarmList").insertRow(-1).innerHTML = ` <button value="Image" onclick="SignalsSpec(${alarm.CameraId}, '${alarm.TimeStamp}')">Показать</button></td><tr onclick=SignalsSpec(3,"23-12-2021 23:00:00")><td>${alarm.CameraId}</td><td>${alarm.TimeStamp}</td><td>${alarm.IsMoved}</td><td>${alarm.IsMoving}</td></td></tr>`;
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

