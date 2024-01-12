
function init() {
  //  console.log("Test scrip");
}


function isFlip(otherUserID,activeUserID,receiver){
  let rightFlip; 
  if ((otherUserID != activeUserID) ||(activeUserID == receiver)) { 
    rightFlip = ' rightFlip'; 
  }else{
    rightFlip="";
  }
  return rightFlip;
}


function getUserJson(jsonResponse) {
  let uList = []
  jsonResponse.users.forEach((us) => {
    uList.push(JSON.parse(us));
  });
  return uList;
}

function getMessageJson(jsonResponse) {
  let mList = []
  jsonResponse.messages.forEach((ms) => {
    mList.push(JSON.parse(ms));
  });
  return mList;
}

function renderMessages(messList, userlist, otherUserID) {
  let content = "";
  console.log(messList);
  messList.forEach((u) => {   
    rightFlip = isFlip(otherUserID,u.fields.author,u.fields.receiver)
    content += ` <div class="message ${rightFlip}">[${u.fields.created_at}] ${userlist[u.fields.author - 1].fields.first_name}: <i>${u.fields.text}</i></div>`
  });
  //console.log(content);
  return content;
}

function renderUserList(userlist){
  let content = "";
  let i = 1;
  userlist.forEach((u) => {  
    content += `<ul class="demo-list-icon mdl-list"> <li class="mdl-list__item" onclick="getMessagWithUser(${i})">
      <span style="cursor:pointer" class="mdl-list__item-primary-content">
      <i class="material-icons mdl-list__item-icon">person</i>
     ${u.fields.first_name}</span></li> `;
    i++;
  });
  console.log(content);
  return content;
}

