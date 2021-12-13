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

let cards = document.querySelectorAll('.card')
let videoName = document.querySelector('.input-info')
let videoInput = document.getElementById('video-input')


// Input name func
for (let card of cards) {
  card.onclick = function () {
    console.log('click on card!')
    //input name
    videoName.textContent = card.textContent;
  }
}

// Input video src func
var videoTags = document.getElementsByTagName('video')
for (let tag of videoTags) {
  tag.onclick = function () {
    videoInput.src = tag.src;
    videoInput.load();
    videoInput.play();
  }
}


//Modals
let buttons = document.getElementsByClassName('modal-btn')
let modals = document.querySelectorAll('.modal')
let span = document.getElementsByClassName('close-modal')[0];



for (let modal of modals) {
  if (span.id == modal.id) {
    modal.style.display = "none"
    console.log('Close Modal!')
  }
}

for (let button of buttons) {
  button.onclick = function () {
    for (let modal of modals) {
      //open modal
      if (button.id === modal.id) {
        modal.style.display = "block";

        //close when click outside
        window.onclick = function (event) {
          if (event.target == modal) {
            modal.style.display = "none";
          }
        }
        //close when click on X
        span.onclick = function () {
          modal.style.display = "none";
        }
      }
    }
  }
}

//Add Input
let inputName = document.getElementById('name')
let inputSource = document.getElementById('source')
let addButton = document.getElementById('add-input')

inputName.onkeyup = function () {
  document.getElementById('input-name').textContent = inputName.value;
}
inputSource.onkeyup = function () {
  document.getElementById('input-video').src = inputSource.value
}
addButton.onclick = function () {
  let clone = document.getElementById('example-card').cloneNode(true)
  clone.removeAttribute('id')
  document.querySelector('.cards').append(clone)



  console.log('New card created')
}


//Sidenav Warnings
//Я потом нормально сделаю, честно..
function openNav() {
  document.querySelector(".warnings-container").style.width = "600px";
}
function closeNav() {
  document.querySelector(".warnings-container").style.width = "0";
}

