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
let buttons = document.querySelectorAll('button')
let modals = document.querySelectorAll('.modal')
let span = document.getElementsByClassName('.close-modal');

for (let button of buttons) {
  button.onclick = function () {
    for (let modal of modals) {
      if (button.id === modal.id) {
        modal.style.display = "block";

        //close when click outside
        window.onclick = function (event) {
          if (event.target == modal) {
            modal.style.display = "none";
          }
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
  clone.classList.add('test')
  document.querySelector('.cards').append(clone)

  
  // //for click event to work
  // clone.addEventListener('click', Click, false)

  // var newDiv = document.createElement('card')
  // newDiv.cloneNode(true)
  // document.querySelector('.cards').appendChild(newDiv)
  
  console.log('New card created')
  console.log(test)
}


