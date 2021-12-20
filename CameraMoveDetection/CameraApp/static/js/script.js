//Sidenav Warnings
//Я потом нормально сделаю, честно..
function openNav() {
  document.querySelector(".warnings-container").style.width = "65%";    
}
function closeNav() {
  document.querySelector(".warnings-container").style.width = "0";
}




//Table func
let table = document.querySelector('.warnings-table')
let cells = document.getElementsByName('alarmCell')

for (let cell of cells) {
  cell.onclick = function () {
    console.log('Cell click!')
    getImage()
  }
}


//Cards
let cards = document.querySelectorAll('.card')
let videoName = document.querySelector('.input-info')
let videoInput = document.getElementById('video-input')

// Input name func
for (let card of cards) {
  card.onclick = function () {
    console.log('click on card!')
    //input name
    videoName.textContent = card.textContent;

    closeNav();
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

let tests = document.querySelectorAll('.input-name')

//Right Click Menu
//Open menu when click on card
for (let card of cards) {
  card.oncontextmenu = rightClick;
}

//Hide menu when click on page
document.onclick = hideMenu;

function hideMenu() {
  document.getElementById("contextMenu")
    .style.display = "none"
}

function rightClick(e) {
  e.preventDefault();

  if (document.getElementById("contextMenu").style.display == "block") {
    hideMenu();
  } else {
    var menu = document.getElementById("contextMenu")
    menu.style.display = 'block';
    menu.style.left = e.pageX + "px";
    menu.style.top = e.pageY + "px";
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

// Add Input
// let inputName = document.getElementById('name')
// let inputSource = document.getElementById('source')
// let addButton = document.getElementById('add-input')
 //let inputname = document.getelementbyid('name')
 //let inputsource = document.getelementbyid('source')
 //let addbutton = document.getelementbyid('add-input')

 //inputname.onkeyup = function () {
 //  document.getelementbyid('input-name').textcontent = inputname.value;
 //}
 //inputsource.onkeyup = function () {
 //  document.getelementbyid('input-video').src = inputsource.value
 //}
 //addbutton.onclick = function () {
 //  let clone = document.getelementbyid('example-card').clonenode(true)
 //  clone.removeattribute('id')
 //  document.queryselector('.cards').append(clone)
  
 //  console.log('new card created')
 //}


